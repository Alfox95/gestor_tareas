from flask import Flask, redirect, render_template, request, url_for


def create_app() -> Flask:
    app = Flask(__name__)

    # Lista de tareas en memoria
    tareas = []
    siguiente_id = 1

    @app.route("/")
    def index():
        return render_template("index.html", tareas=tareas)

    @app.route("/agregar", methods=["POST"])
    def agregar():
        nonlocal siguiente_id
        texto = request.form.get("texto", "").strip()
        if texto:
            tareas.append(
                {"id": siguiente_id, "texto": texto, "hecho": False},
            )
            siguiente_id += 1
        return redirect(url_for("index"))

    @app.route("/completar/<int:tarea_id>", methods=["POST"])
    def completar(tarea_id: int):
        for tarea in tareas:
            if tarea["id"] == tarea_id:
                tarea["hecho"] = True
                break
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

