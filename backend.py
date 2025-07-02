#
# UNOC - backend.py
#
# Main backend application with data validation, in-memory state, and snapshots.
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

# --- Application Setup ---
app = Flask(__name__)
CORS(app)

# Define the directory for snapshots
SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), 'snapshots')

# --- In-Memory State ---
app_state = {
    "topology": None,
    "events": []
}

# --- Helper Functions ---
def add_event(message: str):
    """Adds a timestamped event to the in-memory event log."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    app_state["events"].insert(0, f"[{timestamp}] {message}")
    app_state["events"] = app_state["events"][:100]

# --- Data Loading and Initialization ---
def load_and_validate_topology(filepath="topology.yml"):
    """Loads and validates network topology data from a YAML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"FATAL: Topology file not found at '{filepath}'. Exiting.", file=sys.stderr)
        sys.exit(1)

    try:
        topology = Topology.model_validate(data)
        if topology.version != SUPPORTED_TOPOLOGY_VERSION:
            raise ValueError(f"Unsupported version '{topology.version}'. Requires '{SUPPORTED_TOPOLOGY_VERSION}'.")

        device_ids = {device.id for device in topology.devices}
        for link in topology.links:
            if link.source not in device_ids or link.target not in device_ids:
                raise ValueError(f"Link '{link.id}' references a non-existent device.")

        return topology
    except (ValidationError, ValueError) as e:
        print(f"FATAL: Invalid data in '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


# --- API Endpoints ---
@app.route('/api/topology', methods=['GET'])
def get_topology():
    """API endpoint to retrieve the current network topology from memory."""
    if app_state["topology"]:
        return jsonify(app_state["topology"].model_dump())
    abort(500, description="Topology has not been initialized.")

@app.route('/api/events', methods=['GET'])
def get_events():
    """API endpoint to retrieve the latest events."""
    return jsonify(app_state["events"])

@app.route('/api/links/<string:link_id>/status', methods=['POST'])
def update_link_status(link_id: str):
    """Simulation endpoint to update the status of a specific link."""
    try:
        payload = UpdateLinkStatusPayload.model_validate(request.get_json())
    except ValidationError as e:
        abort(422, description=e.errors())

    topology = app_state["topology"]
    target_link = next((link for link in topology.links if link.id == link_id), None)
    if not target_link:
        abort(404, description=f"Link with ID '{link_id}' not found.")

    old_status = target_link.status
    target_link.status = payload.status
    add_event(f"SIMULATION: Status of link '{link_id}' changed from '{old_status}' to '{payload.status}'.")
    return jsonify(target_link.model_dump())

@app.route('/api/snapshot/save', methods=['POST'])
def save_snapshot():
    """Saves the current application state to a snapshot file."""
    payload = request.get_json()
    if not payload or 'name' not in payload:
        abort(400, description="Missing 'name' in request body.")
    
    snapshot_name = payload['name']
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)
        
    snapshot_path = os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.json")
    
    try:
        state_to_save = {
            "topology": app_state["topology"].model_dump(),
            "events": app_state["events"]
        }
        with open(snapshot_path, 'w', encoding='utf-8') as f:
            json.dump(state_to_save, f, indent=2)
        
        add_event(f"SYSTEM: Snapshot '{snapshot_name}' saved successfully.")
        return jsonify({"message": f"Snapshot '{snapshot_name}' saved."}), 201
    except Exception as e:
        abort(500, description=f"Failed to save snapshot: {e}")

@app.route('/api/snapshot/load', methods=['POST'])
def load_snapshot():
    """Loads the application state from a snapshot file."""
    payload = request.get_json()
    if not payload or 'name' not in payload:
        abort(400, description="Missing 'name' in request body.")
        
    snapshot_name = payload['name']
    snapshot_path = os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.json")
    
    if not os.path.exists(snapshot_path):
        abort(404, description=f"Snapshot '{snapshot_name}' not found.")
        
    try:
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            snapshot_data = json.load(f)
        
        # Validate and load state
        app_state["topology"] = Topology.model_validate(snapshot_data["topology"])
        app_state["events"] = snapshot_data.get("events", []) # Safely get events
        
        add_event(f"SYSTEM: Snapshot '{snapshot_name}' loaded successfully.")
        return jsonify({"message": f"Snapshot '{snapshot_name}' loaded."})
    except (ValidationError, KeyError) as e:
        abort(422, description=f"Invalid snapshot file format: {e}")
    except Exception as e:
        abort(500, description=f"Failed to load snapshot: {e}")


# --- Main Execution ---
if __name__ == '__main__':
    app_state["topology"] = load_and_validate_topology()
    add_event("SYSTEM: Backend started and topology loaded successfully.")
    print("Starting UNOC backend server (v4 with Snapshots)...")
    print(f"Required topology version: {SUPPORTED_TOPOLOGY_VERSION}")
    print("Access the API at http://127.0.0.1:5000/api/topology")
    app.run(host='0.0.0.0', port=5000, debug=True)