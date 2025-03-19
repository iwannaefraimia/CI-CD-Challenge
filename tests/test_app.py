import pytest
from app import app, db, Resource

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def init_db():
    db.create_all()
    yield db
    db.drop_all()

def test_create_resource(client, init_db):
    response = client.post('/resources', json={'name': 'Oxygen', 'quantity': 100})
    assert response.status_code == 201
    assert b'Resource added!' in response.data

def test_get_resources(client, init_db):
    response = client.get('/resources')
    assert response.status_code == 200
    assert b'Oxygen' in response.data
