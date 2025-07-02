import yaml
import sys
import datetime
import os
import json
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from pydantic import ValidationError

from schemas import Topology, UpdateLinkStatusPayload, SUPPORTED_TOPOLOGY_VERSION

app = Flask(__name__)
CORS(app)

# Globaler Applikationszustand
app_state = {
    "topology": None,
    "events": []
}

def add_event(message: str):
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    app_state["events"].insert(0, f"[{timestamp}] {message}")
    app_state["events"] = app_state["events"][:100]

def load_and_validate_topology(filepath="topology.yml"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"FATAL: Topology file not found at '{filepath}'. Exiting.", file=sys.stderr)
        sys.exit(1)

    try:
        topology = Topology.model_validate(data)
        if topology.version != SUPPORTED_TOPOLOGY_VERSION:
            raise ValueError(f"Unsupported topology version '{topology.version}'. Backend requires '{SUPPORTED_TOPOLOGY_VERSION}'.")

        device_ids = {device.id for device in topology.devices}
        for link in topology.links:
            if link.source not in device_ids:
                raise ValueError(f"Link '{link.id}' references a non-existent source '{link.source}'.")
            if link.target not in device_ids:
                raise ValueError(f"Link '{link.id}' references a non-existent target '{link.target}'.")

        return topology
    except (ValidationError, ValueError) as e:
        print(f"FATAL: Invalid data in '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)

@app.route('/api/topology', methods=['GET'])
def get_topology():
    if app_state["topology"]:
        return jsonify(app_state["topology"].model_dump())
    abort(500, description="Topology has not been initialized.")

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(app_state["events"])

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

    old_status = target_link.status
    target_link.status = payload.status
    add_event(f"SIMULATION: Status of link '{link_id}' changed from '{old_status}' to '{payload.status}'.")

    return jsonify(target_link.model_dump())

@app.route('/api/snapshot/save', methods=['POST'])
def save_snapshot():
    snapshot_name = request.json.get("name", "snapshot")
    snapshot_path = os.path.join("snapshots", f"{snapshot_name}.json")

    serializable_state = {
        "topology": app_state["topology"].model_dump() if app_state["topology"] else None,
        "events": app_state["events"]
    }

    os.makedirs("snapshots", exist_ok=True)
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(serializable_state, f, indent=2)

    add_event(f"Snapshot '{snapshot_name}' saved.")
    return jsonify({"message": f"Snapshot '{snapshot_name}' saved."})

@app.route('/api/snapshot/load', methods=['POST'])
def load_snapshot():
    snapshot_name = request.json.get("name", "snapshot")
    snapshot_path = os.path.join("snapshots", f"{snapshot_name}.json")
    if not os.path.exists(snapshot_path):
        return jsonify({"error": "Snapshot not found."}), 404

    with open(snapshot_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        app_state["topology"] = Topology.model_validate(data["topology"]) if data["topology"] else None
        app_state["events"] = data.get("events", [])
        add_event(f"Snapshot '{snapshot_name}' loaded.")
        return jsonify({"message": f"Snapshot '{snapshot_name}' loaded."})
    except ValidationError as e:
        return jsonify({"error": f"Snapshot load failed: {str(e)}"}), 400

if __name__ == '__main__':
    app_state["topology"] = load_and_validate_topology()
    add_event("SYSTEM: Backend started and topology loaded successfully.")
    print("Starting UNOC backend server (v3 with State & Simulation)...")
    print(f"Required topology version: {SUPPORTED_TOPOLOGY_VERSION}")
    print("Access the API at http://127.0.0.1:5000/api/topology")
    app.run(host='0.0.0.0', port=5000, debug=True)
