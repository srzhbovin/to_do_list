import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_all_targets(client):
    response = client.get('/todo')
    print(response)
    print(response.json())
    assert response.status_code == 200


def test_add_target(client):
    data = {
        "title": 'do it',
        'description': 'about it'
    }
    response = client.post('/todo/new_target', json=data)
    assert response.status_code == 200


def test_update_target(client):
    data = {
        "new_title": 'do_something_else',
        "new_description": 'something more about it'
    }
    title = 'ddd'
    response = client.put(f'/todo/update/{title}', json=data)
    assert response.status_code == 200


def test_delete_tatget(client):
    title = {'title': 'do it'}
    response = client.delete(f'/todo/delete/{title}')
    assert response.status_code == 200

