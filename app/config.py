"""Configuración. Todo lo sensible o variable entre entornos se lee de variables de entorno."""
from __future__ import annotations

import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _load_dotenv() -> None:
    """Carga un .env sencillo (CLAVE=valor) sin dependencias externas."""
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()


class Config:
    SECRET_KEY = _env("SECRET_KEY") or secrets.token_hex(32)
    # Dominio público. Vacío = se toma del propio request (útil en servidores de prueba)
    SITE_URL = _env("SITE_URL").rstrip("/")
    DATABASE = _env("DATABASE", str(BASE_DIR / "instance" / "cafechute.sqlite3"))

    # Seguridad
    FORCE_HTTPS = _env("FORCE_HTTPS", "1") == "1"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _env("FORCE_HTTPS", "1") == "1"
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 8
    MAX_CONTENT_LENGTH = 64 * 1024  # solo formularios de texto
    ADMIN_PASSWORD_HASH = _env("ADMIN_PASSWORD_HASH")

    # Modo demo: no indexar en Google (robots + X-Robots-Tag). Opcional: usuario/clave de acceso.
    DEMO_MODE = _env("DEMO_MODE", "0") == "1"
    DEMO_USER = _env("DEMO_USER")
    DEMO_PASSWORD = _env("DEMO_PASSWORD")

    # Medición (vacío = sin analítica y sin banner de cookies)
    GA4_ID = _env("GA4_ID")

    # Datos legales — se muestran solo si están definidos
    RNT_NUMBER = _env("RNT_NUMBER")
    LEGAL_NAME = _env("LEGAL_NAME", "Casa Chute – Café Chute")
    LEGAL_ID = _env("LEGAL_ID")  # NIT o cédula del responsable del tratamiento de datos

    # Precio de la bolsa de 500 g en COP (vacío = "pide precio por WhatsApp")
    COFFEE_PRICE_COP = int(_env("COFFEE_PRICE_COP") or 0) or None

    # Reputación en Google (actualizar a mano o con la API de Places)
    GOOGLE_RATING = _env("GOOGLE_RATING", "4,9")
    GOOGLE_REVIEWS = int(_env("GOOGLE_REVIEWS", "10"))

    # Clima en vivo (Open-Meteo, sin clave). Poner 0 para desactivar.
    LIVE_WEATHER = _env("LIVE_WEATHER", "1") == "1"

    # Compresión gzip/brotli
    COMPRESS_MIMETYPES = ["text/html", "text/css", "application/javascript", "text/javascript", "application/json",
                          "image/svg+xml", "application/xml", "text/plain"]
    COMPRESS_MIN_SIZE = 600
    SEND_FILE_MAX_AGE_DEFAULT = 60 * 60 * 24 * 365


class DevConfig(Config):
    DEBUG = True
    FORCE_HTTPS = False
    SESSION_COOKIE_SECURE = False


class TestConfig(Config):
    TESTING = True
    SITE_URL = "https://www.cafechute.com"
    DEMO_MODE = False
    DEMO_USER = DEMO_PASSWORD = ""
    FORCE_HTTPS = False
    SESSION_COOKIE_SECURE = False
    LIVE_WEATHER = False
    SECRET_KEY = "test"
