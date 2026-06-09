from fastapi.testclient import TestClient   # Permite probars APIs sin levantar Uvicorn.

from app.main import app

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
def created_user(client, valid_user_payload):
    response = client.post("/users", json=valid_user_payload)

    assert response.status_code == 201

    return response.json()