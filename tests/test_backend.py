import pytest
import yaml
from backend import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_topology_success(client):
    response = client.get('/api/topology')
    assert response.status_code == 200
    data = response.get_json()
    assert "devices" in data and "links" in data
    assert data["version"] == "1.0.0"
