from copy import deepcopy
import pytest
from backend import app, routes

@pytest.fixture
def isolated_client():
    saved = deepcopy(routes.data)
    yield app.test_client()
    routes.data[:] = saved

@pytest.mark.parametrize('payload', [{}, [], {'id': True}, {'id': '2'}, {'id': -1}])
def test_invalid_picture_is_rejected(isolated_client, payload):
    before = len(routes.data)
    assert isolated_client.post('/picture', json=payload).status_code == 400
    assert len(routes.data) == before


def test_empty_collection_is_success(isolated_client):
    routes.data.clear()
    assert isolated_client.get('/count').json == {'length': 0}
    assert isolated_client.get('/picture').json == []


def test_identity_cannot_change(isolated_client):
    payload = deepcopy(routes.data[0])
    original_id = payload['id']
    payload['id'] = 98765
    assert isolated_client.put(f'/picture/{original_id}', json=payload).status_code == 400
    assert isolated_client.get(f'/picture/{original_id}').status_code == 200
