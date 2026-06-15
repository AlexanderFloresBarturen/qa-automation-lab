from fastapi.testclient import TestClient   # Permite probars APIs sin levantar Uvicorn.

from app.main import app
from app.database import SessionLocal

import pytest
import uuid
import random

"""
Fixture sirve para preparar el entorno y los datos necesarios antes de ejecutar una prueba y limpiarlos después.
Permite evitar código repetitivo y estructurar los tests de forma modular
"""
@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def valid_user_payload():
    return{
        "name": "Alex",
        "email": f"{uuid.uuid4()}@gmail.com",
        "age": 25
    }

@pytest.fixture
def valid_update_payload():
    return{
        "name": "Pepe",
        "email": f"{uuid.uuid4()}@hotmail.com",
        "age": 42
    }

@pytest.fixture
def user_payload():
    def _user_payload(
            name="Pepe",
            age=49
    ):
        return {
            "name": name,
            "email": f"{uuid.uuid4()}@gmail.com",
            "age": age
        }
    
    return _user_payload

@pytest.fixture
def patch_user(client):
    # El '*' obliga que todo lo que está a la derecha se pase con nombre
    def _patch_user(id, *, name = False, email = False, age = False):
        patch_payload = {}
        if name:
            patch_payload["name"] = "Diego Armando"
        if email:
            patch_payload["email"] = f"{uuid.uuid4()}@yahoo.com"
        if age:
            patch_payload["age"] = 36
        
        return client.patch(f"/users/{id}", json=patch_payload)
    
    return _patch_user # <-- Importante no olvidar esta línea

@pytest.fixture
def created_user(client, valid_user_payload):
    response = client.post("/users", json=valid_user_payload)

    assert response.status_code == 201

    return response.json()

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()