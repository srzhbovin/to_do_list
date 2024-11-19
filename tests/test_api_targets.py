import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_get_all_targets(client):
    response = await client.get('/todo')
    print(response)
    print(response.json())
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_target(client):
    data = {
        "title": 'do it',
        'description': 'about it'
    }
    response = await client.post('/todo/new_target', json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_target(client):
    data = {
        "new_title": 'do_something_else',
        "new_description": 'something more about it'
    }
    title = 'ddd'
    response = await client.put(f'/todo/update/{title}', json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_target(client):
    title = 'do it'
    response = await client.delete(f'/todo/delete/{title}')
    assert response.status_code == 200
