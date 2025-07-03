#
# UNOC - tests/test_backend.py
#
# Unit tests for the stateful backend application with snapshots and undo/redo (dynamische Werte!).
#

import pytest
import copy
import os
from backend import app, app_state, load_and_validate_topology, SNAPSHOT_DIR, initialize_rings, build_graph

# --- Test Setup ---
BASE_TOPOLOGY = load_and_validate_topology()

# --- Pytest Fixtures ---
@pytest.fixture
def client():
    """Create a test client, resetting state and cleaning up snapshots."""
    app.config['TESTING'] = True

    # Cleanup snapshot directory before tests
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)
    for f in os.listdir(SNAPSHOT_DIR):
        os.remove(os.path.join(SNAPSHOT_DIR, f))

    # Reset app state for each test
    app_state["topology"] = copy.deepcopy(BASE_TOPOLOGY)
    app_state["graph"] = build_graph(app_state["topology"])
    app_state["events"] = []      # <- Fix: Events leeren VOR initialize_rings!
    app_state["undo_stack"] = []
    app_state["redo_stack"] = []
    initialize_rings()            # <- Jetzt erzeugt initialize_rings() Events!

    with app.test_client() as client:
        yield client

    # Cleanup snapshot directory after tests
    if os.path.exists(SNAPSHOT_DIR):
        for f in os.listdir(SNAPSHOT_DIR):
            os.remove(os.path.join(SNAPSHOT_DIR, f))

# --- Test Cases ---

def test_get_topology_success(client):
    response = client.get('/api/topology')
    assert response.status_code == 200
    assert "version" in response.get_json()

def test_update_link_status_success(client):
    topo = client.get('/api/topology').get_json()
    up_link = next((l['id'] for l in topo['links'] if l['status'] == 'up'), None)
    assert up_link is not None
    response = client.post(f'/api/links/{up_link}/status', json={"status": "down"})
    assert response.status_code == 200
    assert response.get_json()['status'] == 'down'

def test_update_link_status_not_found(client):
    response = client.post('/api/links/non-existent-link/status', json={"status": "down"})
    assert response.status_code == 404

def test_update_link_status_invalid_payload(client):
    topo = client.get('/api/topology').get_json()
    up_link = next((l['id'] for l in topo['links'] if l['status'] == 'up'), None)
    assert up_link is not None
    response = client.post(f'/api/links/{up_link}/status', json={"status": "broken"})
    assert response.status_code == 422

def test_get_events_initial(client):
    response = client.get('/api/events')
    assert response.status_code == 200
    events = response.get_json()
    assert isinstance(events, list)
    assert any("set to BLOCKING" in e and "ERPS" in e for e in events) or \
           any("rings initialized" in e for e in events)

