"""Cabeceras de seguridad, CSRF, limitación de envíos y redirección a HTTPS."""
from __future__ import annotations

import hmac
import secrets
import threading
import time
from collections import defaultdict, deque

from flask import Response, abort, current_app, redirect, request, session

# --------------------------------------------------------------------------- CSRF

def csrf_token() -> str:
    token = session.get("_csrf")
    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf"] = token
    return token


def csrf_valid() -> bool:
    sent = request.form.get("_csrf", "")
    expected = session.get("_csrf", "")
    return bool(sent) and bool(expected) and hmac.compare_digest(sent, expected)


# --------------------------------------------------------------- Rate limiting
class RateLimiter:
    """Ventana deslizante en memoria (suficiente para un solo proceso; con varios
    procesos usar Redis o el proxy inverso)."""

    def __init__(self) -> None:
        self._hits: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()

    def hit(self, key: str, limit: int, window: int) -> bool:
        now = time.monotonic()
        with self._lock:
            q = self._hits[key]
            while q and now - q[0] > window:
                q.popleft()
            if len(q) >= limit:
                return False
            q.append(now)
            return True

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


limiter = RateLimiter()


def client_ip() -> str:
    # Detrás de un proxy, configurar ProxyFix en wsgi.py para que remote_addr sea la IP real.
    return request.remote_addr or "?"


def allow(bucket: str, limit: int, window: int) -> bool:
    return limiter.hit(f"{bucket}:{client_ip()}", limit, window)


# --------------------------------------------------------------- Cabeceras

def build_csp(extra_frame: bool = False) -> str:
    ga = bool(current_app.config.get("GA4_ID"))
    script_src = "'self'" + (" https://www.googletagmanager.com" if ga else "")
    connect_src = "'self'" + (" https://*.google-analytics.com https://*.analytics.google.com https://www.googletagmanager.com" if ga else "")
    return "; ".join([
        "default-src 'self'",
        f"script-src {script_src}",
        "style-src 'self'",
        "img-src 'self' data: https://i.ytimg.com" + (" https://www.googletagmanager.com https://*.google-analytics.com" if ga else ""),
        "font-src 'self'",
        f"connect-src {connect_src}",
        "frame-src https://www.youtube-nocookie.com https://www.google.com",
        "frame-ancestors 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "object-src 'none'",
        "upgrade-insecure-requests" if current_app.config.get("FORCE_HTTPS") else "",
    ]).strip("; ")


def init_app(app) -> None:
    @app.before_request
    def _demo_auth():
        user, pw = app.config.get("DEMO_USER"), app.config.get("DEMO_PASSWORD")
        if not (user and pw) or request.path in ("/robots.txt", "/favicon.ico"):
            return None
        auth = request.authorization
        if auth and hmac.compare_digest(auth.username or "", user) and hmac.compare_digest(auth.password or "", pw):
            return None
        return Response("Acceso restringido — versión de prueba", 401,
                        {"WWW-Authenticate": 'Basic realm="Casa Chute (demo)", charset="UTF-8"'})

    @app.before_request
    def _https_and_csrf():
        if app.config.get("FORCE_HTTPS") and not request.is_secure and request.host.split(":")[0] not in ("localhost", "127.0.0.1"):
            return redirect(request.url.replace("http://", "https://", 1), code=301)
        if request.method == "POST" and not csrf_valid():
            # El error se muestra en la propia página (ver routes._csrf_failed)
            request.csrf_failed = True  # type: ignore[attr-defined]

    @app.after_request
    def _headers(resp):
        h = resp.headers
        h["Content-Security-Policy"] = build_csp()
        h["X-Content-Type-Options"] = "nosniff"
        h["X-Frame-Options"] = "DENY"
        h["Referrer-Policy"] = "strict-origin-when-cross-origin"
        h["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
        h["Cross-Origin-Opener-Policy"] = "same-origin"
        if app.config.get("FORCE_HTTPS"):
            h["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        h.pop("Server", None)
        if app.config.get("DEMO_MODE"):
            h["X-Robots-Tag"] = "noindex, nofollow"
        if request.path.startswith("/static/"):
            h["Cache-Control"] = "public, max-age=31536000, immutable"
        elif request.path.startswith("/admin"):
            h["Cache-Control"] = "no-store"
            h["X-Robots-Tag"] = "noindex, nofollow"
        elif resp.mimetype == "text/html":
            h.setdefault("Cache-Control", "no-cache")
        return resp


def require_csrf() -> None:
    if getattr(request, "csrf_failed", False):
        abort(400)
