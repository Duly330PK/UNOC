#
# UNOC - tests/test_backend.py
#
# Unit tests for the stateful backend application with snapshots.
#

import pytest
import copy
import os
import json
from backend import app, load_and_validate_topology, SNAPSHOT_DIR

# --- Test Setup ---
BASE_TOPOLOGY = load_and_validate_topology()

# --- Pytest Fixtures ---
@pytest.fixture
def client():
    """Create a test client, resetting state and cleaning up snapshots."""
    app.config['TESTING'] = True
    # Ensure snapshot dir exists and is empty before a test
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)
    for f in os.listdir(SNAPSHOT_DIR):
        os.remove(os.path.join(SNAPSHOT_DIR, f))

    # Reset state before each test
    app.app_state["topology"] = copy.deepcopy(BASE_TOPOLOGY)
    app.app_state["events"] = []
    
    with app.test_client() as client:
        yield client
    
    # Cleanup after test
    for f in os.listdir(SNAPSHOT_DIR):
        os.remove(os.path.join(SNAPSHOT_DIR, f))


# --- Test Cases ---

def test_get_topology_success(client):
    """Tests if the initial topology is returned correctly."""
    response = client.get('/api/topology')
    assert response.status_code == 200
    assert response.get_json()['version'] == "1.0.0"

def test_update_link_status_success(client):
    """Tests if a link's status can be successfully updated."""
    response = client.post('/api/links/link-01/status', json={"status": "down"})
    assert response.status_code == 200
    assert response.get_json()['status'] == 'down'

def test_update_link_status_not_found(client):
    """Tests updating a non-existent link."""
    response = client.post('/api/links/non-existent-link/status', json={"status": "down"})
    assert response.status_code == 404

def test_update_link_status_invalid_payload(client):
    """Tests updating a link with invalid data."""
    response = client.post('/api/links/link-01/status', json={"status": "broken"})
    assert response.status_code == 422

def test_get_events_initial(client):
    """Tests if the event log is initially empty."""
    response = client.get('/api/events')
    assert response.status_code == 200
    assert response.get_json() == []

def test_snapshot_cycle(client):
    """
    Tests the full save/change/load cycle of a snapshot.
    """
    snapshot_name = "test_run_1"

    # 1. Change the state
    client.post('/api/links/link-02/status', json={"status": "degraded"})

    # 2. Save the changed state
    save_response = client.post('/api/snapshot/save', json={"name": snapshot_name})
    assert save_response.status_code == 201
    assert os.path.exists(os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.json"))

    # 3. Change the state again to something different
    client.post('/api/links/link-02/status', json={"status": "up"})
    topo_response = client.get('/api/topology')
    assert next(l for l in topo_response.get_json()['links'] if l['id'] == 'link-02')['status'] == 'up'

    # 4. Load the original snapshot
    load_response = client.post('/api/snapshot/load', json={"name": snapshot_name})
    assert load_response.status_code == 200

    # 5. Verify that the state has been restored to the snapshot's state
    final_topo_response = client.get('/api/topology')
    restored_link = next(l for l in final_topo_response.get_json()['links'] if l['id'] == 'link-02')
    assert restored_link['status'] == 'degraded'

    # 6. Verify event log contains snapshot messages
    events_response = client.get('/api/events')
    events = events_response.get_json()
    assert "Snapshot 'test_run_1' loaded" in events[0]
    assert "Snapshot 'test_run_1' saved" in events[2]