def test_snapshot_cycle(client):
    snapshot_name = "test_run_1"

    topo = client.get('/api/topology').get_json()
    target_link = next((l['id'] for l in topo['links'] if l['status'] == 'up'), None)
    assert target_link is not None

    client.post(f'/api/links/{target_link}/status', json={"status": "degraded"})
    save_response = client.post('/api/snapshot/save', json={"name": snapshot_name})
    assert save_response.status_code == 201
    assert os.path.exists(os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.json"))

    client.post(f'/api/links/{target_link}/status', json={"status": "up"})
    topo_response = client.get('/api/topology')
    assert next(l for l in topo_response.get_json()['links'] if l['id'] == target_link)['status'] == 'up'

    load_response = client.post('/api/snapshot/load', json={"name": snapshot_name})
    assert load_response.status_code == 200

    final_topo_response = client.get('/api/topology')
    restored_link = next(l for l in final_topo_response.get_json()['links'] if l['id'] == target_link)
    assert restored_link['status'] == 'degraded'

    events_response = client.get('/api/events')
    events = events_response.get_json()
    assert any(f"SYSTEM: Snapshot '{snapshot_name}' saved." in e for e in events)
    assert any(f"SYSTEM: Snapshot '{snapshot_name}' loaded successfully." in e for e in events)

def test_undo_redo_cycle(client):
    topo = client.get('/api/topology').get_json()
    link = next((l for l in topo['links'] if l['status'] == 'up'), None)
    assert link is not None
    link_id = link['id']
    original_status = link['status']
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

    response = client.post('/api/simulation/fiber-cut', json={"node_id": splitter_id})
    assert response.status_code == 200

    topo_after_cut = client.get('/api/topology').get_json()
    onts = [d for d in topo_after_cut['devices'] if d['id'].startswith('ONT')]
    assert onts, "Keine ONTs gefunden"
    for ont in onts:
        if any(l['source'] == splitter_id and l['target'] == ont['id'] for l in topo_after_cut['links']):
            assert ont['status'] == 'offline'

    affected_links = [l for l in topo_after_cut['links'] if l['source'] == splitter_id or l['target'] == splitter_id]
    assert any(l['status'] == 'down' for l in affected_links)

    undo_resp = client.post('/api/simulation/undo')
    assert undo_resp.status_code == 200

    topo_after_undo = client.get('/api/topology').get_json()
    original_onts = [d for d in BASE_TOPOLOGY.devices if d.id in [o['id'] for o in onts]]
    for original_ont in original_onts:
         restored_ont = next(ont for ont in topo_after_undo['devices'] if ont['id'] == original_ont.id)
         assert restored_ont['status'] == original_ont.status

    original_affected_links = [l for l in BASE_TOPOLOGY.links if l.id in [al['id'] for al in affected_links]]
    for original_link in original_affected_links:
        restored_link = next(link for link in topo_after_undo['links'] if link['id'] == original_link.id)
        assert restored_link['status'] == original_link.status

def test_get_topology_stats(client):
    """
    Tests the statistics calculation endpoint (dynamisch).
    """
    response1 = client.get('/api/topology/stats')
    assert response1.status_code == 200
    stats1 = response1.get_json()

    assert stats1['devices_online'] <= stats1['devices_total']
    assert stats1['links_up'] <= stats1['links_total']

    response_full = client.get('/api/topology')
    topo = response_full.get_json()
    expected_device_alarms = stats1['devices_total'] - stats1['devices_online']
    expected_link_alarms = sum(1 for l in topo['links'] if l['status'] not in ['up', 'blocking'])
    assert stats1['alarms'] == expected_device_alarms + expected_link_alarms

    up_link = next((l['id'] for l in topo['links'] if l['status'] == 'up'), None)
    assert up_link, "Es muss mindestens einen aktiven Link geben"
    
    client.post(f'/api/links/{up_link}/status', json={"status": "down"})
    response2 = client.get('/api/topology/stats')
    stats2 = response2.get_json()

    assert stats2['links_up'] == stats1['links_up'] - 1
    response_full2 = client.get('/api/topology')
    topo2 = response_full2.get_json()
    expected_device_alarms2 = stats2['devices_total'] - stats2['devices_online']
    expected_link_alarms2 = sum(1 for l in topo2['links'] if l['status'] not in ['up', 'blocking'])
    assert stats2['alarms'] == expected_device_alarms2 + expected_link_alarms2

def test_erps_failover_scenario(client):
    """
    Tests the ERPS failover logic (dynamisch!).
    """
    topo1 = client.get('/api/topology').get_json()
    assert 'rings' in topo1 and len(topo1['rings']) > 0, "Kein Ring in der Topologie definiert."
    ring = topo1['rings'][0]
    rpl_link_id = ring['rpl_link_id']
    
    ring_links_ids = [l['id'] for l in topo1['links']
                  if l['source'] in ring['nodes'] and l['target'] in ring['nodes'] and l['id'] != rpl_link_id]
    
    link_to_break = None
    for link_id in ring_links_ids:
        link_details = next((l for l in topo1['links'] if l['id'] == link_id), None)
        if link_details and link_details['status'] == 'up':
            link_to_break = link_id
            break

    assert link_to_break, "Kein 'up'-Link im Ring gefunden, um einen Failover zu testen."
    
    assert next(l for l in topo1['links'] if l['id'] == rpl_link_id)['status'] == 'blocking'

    client.post(f'/api/links/{link_to_break}/status', json={"status": "down"})

    topo2 = client.get('/api/topology').get_json()
    assert next(l for l in topo2['links'] if l['id'] == link_to_break)['status'] == 'down'
    assert next(l for l in topo2['links'] if l['id'] == rpl_link_id)['status'] == 'up'

    client.post('/api/simulation/undo')

    topo3 = client.get('/api/topology').get_json()
    assert next(l for l in topo3['links'] if l['id'] == link_to_break)['status'] == 'up'
    assert next(l for l in topo3['links'] if l['id'] == rpl_link_id)['status'] == 'blocking'

def test_optical_power_calculation(client):
    """
    Tests the optical power calculation for a specific ONT.
    """
    ont_id = "ONT-KUNDE-123"
    
    tx_power = 4.0
    link2_loss = 2.5 * 0.35 # FIBER_LOSS_PER_KM
    link3_loss = 0.8 * 0.35
    splitter_loss = 10.5
    expected_power = tx_power - link2_loss - link3_loss - splitter_loss
    
    response = client.get(f'/api/devices/{ont_id}/signal')
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['status'] == 'GOOD'
    assert data['power_dbm'] == pytest.approx(expected_power, abs=0.01)

def test_trace_path(client):
    """
    Tests the path tracing functionality before and after a failover.
    """
    # 1. Trace path im Normalzustand
    payload1 = {"start_node": "AGG-MST-01", "end_node": "AGG-RHE-01"}
    response1 = client.post('/api/simulation/trace-path', json=payload1)
    assert response1.status_code == 200
    path1 = response1.get_json()
    assert path1['nodes'] == ["AGG-MST-01", "AGG-COE-01", "AGG-RHE-01"]
    assert "link-mst-coe" in path1['links']
    assert "link-coe-rhe" in path1['links']

    # 2. Simuliere einen Link-Ausfall im Ring
    client.post('/api/links/link-mst-coe/status', json={"status": "down"})

    # 3. Trace den Pfad erneut, er muss jetzt über den RPL gehen
    response2 = client.post('/api/simulation/trace-path', json=payload1)
    assert response2.status_code == 200
    path2 = response2.get_json()
    # Der Pfad ist jetzt der umgekehrte Weg über den vormals blockierten Link
    assert path2['nodes'] == ["AGG-MST-01", "AGG-RHE-01"]
    assert "link-rhe-mst" in path2['links']