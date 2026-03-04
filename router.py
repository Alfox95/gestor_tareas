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
    if descripcion:
        nueva_tarea = Tarea(id=siguiente_id, descripcion=descripcion)
        tareas.append(nueva_tarea)
        siguiente_id += 1
    return redirect(url_for("tareas.index"))


@bp.route("/completar/<int:tarea_id>", methods=["POST"])
def completar(tarea_id: int):
    for tarea in tareas:
        if tarea.id == tarea_id:
            tarea.completo = True
            break
    return redirect(url_for("tareas.index"))

