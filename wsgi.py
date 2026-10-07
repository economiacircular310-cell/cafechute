"""Entrada para producción.

    waitress-serve --listen=0.0.0.0:8000 wsgi:app        (Windows / Linux)
    gunicorn -w 3 -b 0.0.0.0:8000 wsgi:app               (Linux)

Si hay un proxy inverso delante (Nginx, Caddy, Cloudflare), ProxyFix hace que
Flask vea la IP real del visitante y que la petición era HTTPS.
"""
from werkzeug.middleware.proxy_fix import ProxyFix

from app import create_app

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
