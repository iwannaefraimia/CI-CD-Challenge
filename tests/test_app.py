import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db  
@pytest.fixture
def init_db():
    with app.app_context():
        db.create_all()  
    yield db  
    with app.app_context():
        db.drop_all()  

def test_create_resource(init_db):
    pass

def test_get_resources(init_db):
    pass

