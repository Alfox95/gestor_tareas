from datetime import date, datetime

from flask import Blueprint, redirect, render_template, request, url_for

from models import Tarea

bp = Blueprint("tareas", __name__)

# Lista de tareas en memoria
tareas: list[Tarea] = []
siguiente_id = 1


@bp.route("/")
def index():
    return render_template("index.html", tareas=tareas)


@bp.route("/agregar", methods=["POST"])
def agregar():
    global siguiente_id
    descripcion = request.form.get("texto", "").strip()
    prioridad_raw = request.form.get("prioridad", "").strip()
    fecha_max_raw = request.form.get("fecha_max", "").strip()

    if not descripcion:
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
    )
    tareas.append(nueva_tarea)
    siguiente_id += 1

    return redirect(url_for("tareas.index"))


@bp.route("/completar/<int:tarea_id>", methods=["POST"])
def completar(tarea_id: int):
    for tarea in tareas:
        if tarea.id == tarea_id:
            tarea.completo = True
            tarea.fecha_realizada = datetime.now()
            break
    return redirect(url_for("tareas.index"))

