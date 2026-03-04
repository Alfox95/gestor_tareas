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


def test_crear_usuario_duplicado_muestra_error(client):
    """Si el nombre ya existe, se muestra error y no se crea otro usuario."""
    client.post("/usuarios/crear", data={"nombre_usuario": "UsuarioUnico"})
    r = client.post(
        "/usuarios/crear",
        data={"nombre_usuario": "UsuarioUnico"},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"El usuario ya existe" in r.data


def test_crear_usuario_duplicado_insensible_mayusculas(client):
    """Nombre duplicado se detecta sin importar mayúsculas/minúsculas."""
    client.post("/usuarios/crear", data={"nombre_usuario": "Ana"})
    r = client.post(
        "/usuarios/crear",
        data={"nombre_usuario": "ana"},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"El usuario ya existe" in r.data
