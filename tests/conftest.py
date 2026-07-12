import uuid
from typing import Any

import pytest
from fastapi.testclient import TestClient  # Permite probars APIs sin levantar Uvicorn.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.config import Config
from app.core.settings import DatabaseEnvironment, settings
from app.database.dependencies import get_db
from app.main import app
from app.models.user_model import UserModel
from tests.database import ensure_test_database_exists

# region Configuración de DB de testing


# Hook de inicio
def pytest_sessionstart(session):
    settings.use_test_database()

    assert settings.CURRENT_DATABASE == DatabaseEnvironment.TEST

    ensure_test_database_exists()

    alembic_cfg = Config("alembic.ini")

    command.upgrade(alembic_cfg, "head")

    print(f"Running test against: {settings.CURRENT_DATABASE.value} database")


# Hook de finalización
def pytest_sessionfinish(session, exitstatus):
    settings.use_development_database()

    assert settings.CURRENT_DATABASE == DatabaseEnvironment.DEVELOPMENT

    print(f"Restoring to: {settings.CURRENT_DATABASE.value} database")


# Crea conexión PostgreSQL para testing
test_engine = create_engine(settings.TEST_DATABASE_URL)

# Crea sesiones para consultas
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def db():
    # Abre conexión física con PostgreSQL
    connection = test_engine.connect()

    # Abre una transacción sobre la conexión
    transaction = connection.begin()

    """
    Abre una sesión para los endpoints, la cual se asocia a la transacción
    existente y se ejecuta dentro de esta
    """
    db = TestingSessionLocal(bind=connection)

    yield db

    # Cierra la sesión
    db.close()

    # Revierte los cambios dentro de la transacción
    transaction.rollback()

    # Cierra la conexión
    connection.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()  # Evita que el override quede activo para otros contextos


# endregion

"""
Fixture sirve para preparar el entorno y los datos necesarios antes de ejecutar una prueba y limpiarlos después.
Permite evitar código repetitivo y estructurar los tests de forma modular
"""


@pytest.fixture
def valid_user_payload():
    return {"name": "Alex", "email": f"{uuid.uuid4()}@gmail.com", "age": 25, "password": "Password123!"}


@pytest.fixture
def valid_update_payload():
    return {"name": "Pepe", "email": f"{uuid.uuid4()}@hotmail.com", "age": 42, "password": "Password123!"}


@pytest.fixture
def user_payload():
    def _user_payload(name="Pepe", age=49, password="Password123!"):
        return {"name": name, "email": f"{uuid.uuid4()}@gmail.com", "age": age, "password": password}

    return _user_payload


@pytest.fixture
def patch_user(client):
    # El '*' obliga que todo lo que está a la derecha se pase con nombre
    def _patch_user(*, name=False, email=False, age=False, is_admin=False, user_id=0, headers=""):
        patch_payload: dict[str, Any] = {}
        if name:
            patch_payload["name"] = "Diego Armando"
        if email:
            patch_payload["email"] = f"{uuid.uuid4()}@yahoo.com"
        if age:
            patch_payload["age"] = 36

        if is_admin:
            return client.patch(f"/users/{user_id}", json=patch_payload, headers=headers)
        else:
            return client.patch("/profile", json=patch_payload, headers=headers)

    return _patch_user  # <-- Importante no olvidar esta línea


@pytest.fixture
def created_user(client, valid_user_payload):
    response = client.post("/auth/register", json=valid_user_payload)

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def loged_user(client, valid_user_payload):
    created_response = client.post("/auth/register", json=valid_user_payload)
    created_body = created_response.json()

    payload = {"username": valid_user_payload["email"], "password": valid_user_payload["password"]}
    login_response = client.post("/auth/login", data=payload)
    login_body = login_response.json()

    assert created_response.status_code == 201
    assert login_response.status_code == 200

    created_body["token"] = login_body["access_token"]

    return created_body


@pytest.fixture
def get_token(client):
    def _get_token(*, username="", password=""):
        payload = {"username": username, "password": password}
        login_response = client.post("/auth/login", data=payload)
        login_body = login_response.json()

        assert login_response.status_code == 200

        return login_body["access_token"]

    return _get_token


@pytest.fixture
def user_reset_password_payload(client, created_user):
    def _user_reset_password_payload(*, password="NewPassword123!"):
        fp_response = client.post("/auth/forgot-password", json={"email": created_user["email"]})
        fp_body = fp_response.json()

        assert fp_response.status_code == 200

        return {"token": fp_body["token"], "new_password": password}

    return _user_reset_password_payload


@pytest.fixture
def admin_user(db, client, valid_user_payload):
    created_response = client.post("/auth/register", json=valid_user_payload)
    created_body = created_response.json()

    user = db.query(UserModel).filter(UserModel.id == created_body["id"]).first()

    user.role_id = 1

    db.commit()

    payload = {"username": valid_user_payload["email"], "password": valid_user_payload["password"]}
    login_response = client.post("/auth/login", data=payload)
    login_body = login_response.json()

    assert created_response.status_code == 201
    assert login_response.status_code == 200

    created_body["token"] = login_body["access_token"]

    return created_body
