## Gestor de tareas con Flask

Aplicación web de ejemplo para gestionar tareas, pensada como proyecto de aprendizaje con Flask.  
Incluye:

- Modelo `Tarea` con prioridad, fechas y relación con usuarios.
- Usuarios simples (solo nombre, sin login ni auth compleja).
- Orden inteligente de tareas por urgencia y prioridad.
- Persistencia en archivo JSON.
- Tests básicos con `pytest`.

---

### Funcionalidades principales

- **Usuarios**
  - Crear usuarios con nombre único (no permite duplicados, sin distinguir mayúsculas/minúsculas).
  - Listado de usuarios en la interfaz.

- **Tareas**
  - Crear tareas con:
    - Descripción.
    - Usuario creador (obligatorio).
    - Prioridad (1–5, de “Muy baja” a “Urgente”).
    - Fecha máxima opcional.
  - Orden de tareas pendientes:
    - Primero las que tienen **≤ 2 días restantes**.
    - Dentro de eso, por **prioridad** (5 → 1).
    - Luego por **días restantes** (menos días primero).
    - Si no se define fecha máxima, se usan **60 días por defecto** para el orden y se muestra como tal.
  - Cambio de prioridad desde la UI:
    - Botón para **subir** prioridad.
    - Botón para **bajar** prioridad.
  - Completar tareas:
    - Es obligatorio seleccionar el **usuario que completa**.
    - Se guarda la fecha de realización y el usuario completador.
  - Reabrir tareas:
    - Desde el listado de completadas, se puede enviar una tarea de vuelta a pendientes.
    - Se conserva el historial (fecha de realización y completador).

- **Persistencia**
  - Estado (usuarios, tareas, contadores de IDs) guardado en `data.json` usando JSON.
  - Carga automática del estado al iniciar la aplicación.
  - Guardado automático tras cada cambio de datos.
  - `data.json` está ignorado en Git.

- **Interfaz**
  - Vista única (`index.html`) con:
    - Sección de usuarios.
    - Formulario de nueva tarea.
    - Lista de tareas pendientes.
    - Lista de tareas completadas.
  - Estilos CSS simples pero cuidados (`static/styles.css`), con:
    - Badges de prioridad por color (de verde claro a rojo).
    - Badge de días restantes con escala de azul claro a rojo.
    - Etiquetas de fechas y usuarios.

---

### Requisitos

- **Python** 3.10 o superior.
- `pip` instalado.

---

### Instalación

Desde la carpeta raíz del proyecto:

```bash
pip install -r requirements.txt
```

---

### Ejecutar la aplicación

Desde la carpeta del proyecto:

```bash
python app.py
```

Luego abre en el navegador:

```text
http://127.0.0.1:5000/
```

Algunas cosas para probar:

- Crear uno o varios usuarios.
- Crear tareas con distintas prioridades y fechas límite.
- Ver cómo cambia el orden según los días restantes y la prioridad.
- Completar tareas con distintos usuarios.
- Reabrir tareas desde la sección de completadas.
- Reiniciar la app y comprobar que las tareas y usuarios se mantienen (gracias a `data.json`).

---

### Estructura del proyecto (resumen)

- **`app.py`**: punto de entrada de la aplicación Flask, configuración principal e inicialización de estado.
- **`router.py`**: rutas principales (usuarios, tareas, prioridad, reabrir), lógica de orden y conexión con la capa de persistencia.
- **`models.py`**:
  - `Usuario`: id, nombre.
  - `Tarea`: id, descripción, prioridad, fechas, tipo de tarea opcional, completo, creador, completador y algunos métodos de utilidad.
- **`storage.py`**: lectura/escritura del estado en archivo JSON (`data.json`), conversión de fechas y reconstrucción de objetos.
- **`templates/index.html`**: plantilla principal de la interfaz.
- **`static/styles.css`**: estilos de la interfaz.
- **`tests/`**:
  - `conftest.py`: configuración común de tests (app de prueba, archivo JSON temporal, reseteo de estado).
  - `test_routes.py`: tests básicos de rutas y creación de usuarios.

---

### Tests

El proyecto utiliza **pytest**.

Para ejecutar los tests:

```bash
python -m pytest tests/ -v
```

Los tests actuales cubren:

- Que la página principal responde correctamente.
- Que aparece el título del gestor.
- Que la creación de usuario redirige correctamente.
- Que no se aceptan nombres vacíos.
- Que no se permiten nombres de usuario duplicados (incluyendo variaciones de mayúsculas/minúsculas).

---

### Notas y futuras mejoras posibles

- Persistencia actual en JSON (sencilla y suficiente para el proyecto).  
  Futuro: migrar a SQLite o una base de datos real.
- Sistema de usuarios es mínimo (solo nombre, sin login).  
  Futuro: añadir autenticación real, roles, etc.
- Podrían añadirse más tests:
  - Orden de tareas por prioridad/tiempo.
  - Cambio de prioridad desde la UI.
  - Completar y reabrir tareas.

Este proyecto está pensado como base de aprendizaje: puedes usarlo para practicar Flask, Jinja, organización por módulos, persistencia simple y testing con pytest.

