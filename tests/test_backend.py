#
# UNOC - tests/test_backend.py
#
# Unit tests for the stateful backend application with snapshots and undo/redo.
#

import pytest
import copy
import os
import json
from backend import app, app_state, load_and_validate_topology, SNAPSHOT_DIR

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
    app_state["topology"] = copy.deepcopy(BASE_TOPOLOGY)
    app_state["events"] = []
    app_state["undo_stack"] = []
    app_state["redo_stack"] = []

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

    # 6. Verify event log contains snapshot messages (JETZT korrekt eingerückt)
    events_response = client.get('/api/events')
    events = events_response.get_json()

    print("\n\nDEBUG-EVENTS:\n", "\n".join(events), "\n\n")  # optional

    assert any(f"SYSTEM: Snapshot '{snapshot_name}' saved." in e for e in events)
    assert any(f"SYSTEM: Snapshot '{snapshot_name}' loaded successfully." in e for e in events)
    
def test_undo_redo_cycle(client):
    """
    Tests the full undo/redo cycle for a simulation action.
    """
    link_id = "link-01"
    original_status = "up"
    changed_status = "down"

    # 1. Action: Change status from 'up' to 'down'
    res1 = client.post(f'/api/links/{link_id}/status', json={"status": changed_status})
    assert res1.status_code == 200
    assert res1.get_json()['status'] == changed_status

    # 2. Verify history status
    res_hist1 = client.get('/api/history/status')
    assert res_hist1.get_json() == {"can_undo": True, "can_redo": False}

    # 3. Undo: Change status back to 'up'
    res_undo = client.post('/api/simulation/undo')
    assert res_undo.status_code == 200

    topo_after_undo = client.get('/api/topology').get_json()
    link_after_undo = next(l for l in topo_after_undo['links'] if l['id'] == link_id)
    assert link_after_undo['status'] == original_status

    # 4. Verify history status after undo
    res_hist2 = client.get('/api/history/status')
    assert res_hist2.get_json() == {"can_undo": False, "can_redo": True}

    # 5. Redo: Change status back to 'down'
    res_redo = client.post('/api/simulation/redo')
    assert res_redo.status_code == 200

    topo_after_redo = client.get('/api/topology').get_json()
    link_after_redo = next(l for l in topo_after_redo['links'] if l['id'] == link_id)
    assert link_after_redo['status'] == changed_status

    # 6. Verify history status after redo
    res_hist3 = client.get('/api/history/status')
    assert res_hist3.get_json() == {"can_undo": True, "can_redo": False}
