#
# UNOC - backend.py
#
# Main backend application with state, snapshots, and undo/redo functionality.
#

import yaml
import sys
import datetime
import os
import json
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from pydantic import ValidationError
import networkx as nx

from schemas import (
    Topology,
    UpdateLinkStatusPayload,
    UpdateDeviceStatusPayload,
    SUPPORTED_TOPOLOGY_VERSION
)
from commands import (
    UpdateLinkStatusCommand,
    UpdateDeviceStatusCommand,
    CompositeCommand
)

# --- Application Setup ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}}, supports_credentials=True, methods=["GET", "POST", "OPTIONS"])

SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), 'snapshots')

# --- In-Memory State ---
app_state = {
    "topology": None,
    "graph": None,  # Für Graphenanalyse
    "events": [],
    "undo_stack": [],
    "redo_stack": []
}

# --- Physikalische Konstanten ---
FIBER_LOSS_PER_KM = 0.35 # dB pro Kilometer

# --- Helper Functions ---
def add_event(message: str):
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    app_state["events"].insert(0, f"[{timestamp}] {message}")
    app_state["events"] = app_state["events"][:100]

def execute_command(command):
    """Executes a command and manages undo/redo stacks."""
    command.execute()
    app_state["undo_stack"].append(command)
    app_state["redo_stack"].clear()

def clear_history():
    """Clears undo/redo history, e.g., after loading a snapshot."""
    app_state["undo_stack"].clear()
    app_state["redo_stack"].clear()

def build_graph(topology: Topology) -> nx.DiGraph:
    """Builds a NetworkX directed graph from the topology data."""
    G = nx.DiGraph()
    for device in topology.devices:
        G.add_node(device.id, data=device)
    for link in topology.links:
        G.add_edge(link.source, link.target, data=link)
    return G

# --- Ring-Logik ---
def initialize_rings():
    """Sets the initial state for all defined rings (e.g., blocks RPL)."""
    topology = app_state["topology"]
    if not hasattr(topology, 'rings') or not topology.rings:
        return

    for ring in topology.rings:
        rpl_link = next((l for l in topology.links if l.id == ring.rpl_link_id), None)
        if rpl_link:
            rpl_link.status = 'blocking'
            add_event(f"ERPS: Link '{rpl_link.id}' in Ring '{ring.id}' set to BLOCKING.")

def handle_ring_failure(broken_link_id: str):
    """Checks if a broken link is part of a ring and triggers failover."""
    topology = app_state["topology"]
    affected_ring = None
    if not hasattr(topology, 'rings') or not topology.rings:
        return None
        
    for r in topology.rings:
        link_nodes = set()
        for l in topology.links:
            if l.id == broken_link_id:
                link_nodes.add(l.source)
                link_nodes.add(l.target)
                break
        
        if hasattr(r, 'nodes') and link_nodes.issubset(set(r.nodes)):
            affected_ring = r
            break

    if not affected_ring or affected_ring.rpl_link_id == broken_link_id:
        return None

    rpl_link = next((l for l in topology.links if l.id == affected_ring.rpl_link_id), None)
    if rpl_link and rpl_link.status == 'blocking':
        failover_command = UpdateLinkStatusCommand(topology, rpl_link.id, 'up')
        add_event(f"ERPS: Failover in Ring '{affected_ring.id}'. Unblocking RPL '{rpl_link.id}'.")
        return failover_command
    return None

# --- Berechnungslogik ---
def calculate_ont_power(ont_id: str):
    """
    Calculates the received optical power at a specific ONT.
    """
    graph = app_state["graph"]
    topology = app_state["topology"]

    try:
        olts = [d.id for d in topology.devices if d.type == 'OLT']
        path_to_olt = None
        for olt_id in olts:
            if nx.has_path(graph, olt_id, ont_id):
                path_to_olt = nx.shortest_path(graph, source=olt_id, target=ont_id)
                break
        if not path_to_olt:
            raise nx.NetworkXNoPath
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return {"status": "NO_PATH", "power_dbm": None}

    path_devices_data = [graph.nodes[node_id]['data'] for node_id in path_to_olt]
    path_links_data = [graph.get_edge_data(path_to_olt[i], path_to_olt[i+1])['data'] for i in range(len(path_to_olt) - 1)]

    for device in path_devices_data[1:]:
        if device.status == 'offline':
            return {"status": "NO_PATH", "power_dbm": None, "reason": f"Device {device.id} is offline"}
    
    for link in path_links_data:
        if link.status not in ['up', 'blocking']:
            return {"status": "NO_PATH", "power_dbm": None, "reason": f"Link {link.id} is {link.status}"}

    olt_device = path_devices_data[0]
    transmit_power = olt_device.properties.get("transmit_power_dbm", 0)

    total_loss = 0
    for link_data in path_links_data:
        total_loss += link_data.properties.get("length_km", 0) * FIBER_LOSS_PER_KM
    
    for device in path_devices_data:
        if device.type == 'Splitter':
            total_loss += device.properties.get("insertion_loss_db", 0)

    received_power = transmit_power - total_loss

    if received_power >= -25:
        signal_status = "GOOD"
    elif -28 < received_power < -25:
        signal_status = "WARNING"
    else:
        signal_status = "LOS"

    return {"status": signal_status, "power_dbm": round(received_power, 2)}


