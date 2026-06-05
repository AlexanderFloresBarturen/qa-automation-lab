from fastapi.testclient import TestClient   # Permite probars APIs sin levantar Uvicorn.

from app.main import app

import pytest

"""
Fixture sirve para preparar el entorno y los datos necesarios antes de ejecutar una prueba y limpiarlos después.
Permite evitar código repetitivo y estructurar los tests de forma modular
"""
@pytest.fixture
def client():
    return TestClient(app)