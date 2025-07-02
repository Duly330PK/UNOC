import pytest
import copy
from backend import app, load_and_validate_topology, app_state

BASE_TOPOLOGY = load_and_validate_topology()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app_state["topology"] = copy.deepcopy(BASE_TOPOLOGY)
    app_state["events"] = []
    with app.test_client() as client:
        yield client

def test_get_topology_success(client):
    response = client.get('/api/topology')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['version'] == "1.0.0"
    assert json_data['devices'][0]['id'] == "OLT-MST-01"

def test_update_link_status_success(client):
    link_to_change = "link-01"
    new_status = "down"
    payload = {"status": new_status}

    response = client.post(f'/api/links/{link_to_change}/status', json=payload)
    assert response.status_code == 200
    assert response.get_json()['status'] == new_status

    response = client.get('/api/topology')
    topology_data = response.get_json()
    assert next(link for link in topology_data['links'] if link['id'] == link_to_change)['status'] == new_status

    response = client.get('/api/events')
    events_data = response.get_json()
    assert len(events_data) == 1
    assert f"Status of link '{link_to_change}' changed" in events_data[0]

def test_update_link_status_not_found(client):
    response = client.post('/api/links/unknown/status', json={"status": "down"})
    assert response.status_code == 404

def test_update_link_status_invalid_payload(client):
    response = client.post('/api/links/link-01/status', json={"status": "broken"})
    assert response.status_code == 422

def test_get_events_initial(client):
    response = client.get('/api/events')
    assert response.status_code == 200
    assert response.get_json() == []


def test_snapshot_cycle(client):
    # Save snapshot
    response = client.post('/api/snapshot/save', json={'name': 'pytest'})
    assert response.status_code == 200
    # Load snapshot
    response = client.post('/api/snapshot/load', json={'name': 'pytest'})
    assert response.status_code == 200
