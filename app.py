from pathlib import Path

from flask import Flask

import router
from router import bp as tareas_bp


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = app.config.get("SECRET_KEY") or "dev-no-usar-en-produccion"
    app.config.setdefault("DATA_FILE", Path(__file__).with_name("data.json"))
    if test_config:
        app.config.update(test_config)

    app.register_blueprint(tareas_bp)

    with app.app_context():
        router.init_app()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

