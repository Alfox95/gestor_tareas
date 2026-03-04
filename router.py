from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import DIAS_POR_DEFECTO, Tarea, Usuario

bp = Blueprint("tareas", __name__)

# Datos en memoria
tareas: list[Tarea] = []
usuarios: list[Usuario] = []
siguiente_id = 1
siguiente_usuario_id = 1


@bp.route("/")
def index():
    def clave_pendiente(t: Tarea) -> tuple[int, int, int]:
        dias_val = t.dias_restantes_para_ordenar()
        # 1) Las que tienen ≤2 días primero; 2) luego por prioridad (5→1); 3) luego por días (menos primero)
        urgente_tiempo = 0 if dias_val <= 2 else 1
        return (urgente_tiempo, -t.prioridad, dias_val)

    tareas_pendientes = sorted(
        (t for t in tareas if not t.completo),
        key=clave_pendiente,
    )
    tareas_completas = sorted(
        (t for t in tareas if t.completo),
        key=lambda t: t.fecha_realizada or t.fecha_creado,
        reverse=True,
    )

    return render_template(
        "index.html",
        tareas_pendientes=tareas_pendientes,
        tareas_completas=tareas_completas,
        usuarios=usuarios,
    )


@bp.route("/usuarios/crear", methods=["POST"])
def crear_usuario():
    global siguiente_usuario_id
    nombre = request.form.get("nombre_usuario", "").strip()
    if not nombre:
        return redirect(url_for("tareas.index"))

    nombre_normalizado = nombre.lower()
    if any(u.nombre.lower() == nombre_normalizado for u in usuarios):
        flash("El usuario ya existe.", "error")
        return redirect(url_for("tareas.index"))

    nuevo_usuario = Usuario(id=siguiente_usuario_id, nombre=nombre)
    usuarios.append(nuevo_usuario)
    siguiente_usuario_id += 1

    return redirect(url_for("tareas.index"))


@bp.route("/agregar", methods=["POST"])
def agregar():
    global siguiente_id
    descripcion = request.form.get("texto", "").strip()
    prioridad_raw = request.form.get("prioridad", "").strip()
    fecha_max_raw = request.form.get("fecha_max", "").strip()
    usuario_crea_raw = request.form.get("usuario_crea", "").strip()

    if not descripcion:
        return redirect(url_for("tareas.index"))

    if not usuario_crea_raw.isdigit():
        return redirect(url_for("tareas.index"))

    usuario_crea_id = int(usuario_crea_raw)
    creador = next((u for u in usuarios if u.id == usuario_crea_id), None)
    if creador is None:
        return redirect(url_for("tareas.index"))

    prioridad = 3
    if prioridad_raw.isdigit():
        prioridad_int = int(prioridad_raw)
        if 1 <= prioridad_int <= 5:
            prioridad = prioridad_int

    fecha_max = None
    if fecha_max_raw:
        try:
            fecha_max = date.fromisoformat(fecha_max_raw)
        except ValueError:
            fecha_max = None

    nueva_tarea = Tarea(
        id=siguiente_id,
        descripcion=descripcion,
        prioridad=prioridad,
        fecha_max=fecha_max,
        creador=creador,
    )
    tareas.append(nueva_tarea)
    siguiente_id += 1

    return redirect(url_for("tareas.index"))


@bp.route("/completar/<int:tarea_id>", methods=["POST"])
def completar(tarea_id: int):
    usuario_completa_raw = request.form.get("usuario_completa", "").strip()
    if not usuario_completa_raw.isdigit():
        return redirect(url_for("tareas.index"))

    usuario_completa_id = int(usuario_completa_raw)
    completador = next((u for u in usuarios if u.id == usuario_completa_id), None)
    if completador is None:
        return redirect(url_for("tareas.index"))

    for tarea in tareas:
        if tarea.id == tarea_id:
            tarea.completo = True
            tarea.fecha_realizada = datetime.now()
            tarea.completador = completador
            break
    return redirect(url_for("tareas.index"))


@bp.route("/tarea/<int:tarea_id>/prioridad/subir", methods=["POST"])
def subir_prioridad(tarea_id: int):
    for tarea in tareas:
        if tarea.id == tarea_id and not tarea.completo and tarea.prioridad < 5:
            tarea.editar_prioridad(tarea.prioridad + 1)
            break
    return redirect(url_for("tareas.index"))


@bp.route("/tarea/<int:tarea_id>/prioridad/bajar", methods=["POST"])
def bajar_prioridad(tarea_id: int):
    for tarea in tareas:
        if tarea.id == tarea_id and not tarea.completo and tarea.prioridad > 1:
            tarea.editar_prioridad(tarea.prioridad - 1)
            break
    return redirect(url_for("tareas.index"))


@bp.route("/reabrir/<int:tarea_id>", methods=["POST"])
def reabrir(tarea_id: int):
    for tarea in tareas:
        if tarea.id == tarea_id and tarea.completo:
            tarea.completo = False
            # fecha_realizada y completador se mantienen como historial
            break
    return redirect(url_for("tareas.index"))

