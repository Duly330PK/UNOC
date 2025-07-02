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

from schemas import Topology, UpdateLinkStatusPayload, SUPPORTED_TOPOLOGY_VERSION
from commands import UpdateLinkStatusCommand

# --- Application Setup ---
app = Flask(__name__)
CORS(app)
SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), 'snapshots')

# --- In-Memory State ---
app_state = {
    "topology": None,
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
    # Any new action clears the redo stack
    app_state["redo_stack"].clear()

def clear_history():
    """Clears undo/redo history, e.g., after loading a snapshot."""
    app_state["undo_stack"].clear()
    app_state["redo_stack"].clear()

# --- Data Loading and Initialization ---
def load_and_validate_topology(filepath="topology.yml"):
    # (Dieser Code bleibt unverändert von der letzten Version)
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

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(app_state["events"])

@app.route('/api/history/status', methods=['GET'])
def get_history_status():
    """Returns the status of undo/redo stacks."""
    return jsonify({
        "can_undo": len(app_state["undo_stack"]) > 0,
        "can_redo": len(app_state["redo_stack"]) > 0
    })

# --- Simulation Endpoints ---
@app.route('/api/links/<string:link_id>/status', methods=['POST'])
def update_link_status(link_id: str):
    try:
        payload = UpdateLinkStatusPayload.model_validate(request.get_json())
    except ValidationError as e:
        abort(422, description=e.errors())

    topology = app_state["topology"]
    if not any(link.id == link_id for link in topology.links):
        abort(404, description=f"Link with ID '{link_id}' not found.")
        
    command = UpdateLinkStatusCommand(topology, link_id, payload.status)
    try:
        execute_command(command)
        add_event(f"SIMULATION: Status of link '{link_id}' changed to '{payload.status}'.")
        return jsonify(command._find_link().model_dump())
    except ValueError as e:
        abort(500, description=str(e))

@app.route('/api/simulation/undo', methods=['POST'])
def undo_last_action():
    """Undoes the last executed command."""
    if not app_state["undo_stack"]:
        abort(400, description="Nothing to undo.")
        
    command = app_state["undo_stack"].pop()
    command.undo()
    app_state["redo_stack"].append(command)
    
    add_event(f"SYSTEM: Undid last action.")
    return jsonify({"message": "Action undone."})

@app.route('/api/simulation/redo', methods=['POST'])
def redo_last_action():
    """Redoes the last undone command."""
    if not app_state["redo_stack"]:
        abort(400, description="Nothing to redo.")
        
    command = app_state["redo_stack"].pop()
    command.execute()
    app_state["undo_stack"].append(command)
    
    add_event(f"SYSTEM: Redid last action.")
    return jsonify({"message": "Action redone."})

# --- Snapshot Endpoints (angepasst für History) ---
@app.route('/api/snapshot/save', methods=['POST'])
def save_snapshot():
    snapshot_name = request.get_json()['name']
    snapshot_path = os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.json")
    if not os.path.exists(SNAPSHOT_DIR): os.makedirs(SNAPSHOT_DIR)
    
    # 🟢 ZUERST Event hinzufügen
    add_event(f"SYSTEM: Snapshot '{snapshot_name}' saved.")
    
    # 🟢 DANN speichern (damit Event im Snapshot enthalten ist)
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
    if not os.path.exists(snapshot_path): abort(404)
    with open(snapshot_path, 'r', encoding='utf-8') as f: snapshot_data = json.load(f)
    app_state["topology"] = Topology.model_validate(snapshot_data["topology"])
    app_state["events"] = snapshot_data.get("events", [])
    clear_history() # WICHTIG: History beim Laden eines Snapshots zurücksetzen
    add_event(f"SYSTEM: Snapshot '{snapshot_name}' loaded successfully.")
    return jsonify({"message": "Snapshot loaded."})

# --- Main Execution ---
if __name__ == '__main__':
    app_state["topology"] = load_and_validate_topology()
    add_event("SYSTEM: Backend started and topology loaded successfully.")
    print("Starting UNOC backend server (v5 with Undo/Redo)...")
    app.run(host='0.0.0.0', port=5000, debug=True)