"""Casa Chute · Café Chute — sitio web en Flask."""
from __future__ import annotations

import hashlib
from pathlib import Path

from flask import Flask
from flask_compress import Compress

from . import admin, art, db, routes, security
from .config import Config
from .images import image, srcset


def create_app(config: type[Config] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config or Config)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    Compress(app)
    security.init_app(app)
    db.init_app(app)
    routes.init_app(app)
    app.register_blueprint(admin.bp)

    _static_versioning(app)

    @app.context_processor
    def _images():
        from flask import url_for
        return {"img": image, "srcset": lambda slug: srcset(slug, lambda f: url_for("static", filename=f))}

    from .content import COFFEE
    from .i18n import MONTHS, t
    from .services import harvest_status

    def _ring(lang: str):
        h = harvest_status(lang)
        return art.harvest_ring(MONTHS[lang], COFFEE["harvest_months"], h["month"], t("home.calendar_title", lang))

    app.jinja_env.globals.update(dandelion=art.dandelion, topo=art.topo, harvest_ring=_ring)

    return app


def _static_versioning(app: Flask) -> None:
    """Añade ?v=<hash> a los archivos estáticos para poder cachearlos un año sin riesgo."""
    cache: dict[str, str] = {}
    static = Path(app.static_folder)

    @app.url_defaults
    def _add_version(endpoint, values):
        if endpoint != "static" or "filename" not in values or "v" in values:
            return
        filename = values["filename"]
        if filename.startswith("fonts/"):
            return  # el CSS las pide sin ?v=; el preload debe usar la misma URL
        if filename not in cache or app.debug:
            path = static / filename
            cache[filename] = hashlib.md5(path.read_bytes()).hexdigest()[:10] if path.is_file() else ""
        if cache[filename]:
            values["v"] = cache[filename]
