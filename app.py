from flask import Flask

from router import bp as tareas_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = app.config.get("SECRET_KEY") or "dev-no-usar-en-produccion"

    app.register_blueprint(tareas_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

