#
# UNOC - backend.py
#
# Main backend application with state, snapshots, and undo/redo functionality (now DB & WS driven).
# JETZT: Erweitert für L7-Dienst-Simulation (Phase 6).
#

import yaml
import sys
import datetime
import os
import json
from flask import Flask, jsonify, abort, request, g
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from pydantic import ValidationError

import networkx as nx
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session as DBSessionType

# Importiere Datenbank-Module und ORM-Modelle
from database import SessionLocal, init_db, Device, Link, Ring, Alarm

# Importiere die angepassten Command-Klassen
from commands import (
    Command,
    UpdateLinkStatusCommand,
    UpdateDeviceStatusCommand,
    CompositeCommand
)
# Importiere Pydantic-Schemas für Validierung und Serialisierung
from schemas import (
    Topology,
    Device as PydanticDevice,
    Link as PydanticLink,
    Ring as PydanticRing,
    UpdateLinkStatusPayload,
    UpdateDeviceStatusPayload,
    SUPPORTED_TOPOLOGY_VERSION
)

# --- Application Setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "super-geheimes-flask-socketio-schluessel!")
CORS(app, resources={r"/*": {"origins": ["*", "null"], "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:8000", "http://127.0.0.1:8000"])

# --- Physikalische Konstanten & Konfiguration ---
FIBER_LOSS_PER_KM = {
    '1310nm': 0.35,
    '1490nm': 0.40,
    '1270nm': 0.35,
    '1577nm': 0.25
}
CONNECTOR_LOSS_DB = 0.5
SPLICE_LOSS_DB = 0.1
MAINTENANCE_MARGIN_DB = 3.0

# --- Konfiguration für Gerätetypen ---
HEAD_END_TYPES = ['OLT', 'AON Switch']
END_DEVICE_TYPES = ['ONT', 'Business NT']

# --- In-Memory State ---
app_state = {
    "graph": nx.DiGraph(),
    "undo_stack": [],
    "redo_stack": []
}

# --- NEU/ERWEITERT FÜR PHASE 6: Konfiguration des virtuellen Routers & Dienste ---
VIRTUAL_ROUTER_CONFIG = {
    "wan_type": "DHCP",
    "vlan_tag": None,
    "pd_size_request": 56,
    "dns_server": "DG_DEFAULT" # Neuer Eintrag für DNS-Server
}

VIRTUAL_SIP_PHONE_CONFIG = {
    "registrar": "dg.voip.dg-w.de",
    "status": "UNREGISTERED" # Start-Status
}

# --- Datenbank-Session Management ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.before_request
def before_request():
    g.db = next(get_db())

@app.after_request
def after_request(response):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    return response

# --- Serialisierungs- & Event-Logik ---
def serialize_topology(db: DBSessionType) -> dict:
    devices = db.query(Device).all()
    links = db.query(Link).all()
    rings = db.query(Ring).all()
    device_id_map = {d.id: d.device_id_str for d in devices}
    serialized_devices = [{"id": d.device_id_str, "type": d.type, "status": d.status, "properties": d.properties, "coordinates": d.coordinates} for d in devices]
    serialized_links = [{"id": l.link_id_str, "source": device_id_map.get(l.source_id), "target": device_id_map.get(l.target_id), "status": l.status, "properties": l.properties} for l in links]
    serialized_rings = [{"id": r.ring_id_str, "name": r.name, "rpl_link_id": r.rpl_link_id_str, "nodes": [node.device_id_str for node in r.nodes]} for r in rings]
    return {"devices": serialized_devices, "links": serialized_links, "rings": serialized_rings}

def add_event(message: str):
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    event_message = f"[{timestamp}] {message}"
    try:
        socketio.emit('new_event', event_message)
    except RuntimeError as e:
        if "Working outside of request context" in str(e):
            print(f"WARN: Event '{event_message}' not emitted via WS (no request context during startup).")
        else:
            raise e

# --- Command & Graph-Logik ---
def execute_command(command: Command):
    command.execute()
    app_state["undo_stack"].append(command)
    app_state["redo_stack"].clear()
    build_graph_from_db(g.db)
    emit_full_state_updates(g.db)

def clear_history():
    app_state["undo_stack"].clear()
    app_state["redo_stack"].clear()
    try:
        emit_history_status()
    except RuntimeError as e:
        if "Working outside of request context" in str(e):
            pass
        else:
            raise e

def build_graph_from_db(db_session: DBSessionType):
    app_state["graph"].clear()
    devices = db_session.query(Device).all()
    links = db_session.query(Link).all()
    for device in devices:
        app_state["graph"].add_node(device.device_id_str, db_obj=device)
    for link in links:
        if link.source and link.target:
            source_id_str = link.source.device_id_str
            target_id_str = link.target.device_id_str
            app_state["graph"].add_edge(source_id_str, target_id_str, db_obj=link, link_id_str=link.link_id_str)
    print("In-Memory Graph wurde aus der Datenbank gebaut.")

# --- Realtime & Statistik-Logik ---
def emit_full_state_updates(db_session: DBSessionType):
    full_topology = serialize_topology(db_session)
    stats = get_current_topology_stats(db_session)
    history_status = get_current_history_status()
    active_alarms = db_session.query(Alarm).filter_by(status='ACTIVE').all()
    serialized_alarms = [{"id": a.id, "severity": a.severity, "status": a.status, "timestamp_raised": a.timestamp_raised, "affected_object_type": a.affected_object_type, "affected_object_id": a.affected_object_id, "description": a.description} for a in active_alarms]
    socketio.emit('full_state_update', {'devices': full_topology['devices'], 'links': full_topology['links'], 'rings': full_topology['rings'], 'stats': stats, 'history_status': history_status, 'alarms': serialized_alarms})

def emit_stats_update(db_session: DBSessionType):
    stats = get_current_topology_stats(db_session)
    socketio.emit('stats_update', stats)

def emit_history_status():
    status = get_current_history_status()
    socketio.emit('history_status_update', status)

def get_current_history_status() -> dict:
    return {"can_undo": len(app_state["undo_stack"]) > 0, "can_redo": len(app_state["redo_stack"]) > 0}

def get_current_topology_stats(db_session: DBSessionType) -> dict:
    devices = db_session.query(Device).all()
    links = db_session.query(Link).all()
    devices_total = len(devices)
    devices_online = sum(1 for d in devices if d.status == 'online')
    links_total = len(links)
    links_up = sum(1 for l in links if l.status == 'up')
    links_with_issue = sum(1 for l in links if l.status not in ['up', 'blocking'])
    devices_with_issue = devices_total - devices_online
    alarms = devices_with_issue + links_with_issue
    return {"devices_total": devices_total, "devices_online": devices_online, "links_total": links_total, "links_up": links_up, "alarms": alarms}

# --- Ring-Logik ---
def initialize_rings(db_session: DBSessionType):
    rings = db_session.query(Ring).all()
    if not rings:
        return
    for ring in rings:
        rpl_link = db_session.query(Link).filter_by(link_id_str=ring.rpl_link_id_str).first()
        if rpl_link and rpl_link.status != 'blocking':
            rpl_link.status = 'blocking'
            db_session.add(rpl_link)
            db_session.commit()
            db_session.refresh(rpl_link)
            add_event(f"ERPS: Link '{rpl_link.link_id_str}' in Ring '{ring.name}' set to BLOCKING.")

def handle_ring_failure(db_session: DBSessionType, broken_link_id_str: str):
    affected_ring = None
    rings = db_session.query(Ring).all()
    if not rings:
        return None
    broken_link_db_obj = db_session.query(Link).filter_by(link_id_str=broken_link_id_str).first()
    if not broken_link_db_obj:
        return None
    for r in rings:
        ring_node_ids_str = {node.device_id_str for node in r.nodes}
        if broken_link_db_obj.source.device_id_str in ring_node_ids_str and broken_link_db_obj.target.device_id_str in ring_node_ids_str:
            affected_ring = r
            break
    if not affected_ring or affected_ring.rpl_link_id_str == broken_link_id_str:
        return None
    rpl_link = db_session.query(Link).filter_by(link_id_str=affected_ring.rpl_link_id_str).first()
    if rpl_link and rpl_link.status == 'blocking':
        failover_command = UpdateLinkStatusCommand(db_session, rpl_link.link_id_str, 'up')
        add_event(f"ERPS: Failover in Ring '{affected_ring.name}'. Unblocking RPL '{rpl_link.link_id_str}'.")
        return failover_command
    return None
    
# --- Alarm- & Berechnungs-Logik (Layer 1 & 2) ---
def check_thresholds_and_update_alarms(db, updated_object, **kwargs):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    alarm_changed = False

    if isinstance(updated_object, Link) and updated_object.properties.get("link_technology") == "PtP":
        utilization = updated_object.properties.get('utilization_percent', 0)
        guaranteed_bw = updated_object.properties.get('guaranteed_bandwidth_gbps', 0)
        existing_alarm = db.query(Alarm).filter_by(affected_object_id=updated_object.link_id_str, description="SLA Violation Risk", status="ACTIVE").first()
        if guaranteed_bw > 0 and utilization > 80 and not existing_alarm:
            new_alarm = Alarm(severity="MAJOR", status="ACTIVE", timestamp_raised=now, affected_object_type="link", affected_object_id=updated_object.link_id_str, description="SLA Violation Risk")
            db.add(new_alarm)
            alarm_changed = True
        elif utilization <= 80 and existing_alarm:
            existing_alarm.status = "CLEARED"
            existing_alarm.timestamp_cleared = now
            alarm_changed = True

    if isinstance(updated_object, Device) and updated_object.type in END_DEVICE_TYPES:
        signal_status = kwargs.get("signal_status")
        existing_alarm = db.query(Alarm).filter_by(affected_object_id=updated_object.device_id_str, description="Loss of Signal", status="ACTIVE").first()
        if signal_status == "LOS" and not existing_alarm:
            new_alarm = Alarm(severity="CRITICAL", status="ACTIVE", timestamp_raised=now, affected_object_type="device", affected_object_id=updated_object.device_id_str, description="Loss of Signal")
            db.add(new_alarm)
            alarm_changed = True
        elif signal_status != "LOS" and existing_alarm:
            existing_alarm.status = "CLEARED"
            existing_alarm.timestamp_cleared = now
            alarm_changed = True

    if alarm_changed:
        db.commit()
        emit_full_state_updates(db)

def calculate_signal_power(db: DBSessionType, end_device_id_str: str):
    graph = app_state["graph"]
    end_node = graph.nodes.get(end_device_id_str)
    if not end_node or end_node['db_obj'].type not in END_DEVICE_TYPES:
        return {"error": f"Device is not a valid end device ({', '.join(END_DEVICE_TYPES)})"}

    path_nodes = None
    head_end_device_ids = [n for n, d in graph.nodes(data=True) if d.get('db_obj') and d['db_obj'].type in HEAD_END_TYPES]
    
    for start_node_id in head_end_device_ids:
        if nx.has_path(graph, source=start_node_id, target=end_device_id_str):
            path_nodes = nx.shortest_path(graph, source=start_node_id, target=end_device_id_str)
            break
    
    if not path_nodes:
        return {"error": "No path from any head-end found", "status": "NO_PATH", "power_dbm": None, "budget": {}}

    path_links = [graph.get_edge_data(path_nodes[i], path_nodes[i+1])['db_obj'] for i in range(len(path_nodes) - 1)]
    is_ptp_path = any(link.properties.get("link_technology") == "PtP" for link in path_links)
    start_node_db = graph.nodes[path_nodes[0]]['db_obj']
    transmit_power = float(start_node_db.properties.get("transmit_power_dbm", 0.0))
    ont_tech = end_node['db_obj'].properties.get("technology", "GPON")
    downstream_wavelength = '1490nm' if ont_tech == 'GPON' else '1577nm'
    
    budget_breakdown = {
        "Transmit Power": transmit_power,
        "Fiber Loss": 0.0,
        "Splitter Loss": 0.0,
        "Connector Loss": 0.0,
        "Splice Loss": 0.0,
        "Maintenance Margin": MAINTENANCE_MARGIN_DB
    }

    for link in path_links:
        props = link.properties or {}
        budget_breakdown["Fiber Loss"] += props.get("length_km", 0) * FIBER_LOSS_PER_KM.get(downstream_wavelength, 0.4)
        budget_breakdown["Connector Loss"] += props.get("connector_count", 0) * CONNECTOR_LOSS_DB
        budget_breakdown["Splice Loss"] += props.get("splice_count", 0) * SPLICE_LOSS_DB
        
    if not is_ptp_path:
        for node_id in path_nodes:
            node_db = graph.nodes[node_id]['db_obj']
            if node_db.type == 'Splitter':
                props = node_db.properties or {}
                budget_breakdown["Splitter Loss"] += float(props.get("insertion_loss_db", 0.0))

    total_loss = (
        budget_breakdown["Fiber Loss"] +
        budget_breakdown["Splitter Loss"] +
        budget_breakdown["Connector Loss"] +
        budget_breakdown["Splice Loss"] +
        budget_breakdown["Maintenance Margin"]
    )
    
    received_power = transmit_power - total_loss
    end_device_db_obj = end_node['db_obj']
    end_device_props = end_device_db_obj.properties or {}
    sensitivity = float(end_device_props.get("sensitivity_min_dbm", -30.0))
    device_status = "online" if received_power >= sensitivity else "LOS"
    check_thresholds_and_update_alarms(db, end_device_db_obj, signal_status=device_status)

    return {
        "status": device_status,
        "power_dbm": round(received_power, 2),
        "budget": {k: round(v, 2) for k, v in budget_breakdown.items()},
        "total_loss": round(total_loss, 2),
        "path_technology": "PtP" if is_ptp_path else "PON"
    }

# --- Emulationslogik für Layer 2/3 (unverändert von Phase 5) ---
def simulate_connection_attempt():
    """
    Simuliert den Verbindungsaufbau basierend auf der Konfiguration des virtuellen Routers.
    Bildet die Logik der Deutschen Glasfaser nach.
    """
    config = VIRTUAL_ROUTER_CONFIG

    vlan_tag_value = config.get("vlan_tag")
    if vlan_tag_value not in [None, ""]:
        try:
            int(vlan_tag_value)
            return {"status": "FAILED", "reason": "Unerwartetes VLAN-Tag am WAN-Port. DG arbeitet auf dem Access-Port."}
        except (ValueError, TypeError):
            pass
        
    if config["wan_type"] != "DHCP":
        return {"status": "FAILED", "reason": f"Authentifizierung fehlgeschlagen: DG verwendet kein {config['wan_type']}."}

    ipv4_address = "100.64.10.5"

    ipv6_prefix = None
    pd_request_size = int(config["pd_size_request"])
    
    if pd_request_size == 56:
        ipv6_prefix = "2a00:6020:abcd:ef00::/56"
    else:
        ipv6_prefix = "2a00:6020:abcd:ef00::/64"
    
    return {
        "status": "CONNECTED",
        "ipv4": {"address": ipv4_address, "type": "CGNAT"},
        "ipv6": {"prefix": ipv6_prefix, "delegated_size": pd_request_size}
    }

# --- NEU FÜR PHASE 6: Emulationslogik für Layer 7 ---
def simulate_sip_registration():
    """Simuliert den SIP-Registrierungsversuch."""
    
    # Simuliere nur, wenn eine Internetverbindung besteht
    if simulate_connection_attempt()["status"] != "CONNECTED":
        VIRTUAL_SIP_PHONE_CONFIG["status"] = "UNREGISTERED (No Internet)"
        return VIRTUAL_SIP_PHONE_CONFIG

    # 1. DNS-Problem simulieren
    if VIRTUAL_ROUTER_CONFIG["dns_server"] == "EXTERNAL":
        # Der DG-interne Registrar ist im "externen" DNS nicht auflösbar
        VIRTUAL_SIP_PHONE_CONFIG["status"] = "FAILED (Registrar not found)"
        add_event("VOIP-SIM: SIP registration failed. Reason: Registrar DNS lookup failed with external DNS.")
        return VIRTUAL_SIP_PHONE_CONFIG

    # 2. Erfolgreiche Registrierung simulieren
    VIRTUAL_SIP_PHONE_CONFIG["status"] = "REGISTERED"
    add_event("VOIP-SIM: SIP registration successful with DG DNS.")
    return VIRTUAL_SIP_PHONE_CONFIG

# --- API Endpoints ---
@app.route('/api/topology', methods=['GET'])
def get_topology_api():
    db = g.db
    topology_data = serialize_topology(db)
    stats = get_current_topology_stats(db)
    history_status = get_current_history_status()
    return jsonify({'devices': topology_data['devices'], 'links': topology_data['links'], 'rings': topology_data['rings'], 'stats': stats, 'history_status': history_status})

@app.route('/api/topology/stats', methods=['GET'])
def get_topology_stats_api():
    db = g.db
    return jsonify(get_current_topology_stats(db))

@app.route('/api/events', methods=['GET'])
def get_events_api():
    return jsonify(["Events sind jetzt über WebSockets verfügbar."])

@app.route('/api/history/status', methods=['GET'])
def get_history_status_api():
    return jsonify(get_current_history_status())

@app.route('/api/links/<string:link_id_str>/status', methods=['POST'])
def update_link_status(link_id_str: str):
    db = g.db
    try:
        payload = UpdateLinkStatusPayload.model_validate(request.get_json())
    except ValidationError as e:
        abort(422, description=e.errors())
    target_link = db.query(Link).filter_by(link_id_str=link_id_str).first()
    if not target_link:
        abort(404, description=f"Link with ID '{link_id_str}' not found.")
    main_command = UpdateLinkStatusCommand(db, link_id_str, payload.status)
    composite_command = CompositeCommand(db)
    composite_command.add(main_command)
    if payload.status in ['down', 'degraded']:
        failover_cmd = handle_ring_failure(db, link_id_str)
        if failover_cmd:
            composite_command.add(failover_cmd)
    try:
        execute_command(composite_command)
        add_event(f"SIMULATION: Status of link '{link_id_str}' changed to '{payload.status}'.")
        return jsonify({"message": f"Link '{link_id_str}' status updated."})
    except ValueError as e:
        db.rollback()
        abort(500, description=str(e))

@app.route('/api/devices/<string:device_id_str>/signal', methods=['GET'])
def get_device_signal(device_id_str: str):
    db = g.db
    device = db.query(Device).filter_by(device_id_str=device_id_str).first()
    if not device:
        abort(404, description="Device not found.")
    
    if device.type not in END_DEVICE_TYPES:
        return jsonify({"status": "NOT_APPLICABLE", "power_dbm": None, "message": f"Device type '{device.type}' is not a supported signal end-device."})
    
    signal_info = calculate_signal_power(db, device_id_str)
    return jsonify(signal_info)


@app.route('/api/links/<string:link_id_str>/utilization', methods=['POST'])
def set_link_utilization(link_id_str: str):
    db = g.db
    payload = request.get_json()
    utilization = payload.get('utilization')
    if utilization is None or not isinstance(utilization, (int, float)):
        abort(400, description="Missing or invalid 'utilization' value.")
    if not (0 <= utilization <= 100):
        abort(400, description="'utilization' must be between 0 and 100.")
    link = db.query(Link).filter_by(link_id_str=link_id_str).first()
    if not link:
        abort(404, description=f"Link with ID '{link_id_str}' not found.")
    
    props = link.properties.copy() if link.properties else {}
    props['utilization_percent'] = utilization
    link.properties = props
    db.add(link)
    
    check_thresholds_and_update_alarms(db, link)
    db.commit()
    
    add_event(f"LINK-UTIL: Utilization of link '{link_id_str}' set to {utilization}%.")
    emit_full_state_updates(db)
    return jsonify({"message": f"Utilization of link '{link_id_str}' set to {utilization}%."})

# --- ERWEITERT FÜR PHASE 6: Endpunkt für die virtuelle Router-Konfiguration ---
@app.route('/api/simulation/virtual-router/config', methods=['POST'])
def configure_virtual_router():
    """
    Nimmt eine Konfiguration vom Frontend entgegen, aktualisiert den globalen State
    und triggert die Verbindungs- und Dienst-Simulation.
    """
    config_data = request.get_json()
    if not config_data:
        abort(400, "Keine Konfigurationsdaten empfangen.")

    # Aktualisiere die globale Konfiguration sicher
    VIRTUAL_ROUTER_CONFIG.update(config_data)
    add_event(f"ROUTER-SIM: Received new config: {config_data}")
    
    # Simuliere einen Verbindungs-Neustart und den SIP-Versuch
    connection_result = simulate_connection_attempt()
    sip_result = simulate_sip_registration()

    # Sende alle relevanten Status an die Clients
    socketio.emit('full_service_status', {
        "connection": connection_result,
        "sip": sip_result
    })
    
    return jsonify({"message": "Configuration applied and services re-evaluated."})


@app.route('/api/simulation/trace-path', methods=['POST'])
def trace_path():
    db = g.db
    payload = request.get_json()
    start_node_str = payload.get('start_node')
    end_node_str = payload.get('end_node')
    if not start_node_str or not end_node_str:
        abort(400, description="Missing 'start_node' or 'end_node' in request.")
    build_graph_from_db(db)
    graph = app_state["graph"]
    if not graph.has_node(start_node_str) or not graph.has_node(end_node_str):
        abort(404, description="One of the specified nodes does not exist.")
    try:
        active_graph = nx.Graph()
        active_graph.add_nodes_from([d.device_id_str for d in db.query(Device).all()])
        active_links = []
        for l in db.query(Link).all():
            if l.status == 'up' and l.source and l.target:
                active_links.append((l.source.device_id_str, l.target.device_id_str))
        active_graph.add_edges_from(active_links)
        path_nodes_str = nx.shortest_path(active_graph, source=start_node_str, target=end_node_str)
        path_links_str = []
        for i in range(len(path_nodes_str) - 1):
            u_str, v_str = path_nodes_str[i], path_nodes_str[i+1]
            link_obj = db.query(Link).filter((Link.source.has(device_id_str=u_str) & Link.target.has(device_id_str=v_str)) | (Link.source.has(device_id_str=v_str) & Link.target.has(device_id_str=u_str))).first()
            if link_obj:
                path_links_str.append(link_obj.link_id_str)
        return jsonify({"nodes": path_nodes_str, "links": path_links_str})
    except nx.NetworkXNoPath:
        return jsonify({"nodes": [], "links": []})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/api/simulation/undo', methods=['POST'])
def undo_last_action():
    db = g.db
    if not app_state["undo_stack"]:
        abort(400, description="Nothing to undo.")
    command = app_state["undo_stack"].pop()
    try:
        command.undo()
        app_state["redo_stack"].append(command)
        add_event("SYSTEM: Undid last action.")
        build_graph_from_db(db)
        emit_full_state_updates(db)
        return jsonify({"message": "Action undone."})
    except ValueError as e:
        db.rollback()
        abort(500, description=str(e))

@app.route('/api/simulation/redo', methods=['POST'])
def redo_last_action():
    db = g.db
    if not app_state["redo_stack"]:
        abort(400, description="Nothing to redo.")
    command = app_state["redo_stack"].pop()
    try:
        command.execute()
        app_state["undo_stack"].append(command)
        add_event("SYSTEM: Redid last action.")
        build_graph_from_db(db)
        emit_full_state_updates(db)
        return jsonify({"message": "Action redone."})
    except ValueError as e:
        db.rollback()
        abort(500, description=str(e))

@app.route('/api/simulation/fiber-cut', methods=['POST'])
def fiber_cut():
    db = g.db
    payload = request.get_json()
    cut_node_id_str = payload.get('node_id')
    build_graph_from_db(db)
    graph = app_state["graph"]
    if not cut_node_id_str or not graph.has_node(cut_node_id_str):
        abort(404, description=f"Node '{cut_node_id_str}' not found.")
    descendant_nodes_str = nx.descendants(graph, cut_node_id_str)
    affected_nodes_set_str = descendant_nodes_str.union({cut_node_id_str})
    composite_command = CompositeCommand(db)
    for node_id_str in affected_nodes_set_str:
        device = db.query(Device).filter_by(device_id_str=node_id_str).first()
        if device and device.status != 'offline':
            composite_command.add(UpdateDeviceStatusCommand(db, node_id_str, 'offline'))
    affected_device_objs = db.query(Device).filter(Device.device_id_str.in_(affected_nodes_set_str)).all()
    device_ids_in_set = [d.id for d in affected_device_objs]
    affected_links = db.query(Link).filter((Link.source_id.in_(device_ids_in_set)) | (Link.target_id.in_(device_ids_in_set))).all()
    for link in affected_links:
        if link.status != 'down':
            composite_command.add(UpdateLinkStatusCommand(db, link.link_id_str, 'down'))
    if composite_command.commands:
        try:
            execute_command(composite_command)
            add_event(f"SCENARIO: Fiber cut at '{cut_node_id_str}' affected {len(affected_nodes_set_str)} devices.")
            return jsonify({"message": f"Fiber cut scenario at '{cut_node_id_str}' executed."})
        except ValueError as e:
            db.rollback()
            abort(500, description=str(e))
    else:
        return jsonify({"message": "No changes needed for fiber cut scenario."})

# --- Snapshot Endpoints ---
@app.route('/api/snapshot/save', methods=['POST'])
def save_snapshot():
    db = g.db
    snapshot_name = request.get_json()['name']
    if not snapshot_name:
        abort(400, description="Snapshot name is required.")
    try:
        topology_data = serialize_topology(db)
        snapshot = {"version": "1.0.0", "devices": topology_data["devices"], "links": topology_data["links"], "rings": topology_data["rings"]}
        SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), 'snapshots')
        if not os.path.exists(SNAPSHOT_DIR):
            os.makedirs(SNAPSHOT_DIR)
        snapshot_path = os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.json")
        with open(snapshot_path, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2)
        add_event(f"SYSTEM: Snapshot '{snapshot_name}' saved.")
        return jsonify({"message": "Snapshot saved."}), 201
    except Exception as e:
        db.rollback()
        abort(500, description=f"Failed to save snapshot: {str(e)}")

