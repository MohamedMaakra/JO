import sys
import os
import pytest
from flask import Flask

# Ajouter le dossier backend au sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# Importer l'application Flask et la base de données directement depuis app.py
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_hello(client):
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello World"}

def test_test_route(client):
    response = client.get('/test')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Test route is working"}
