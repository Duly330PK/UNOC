import yaml
from flask import Flask, jsonify, abort
from flask_cors import CORS
from pydantic import ValidationError

from schemas import Topology, SUPPORTED_TOPOLOGY_VERSION

app = Flask(__name__)
CORS(app)

def load_and_validate_topology(filepath="topology.yml"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        raise

    try:
        topology = Topology.model_validate(data)
    except ValidationError as e:
        raise

    if topology.version != SUPPORTED_TOPOLOGY_VERSION:
        raise ValidationError.from_exception_data(
            title="Unsupported Topology Version",
            line_errors=[{
                "loc": ("version",),
                "msg": f"Version '{topology.version}' is not supported.",
                "type": "value_error"
            }]
        )

    device_ids = {device.id for device in topology.devices}
    for link in topology.links:
        if link.source not in device_ids:
            raise ValueError(f"Link '{link.id}' source '{link.source}' unknown.")
        if link.target not in device_ids:
            raise ValueError(f"Link '{link.id}' target '{link.target}' unknown.")

    return topology

@app.route('/api/topology', methods=['GET'])
def get_topology():
    try:
        topology_model = load_and_validate_topology()
        return jsonify(topology_model.model_dump())
    except FileNotFoundError:
        abort(404, description="topology.yml not found.")
    except ValidationError as e:
        abort(422, description=e.errors())
    except ValueError as e:
        abort(422, description=str(e))

if __name__ == '__main__':
    print("UNOC Backend gestartet.")
    print("API verfügbar unter http://127.0.0.1:5000/api/topology")
    app.run(host='0.0.0.0', port=5000, debug=True)