@app.route('/api/snapshot/load', methods=['POST'])
def load_snapshot():
    db = g.db
    try:
        snapshot_name = request.get_json()['name']
        if not snapshot_name:
            abort(400, description="Snapshot name is required.")
        SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), 'snapshots')
        snapshot_path = os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.json")
        if not os.path.exists(snapshot_path):
            abort(404, "Snapshot not found.")
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            snapshot_data = json.load(f)
        from sqlalchemy import text
        db.execute(text("DELETE FROM ring_device_association"))
        db.query(Link).delete()
        db.query(Ring).delete()
        db.query(Device).delete()
        db.commit()
        device_map = {}
        for device_data in snapshot_data['devices']:
            new_device = Device(device_id_str=device_data['id'], type=device_data['type'], status=device_data['status'], properties=device_data.get('properties', {}), coordinates=device_data.get('coordinates'))
            db.add(new_device)
            db.flush()
            device_map[device_data['id']] = new_device
        db.commit()
        for link_data in snapshot_data['links']:
            source_device = device_map.get(link_data['source'])
            target_device = device_map.get(link_data['target'])
            if not source_device or not target_device:
                raise ValueError(f"Device for link '{link_data['id']}' not found in snapshot.")
            new_link = Link(link_id_str=link_data['id'], source_id=source_device.id, target_id=target_device.id, status=link_data['status'], properties=link_data.get('properties', {}))
            db.add(new_link)
        db.commit()
        for ring_data in snapshot_data.get('rings', []):
            node_devices = [device_map[node_id] for node_id in ring_data['nodes']]
            new_ring = Ring(ring_id_str=ring_data['id'], name=ring_data['name'], rpl_link_id_str=ring_data['rpl_link_id'], nodes=node_devices)
            db.add(new_ring)
        db.commit()
        build_graph_from_db(db)
        clear_history()
        initialize_rings(db)
        add_event(f"SYSTEM: Snapshot '{snapshot_name}' loaded successfully.")
        emit_full_state_updates(db)
        return jsonify({"message": "Snapshot loaded."})
    except Exception as e:
        db.rollback()
        abort(500, description=f"Failed to load snapshot: {str(e)}")

