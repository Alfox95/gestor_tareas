"""Configuración común para pytest."""
import pytest

from app import create_app


@pytest.fixture
def client():
    """Cliente de prueba para la app Flask."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c