# --- Data Loading and Initialization ---
def load_and_validate_topology(filepath="topology.yml"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        topology = Topology.model_validate(data)
        if topology.version != SUPPORTED_TOPOLOGY_VERSION:
            raise ValueError(f"Unsupported version '{topology.version}'. Requires '{SUPPORTED_TOPOLOGY_VERSION}'.")
        device_ids = {d.id for d in topology.devices}
        for link in topology.links:
            if link.source not in device_ids or link.target not in device_ids:
                raise ValueError(f"Link '{link.id}' references a non-existent device.")
        return topology
    except (FileNotFoundError, ValidationError, ValueError) as e:
        print(f"FATAL: Could not load topology from '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)

# --- API Endpoints ---
@app.route('/api/topology', methods=['GET'])
def get_topology():
    if app_state["topology"]:
        return jsonify(app_state["topology"].model_dump())
    abort(500)

@app.route('/api/topology/stats', methods=['GET'])
def get_topology_stats():
    if not app_state["topology"]:
        abort(500, description="Topology not initialized.")
    
    devices = app_state["topology"].devices
    links = app_state["topology"].links
    
    stats = {
        "devices_total": len(devices),
        "devices_online": sum(1 for d in devices if d.status == 'online'),
        "links_total": len(links),
        "links_up": sum(1 for l in links if l.status == 'up'),
    }
    links_with_issue = sum(1 for l in links if l.status not in ['up', 'blocking'])
    devices_with_issue = stats["devices_total"] - stats["devices_online"]
    stats["alarms"] = devices_with_issue + links_with_issue
    
    return jsonify(stats)

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(app_state["events"])

@app.route('/api/history/status', methods=['GET'])
def get_history_status():
    return jsonify({
        "can_undo": len(app_state["undo_stack"]) > 0,
        "can_redo": len(app_state["redo_stack"]) > 0
    })

@app.route('/api/links/<string:link_id>/status', methods=['POST'])
def update_link_status(link_id: str):
    try:
        payload = UpdateLinkStatusPayload.model_validate(request.get_json())
    except ValidationError as e:
        abort(422, description=e.errors())

    topology = app_state["topology"]
    target_link = next((link for link in topology.links if link.id == link_id), None)
    if not target_link:
        abort(404, description=f"Link with ID '{link_id}' not found.")

    main_command = UpdateLinkStatusCommand(topology, link_id, payload.status)
    
    # KORREKTUR: CompositeCommand ohne Argumente initialisieren
    composite_command = CompositeCommand()
    composite_command.add(main_command)
    
    if payload.status in ['down', 'degraded']:
        failover_cmd = handle_ring_failure(link_id)
        if failover_cmd:
            composite_command.add(failover_cmd)
            
    try:
        execute_command(composite_command)
        add_event(f"SIMULATION: Status of link '{link_id}' changed to '{payload.status}'.")
        return jsonify(target_link.model_dump())
    except ValueError as e:
        abort(500, description=str(e))

@app.route('/api/devices/<string:device_id>/signal', methods=['GET'])
def get_device_signal(device_id: str):
    device = next((d for d in app_state["topology"].devices if d.id == device_id), None)
    if not device:
        abort(404, description="Device not found.")
    if device.type != 'ONT':
        return jsonify({"status": "NOT_APPLICABLE", "power_dbm": None})

    signal_info = calculate_ont_power(device_id)
    return jsonify(signal_info)

@app.route('/api/simulation/trace-path', methods=['POST'])
def trace_path():
    """
    Finds the shortest path between two nodes and returns the components.
    """
    payload = request.get_json()
    start_node = payload.get('start_node')
    end_node = payload.get('end_node')

    if not start_node or not end_node:
        abort(400, description="Missing 'start_node' or 'end_node' in request.")

    graph = app_state["graph"]
    if not graph.has_node(start_node) or not graph.has_node(end_node):
        abort(404, description="One of the specified nodes does not exist.")

    try:
        # Wir erstellen einen temporären Graphen
        active_graph = nx.Graph() 
        active_graph.add_nodes_from([d.id for d in app_state["topology"].devices])
        
        # KORREKTUR: Nur 'up'-Links für die Pfadsuche berücksichtigen
        active_links = [
            (l.source, l.target) for l in app_state["topology"].links if l.status == 'up'
        ]
        active_graph.add_edges_from(active_links)

        path_nodes = nx.shortest_path(active_graph, source=start_node, target=end_node)
        
        path_links = []
        for i in range(len(path_nodes) - 1):
            u, v = path_nodes[i], path_nodes[i+1]
            link_id = next(
                (l.id for l in app_state["topology"].links 
                 if (l.source == u and l.target == v) or 
                    (l.source == v and l.target == u)),
                None
            )
            if link_id:
                path_links.append(link_id)

        return jsonify({"nodes": path_nodes, "links": path_links})

    except nx.NetworkXNoPath:
        return jsonify({"nodes": [], "links": []})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/api/simulation/undo', methods=['POST'])
def undo_last_action():
    if not app_state["undo_stack"]:
        abort(400, description="Nothing to undo.")
    command = app_state["undo_stack"].pop()
    command.undo()
    app_state["redo_stack"].append(command)
    add_event("SYSTEM: Undid last action.")
    return jsonify({"message": "Action undone."})

@app.route('/api/simulation/redo', methods=['POST'])
def redo_last_action():
    if not app_state["redo_stack"]:
        abort(400, description="Nothing to redo.")
    command = app_state["redo_stack"].pop()
    command.execute()
    app_state["undo_stack"].append(command)
    add_event("SYSTEM: Redid last action.")
    return jsonify({"message": "Action redone."})

@app.route('/api/simulation/fiber-cut', methods=['POST'])
def fiber_cut():
    payload = request.get_json()
    cut_node_id = payload.get('node_id')
    if not cut_node_id or not app_state["graph"].has_node(cut_node_id):
        abort(404, description=f"Node '{cut_node_id}' not found.")

    graph = app_state["graph"]
    topology = app_state["topology"]
    
    descendant_nodes = nx.descendants(graph, cut_node_id)
    affected_nodes_set = descendant_nodes.union({cut_node_id})

    composite_command = CompositeCommand()

    for node_id in affected_nodes_set:
        device = next((d for d in topology.devices if d.id == node_id), None)
        if device and device.status != 'offline':
            composite_command.add(UpdateDeviceStatusCommand(topology, node_id, 'offline'))

    for link in topology.links:
        if link.source in affected_nodes_set or link.target in affected_nodes_set:
            if link.status != 'down':
                composite_command.add(UpdateLinkStatusCommand(topology, link.id, 'down'))

    if composite_command.commands:
        execute_command(composite_command)
        add_event(f"SCENARIO: Fiber cut at '{cut_node_id}' affected {len(affected_nodes_set)} devices.")

    return jsonify({"message": f"Fiber cut scenario at '{cut_node_id}' executed."})

# --- Snapshot Endpoints ---
@app.route('/api/snapshot/save', methods=['POST'])
def save_snapshot():
    snapshot_name = request.get_json()['name']
    snapshot_path = os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.json")
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)

    add_event(f"SYSTEM: Snapshot '{snapshot_name}' saved.")

    state_to_save = {
        "topology": app_state["topology"].model_dump(),
        "events": app_state["events"]
    }

    with open(snapshot_path, 'w', encoding='utf-8') as f:
        json.dump(state_to_save, f, indent=2)

    return jsonify({"message": "Snapshot saved."}), 201

@app.route('/api/snapshot/load', methods=['POST'])
def load_snapshot():
    snapshot_name = request.get_json()['name']
    snapshot_path = os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.json")
    if not os.path.exists(snapshot_path):
        abort(404, "Snapshot not found.")

    with open(snapshot_path, 'r', encoding='utf-8') as f:
        snapshot_data = json.load(f)

    topology = Topology.model_validate(snapshot_data["topology"])
    app_state["topology"] = topology
    app_state["graph"] = build_graph(topology)
    app_state["events"] = snapshot_data.get("events", [])
    clear_history()
    
    add_event(f"SYSTEM: Snapshot '{snapshot_name}' loaded successfully.")
    return jsonify({"message": "Snapshot loaded."})

# --- Main Execution ---
if __name__ == '__main__':
    topology = load_and_validate_topology()
    app_state["topology"] = topology
    app_state["graph"] = build_graph(topology)
    initialize_rings()
    add_event("SYSTEM: Backend started, topology/graph loaded, rings initialized.")
    print("Starting UNOC backend server (v11 with fixes)...")
    app.run(host='0.0.0.0', port=5000, debug=True)