# --- WebSocket Event Handlers ---
@socketio.on('connect')
def handle_connect():
    print(f'Client verbunden: {request.sid}')

@socketio.on('request_initial_data')
def handle_initial_data_request():
    db = SessionLocal()
    try:
        full_topology = serialize_topology(db)
        stats = get_current_topology_stats(db)
        history_status = get_current_history_status()
        active_alarms = db.query(Alarm).filter_by(status='ACTIVE').all()
        serialized_alarms = [{"id": a.id, "severity": a.severity, "status": a.status, "timestamp_raised": a.timestamp_raised, "affected_object_type": a.affected_object_type, "affected_object_id": a.affected_object_id, "description": a.description} for a in active_alarms]
        socketio.emit('initial_topology', {'devices': full_topology['devices'], 'links': full_topology['links'], 'rings': full_topology['rings'], 'stats': stats, 'history_status': history_status, 'alarms': serialized_alarms}, room=request.sid)
    finally:
        db.close()

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client getrennt: {request.sid}')

# --- Main Execution ---
if __name__ == '__main__':
    print("Initialisiere Datenbank-Schema...")
    init_db()
    print("Schema initialisiert.")
    with SessionLocal() as db:
        build_graph_from_db(db)
        initialize_rings(db)
    SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), 'snapshots')
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)
    add_event("SYSTEM: Backend started with PostgreSQL & WebSockets. Topology loaded, rings initialized.")
    print("Starting UNOC Backend Server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)