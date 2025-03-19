import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db  # Εισάγετε το app και db από το αρχείο app.py

@pytest.fixture
def init_db():
    # Δημιουργία application context
    with app.app_context():
        db.create_all()  # Δημιουργία όλων των tables στη βάση δεδομένων
    yield db  # Επιστροφή της βάσης δεδομένων για χρήση στα tests
    with app.app_context():
        db.drop_all()  # Καθαρισμός των tables μετά τη δοκιμή

def test_create_resource(init_db):
    # Η δοκιμή για τη δημιουργία πόρων
    pass

def test_get_resources(init_db):
    # Η δοκιμή για να πάρετε πόρους
    pass

