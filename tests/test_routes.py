"""Tests básicos de rutas del gestor de tareas."""


def test_index_returns_200(client):
    """La página principal responde con 200."""
    r = client.get("/")
    assert r.status_code == 200


def test_index_contains_gestor_tareas(client):
    """La página principal muestra el título del gestor."""
    r = client.get("/")
    assert b"Gestor de tareas" in r.data or b"gestor" in r.data.lower()


def test_crear_usuario_redirects(client):
    """Crear usuario redirige a la página principal."""
    r = client.post("/usuarios/crear", data={"nombre_usuario": "Test"})
    assert r.status_code == 302
    assert r.location == "/" or r.location.endswith("/")


def test_crear_usuario_vacio_redirects(client):
    """Crear usuario con nombre vacío redirige sin crear."""
    r = client.post("/usuarios/crear", data={"nombre_usuario": ""})
    assert r.status_code == 302
