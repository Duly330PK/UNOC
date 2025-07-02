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
    "graph": None,  # NEU: Für Graphenanalyse
    "events": [],
    "undo_stack": [],
    "redo_stack": []
}

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
    if not topology.rings:
        return

    for ring in topology.rings:
        rpl_link = next((l for l in topology.links if l.id == ring.rpl_link_id), None)
        if rpl_link:
            rpl_link.status = 'blocking'
            add_event(f"ERPS: Link '{rpl_link.id}' in Ring '{ring.id}' set to BLOCKING.")

def handle_ring_failure(broken_link_id: str):
    """Checks if a broken link is part of a ring and triggers failover."""
    topology = app_state["topology"]
    # Find the ring that contains the broken link
    affected_ring = None
    for r in topology.rings:
        # A link is in the ring if both its source and target nodes are part of the ring's node list
        link_nodes = set()
        for l in topology.links:
            if l.id == broken_link_id:
                link_nodes.add(l.source)
                link_nodes.add(l.target)
                break
        
        if link_nodes.issubset(set(r.nodes)):
            affected_ring = r
            break

    if not affected_ring or affected_ring.rpl_link_id == broken_link_id:
        return None # No failover if the RPL itself fails or no ring is affected

    # Failover Logic: Unblock the RPL
    rpl_link = next((l for l in topology.links if l.id == affected_ring.rpl_link_id), None)
    if rpl_link and rpl_link.status == 'blocking':
        failover_command = UpdateLinkStatusCommand(topology, rpl_link.id, 'up')
        add_event(f"ERPS: Failover in Ring '{affected_ring.id}'. Unblocking RPL '{rpl_link.id}'.")
        return failover_command
    return None

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
    """Calculates and returns high-level statistics about the network state."""
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
    # Alarms do not count 'blocking' links as down
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

    # The command for the original action
    main_command = UpdateLinkStatusCommand(topology, link_id, payload.status)
    
    composite_command = CompositeCommand()
    composite_command.add(main_command)
    
    # NEW: Check if a ring failover needs to be triggered
    if payload.status in ['down', 'degraded']:
        failover_cmd = handle_ring_failure(link_id)
        if failover_cmd:
            composite_command.add(failover_cmd)
            
    try:
        execute_command(composite_command)
        add_event(f"SIMULATION: Status of link '{link_id}' changed to '{payload.status}'.")
        # Return the updated link object, as the original command might be part of a composite
        return jsonify(target_link.model_dump())
    except ValueError as e:
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
    """
    Simulates a fiber cut affecting a specific node (e.g., a splitter).
    All downstream links and devices will be set to 'down'/'offline'.
    """
    payload = request.get_json()
    cut_node_id = payload.get('node_id')
    if not cut_node_id or not app_state["graph"].has_node(cut_node_id):
        abort(404, description=f"Node '{cut_node_id}' not found.")

    graph = app_state["graph"]
    topology = app_state["topology"]
    descendant_nodes = nx.descendants(graph, cut_node_id)

    affected_links = [
        link for link in topology.links
        if (link.source in descendant_nodes or link.source == cut_node_id)
        and (link.target in descendant_nodes or link.target == cut_node_id)
    ]

    composite_command = CompositeCommand()

    for node_id in descendant_nodes:
        composite_command.add(UpdateDeviceStatusCommand(topology, node_id, 'offline'))

    for link in affected_links:
        composite_command.add(UpdateLinkStatusCommand(topology, link.id, 'down'))

    execute_command(composite_command)
    add_event(f"SCENARIO: Fiber cut at '{cut_node_id}' affected {len(descendant_nodes)} devices and {len(affected_links)} links.")

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
        abort(404)

    with open(snapshot_path, 'r', encoding='utf-8') as f:
        snapshot_data = json.load(f)

    topology = Topology.model_validate(snapshot_data["topology"])
    app_state["topology"] = topology
    app_state["graph"] = build_graph(topology)
    app_state["events"] = snapshot_data.get("events", [])
    clear_history()
    # After loading a snapshot, re-initialize the rings to their defined state
    initialize_rings()

    add_event(f"SYSTEM: Snapshot '{snapshot_name}' loaded successfully.")
    return jsonify({"message": "Snapshot loaded."})

# --- Main Execution ---
if __name__ == '__main__':
    topology = load_and_validate_topology()
    app_state["topology"] = topology
    app_state["graph"] = build_graph(topology)
    initialize_rings() # NEU: Ring-Status initialisieren
    add_event("SYSTEM: Backend started, topology/graph loaded, rings initialized.")
    print("Starting UNOC backend server (v8 with ERPS Simulation)...")
    app.run(host='0.0.0.0', port=5000, debug=True)
