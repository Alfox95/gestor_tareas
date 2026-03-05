"""Configuración común para pytest."""
import pytest

from app import create_app
import router


@pytest.fixture
def client(tmp_path):
    """Cliente de prueba para la app Flask."""
    router.reset_state()
    app = create_app(
        {
            "TESTING": True,
            "DATA_FILE": tmp_path / "data.json",
            "SECRET_KEY": "test",
        }
    )
    with app.test_client() as c:
        yield c
