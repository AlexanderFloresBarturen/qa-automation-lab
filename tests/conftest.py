from fastapi.testclient import TestClient   # Permite probars APIs sin levantar Uvicorn.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app.dependencies import get_db

import pytest
import uuid

#region Configuración de DB de prueba

TEST_DATABASE_URL = "sqlite:///./test.db"

# Crea conexión SQLite
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Crea sesiones para consultas
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

# Esto crea y cierra sesiones automáticamente por cada request
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()    # Evita que el override quede activo para otros contextos

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

#endregion

"""
Fixture sirve para preparar el entorno y los datos necesarios antes de ejecutar una prueba y limpiarlos después.
Permite evitar código repetitivo y estructurar los tests de forma modular
"""

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
    db = TestingSessionLocal()
    yield db
    db.close()