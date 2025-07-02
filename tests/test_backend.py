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
from backend import build_graph

# --- Test Setup ---
BASE_TOPOLOGY = load_and_validate_topology()

# --- Pytest Fixtures ---
@pytest.fixture
def client():
    """Create a test client, resetting state and cleaning up snapshots."""
    app.config['TESTING'] = True

    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)
    for f in os.listdir(SNAPSHOT_DIR):
        os.remove(os.path.join(SNAPSHOT_DIR, f))

    app_state["topology"] = copy.deepcopy(BASE_TOPOLOGY)
    app_state["events"] = []
    app_state["undo_stack"] = []
    app_state["redo_stack"] = []
    app_state["graph"] = None  # reset optional

    with app.test_client() as client:
        yield client

    for f in os.listdir(SNAPSHOT_DIR):
        os.remove(os.path.join(SNAPSHOT_DIR, f))


# --- Test Cases ---

def test_get_topology_success(client):
    response = client.get('/api/topology')
    assert response.status_code == 200
    assert response.get_json()['version'] == "1.0.0"

def test_update_link_status_success(client):
    response = client.post('/api/links/link-01/status', json={"status": "down"})
    assert response.status_code == 200
    assert response.get_json()['status'] == 'down'

def test_update_link_status_not_found(client):
    response = client.post('/api/links/non-existent-link/status', json={"status": "down"})
    assert response.status_code == 404

def test_update_link_status_invalid_payload(client):
    response = client.post('/api/links/link-01/status', json={"status": "broken"})
    assert response.status_code == 422

def test_get_events_initial(client):
    response = client.get('/api/events')
    assert response.status_code == 200
    assert response.get_json() == []

def test_snapshot_cycle(client):
    snapshot_name = "test_run_1"

    client.post('/api/links/link-02/status', json={"status": "degraded"})
    save_response = client.post('/api/snapshot/save', json={"name": snapshot_name})
    assert save_response.status_code == 201
    assert os.path.exists(os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.json"))

    client.post('/api/links/link-02/status', json={"status": "up"})
    topo_response = client.get('/api/topology')
    assert next(l for l in topo_response.get_json()['links'] if l['id'] == 'link-02')['status'] == 'up'

    load_response = client.post('/api/snapshot/load', json={"name": snapshot_name})
    assert load_response.status_code == 200

    final_topo_response = client.get('/api/topology')
    restored_link = next(l for l in final_topo_response.get_json()['links'] if l['id'] == 'link-02')
    assert restored_link['status'] == 'degraded'

    events_response = client.get('/api/events')
    events = events_response.get_json()
    assert any(f"SYSTEM: Snapshot '{snapshot_name}' saved." in e for e in events)
    assert any(f"SYSTEM: Snapshot '{snapshot_name}' loaded successfully." in e for e in events)

def test_undo_redo_cycle(client):
    link_id = "link-01"
    original_status = "up"
    changed_status = "down"

    res1 = client.post(f'/api/links/{link_id}/status', json={"status": changed_status})
    assert res1.status_code == 200
    assert res1.get_json()['status'] == changed_status

    res_hist1 = client.get('/api/history/status')
    assert res_hist1.get_json() == {"can_undo": True, "can_redo": False}

    res_undo = client.post('/api/simulation/undo')
    assert res_undo.status_code == 200
    topo_after_undo = client.get('/api/topology').get_json()
    link_after_undo = next(l for l in topo_after_undo['links'] if l['id'] == link_id)
    assert link_after_undo['status'] == original_status

    res_hist2 = client.get('/api/history/status')
    assert res_hist2.get_json() == {"can_undo": False, "can_redo": True}

    res_redo = client.post('/api/simulation/redo')
    assert res_redo.status_code == 200
    topo_after_redo = client.get('/api/topology').get_json()
    link_after_redo = next(l for l in topo_after_redo['links'] if l['id'] == link_id)
    assert link_after_redo['status'] == changed_status

    res_hist3 = client.get('/api/history/status')
    assert res_hist3.get_json() == {"can_undo": True, "can_redo": False}

def test_fiber_cut_scenario(client):
    splitter_id = "SPLITTER-01"

    # ❗️ WICHTIG: Graph manuell initialisieren
    app_state["graph"] = build_graph(app_state["topology"])

    response = client.post('/api/simulation/fiber-cut', json={"node_id": splitter_id})
    assert response.status_code == 200

    topo_after_cut = client.get('/api/topology').get_json()
    ont1 = next(d for d in topo_after_cut['devices'] if d['id'] == 'ONT-KUNDE-123')
    ont2 = next(d for d in topo_after_cut['devices'] if d['id'] == 'ONT-KUNDE-124')
    link3 = next(l for l in topo_after_cut['links'] if l['id'] == 'link-03')

    assert ont1['status'] == 'offline'
    assert ont2['status'] == 'offline'
    assert link3['status'] == 'down'

    undo_resp = client.post('/api/simulation/undo')
    assert undo_resp.status_code == 200

    topo_after_undo = client.get('/api/topology').get_json()
    ont1_restored = next(d for d in topo_after_undo['devices'] if d['id'] == 'ONT-KUNDE-123')
    ont2_restored = next(d for d in topo_after_undo['devices'] if d['id'] == 'ONT-KUNDE-124')
    link3_restored = next(l for l in topo_after_undo['links'] if l['id'] == 'link-03')

    assert ont1_restored['status'] == 'online'    # original state
    assert ont2_restored['status'] == 'offline'   # original state
    assert link3_restored['status'] == 'up'       # original state

def test_get_topology_stats(client):
    """
    Tests the statistics calculation endpoint.
    """
    # 1. Get initial stats
    response1 = client.get('/api/topology/stats')
    assert response1.status_code == 200
    stats1 = response1.get_json()
    assert stats1['devices_online'] == 4 # In topology.yml ist einer offline
    assert stats1['links_up'] == 3       # Einer ist down
    assert stats1['alarms'] == 2         # 1 offline device + 1 down link

    # 2. Change a link status and check stats again
    client.post('/api/links/link-01/status', json={"status": "down"})
    
    response2 = client.get('/api/topology/stats')
    stats2 = response2.get_json()
    assert stats2['links_up'] == 2
    assert stats2['alarms'] == 3