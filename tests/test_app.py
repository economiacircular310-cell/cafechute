"""Pruebas del sitio: páginas, SEO, accesibilidad básica, seguridad, formularios y precios.

    python -m pytest -q
"""
from __future__ import annotations

import json
import re
import sqlite3
import xml.etree.ElementTree as ET
from datetime import date, timedelta

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.config import TestConfig
from app.i18n import INDEXABLE, LANGS, SLUGS
from app.security import limiter
from app.seo import page_path
from app.services import estimate_stay, estimate_tour, room_night_price
from app.content import ROOMS_BY_ID

ALL_PAGES = [page_path(k, lang) for k in SLUGS for lang in LANGS]


@pytest.fixture()
def app(tmp_path):
    class Cfg(TestConfig):
        DATABASE = str(tmp_path / "test.sqlite3")
        ADMIN_PASSWORD_HASH = generate_password_hash("clave-de-prueba-123")
    limiter.reset()
    return create_app(Cfg)


@pytest.fixture()
def client(app):
    return app.test_client()


def csrf(client, path: str) -> str:
    html = client.get(path).get_data(as_text=True)
    return re.search(r'name="_csrf" value="([^"]+)"', html).group(1)


def rows(app):
    con = sqlite3.connect(app.config["DATABASE"])
    con.row_factory = sqlite3.Row
    return con.execute("SELECT * FROM requests ORDER BY id").fetchall()


def future(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


# ------------------------------------------------------------------ Páginas y SEO

@pytest.mark.parametrize("path", ALL_PAGES)
def test_pages_render(client, path):
    resp = client.get(path)
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert html.count("<h1") == 1, "cada página debe tener exactamente un H1"
    assert re.search(r'<html lang="(es|en)">', html)
    for img in re.findall(r"<img\b[^>]*>", html):
        assert " alt=" in img, f"imagen sin atributo alt: {img[:120]}"


@pytest.mark.parametrize("key", INDEXABLE)
def test_seo_meta(client, key):
    for lang in LANGS:
        html = client.get(page_path(key, lang)).get_data(as_text=True)
        assert '<meta name="description"' in html
        assert '<link rel="canonical"' in html
        assert 'hreflang="es"' in html and 'hreflang="en"' in html and 'hreflang="x-default"' in html
        assert 'property="og:image"' in html
        data = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))
        assert data["@context"] == "https://schema.org"


def test_titles_and_descriptions_are_unique(client):
    titles, descs = set(), set()
    for key in INDEXABLE:
        for lang in LANGS:
            html = client.get(page_path(key, lang)).get_data(as_text=True)
            titles.add(re.search(r"<title>(.*?)</title>", html).group(1))
            descs.add(re.search(r'<meta name="description" content="([^"]*)"', html).group(1))
    assert len(titles) == len(INDEXABLE) * len(LANGS)
    assert len(descs) == len(INDEXABLE) * len(LANGS)


def test_sitemap_and_robots(client):
    root = ET.fromstring(client.get("/sitemap.xml").data)
    urls = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
    assert len(urls) == len(INDEXABLE) * len(LANGS)
    robots = client.get("/robots.txt").get_data(as_text=True)
    assert "Sitemap:" in robots and "Disallow: /admin" in robots


@pytest.mark.parametrize("old,new", [
    ("/variedades/", "/es/cafe/"), ("/procesos-del-cafe/", "/es/historia/#proceso"),
    ("/donde-comprar/", "/es/cafe/#donde-comprar"), ("/casa-chute/", "/es/casa-chute/"),
    ("/contacto/", "/es/contacto/"), ("/historia/", "/es/historia/"),
])
def test_legacy_redirects(client, old, new):
    resp = client.get(old)
    assert resp.status_code == 301 and resp.headers["Location"].endswith(new)


def test_root_redirects_by_language(client):
    assert client.get("/", headers={"Accept-Language": "en-US,en;q=0.9"}).headers["Location"].endswith("/en/")
    assert client.get("/", headers={"Accept-Language": "es-CO"}).headers["Location"].endswith("/es/")


def test_404_is_branded(client):
    resp = client.get("/es/no-existe/")
    assert resp.status_code == 404 and "secar al sol" in resp.get_data(as_text=True)


# ------------------------------------------------------------------ Seguridad

def test_security_headers(client):
    h = client.get("/es/").headers
    assert "default-src 'self'" in h["Content-Security-Policy"]
    assert "frame-ancestors 'none'" in h["Content-Security-Policy"]
    assert h["X-Frame-Options"] == "DENY"
    assert h["X-Content-Type-Options"] == "nosniff"
    assert "Server" not in h


def test_no_inline_scripts_or_styles(client):
    """La CSP prohíbe scripts y estilos en línea: ninguna plantilla debe usarlos."""
    for path in ALL_PAGES:
        html = client.get(path).get_data(as_text=True)
        for tag in re.findall(r"<script\b[^>]*>", html):
            assert " src=" in tag or 'type="application/ld+json"' in tag, (path, tag)
        assert " style=" not in html, path
        assert "<style" not in html, path


def test_csrf_required(client, app):
    resp = client.post("/es/contacto/", data={"name": "Ana", "phone": "3001234567", "message": "Hola", "consent": "1"})
    assert resp.status_code == 400
    assert rows(app) == []


def test_admin_requires_login(client):
    assert client.get("/admin/").status_code == 302
    token = csrf(client, "/admin/login")
    bad = client.post("/admin/login", data={"_csrf": token, "password": "mala"})
    assert "incorrecta" in bad.get_data(as_text=True)
    ok = client.post("/admin/login", data={"_csrf": token, "password": "clave-de-prueba-123"})
    assert ok.status_code == 302
    assert client.get("/admin/").status_code == 200
    assert client.get("/admin/exportar.csv").mimetype == "text/csv"


def test_rate_limit(client):
    token = csrf(client, "/es/contacto/")
    data = {"_csrf": token, "name": "Ana", "phone": "3001234567", "message": "Hola", "consent": "1"}
    codes = [client.post("/es/contacto/", data=data).status_code for _ in range(7)]
    assert codes[:6] == [303] * 6 and codes[6] == 400


# ------------------------------------------------------------------ Formularios

def test_booking_flow(client, app):
    token = csrf(client, "/es/reservar/")
    resp = client.post("/es/reservar/", data={
        "_csrf": token, "room": "suite", "check_in": future(10), "check_out": future(13), "guests": "2",
        "name": "Laura Gómez", "email": "laura@example.com", "phone": "+57 300 123 4567", "consent": "1",
    })
    assert resp.status_code == 303 and resp.headers["Location"].endswith("/es/gracias/")
    (row,) = rows(app)
    assert row["kind"] == "estancia" and row["estimate"] == 3 * 350_000
    thanks = client.get("/es/gracias/").get_data(as_text=True)
    assert f"#{row['id']}" in thanks and "wa.me/573102874797" in thanks


def test_booking_validation(client, app):
    token = csrf(client, "/es/reservar/")
    resp = client.post("/es/reservar/", data={
        "_csrf": token, "room": "twin", "check_in": future(5), "check_out": future(4), "guests": "3",
        "name": "", "consent": "",
    })
    assert resp.status_code == 422
    html = resp.get_data(as_text=True)
    assert 'aria-invalid="true"' in html and "Revisa los campos" in html
    assert rows(app) == []


def test_honeypot_discards_spam(client, app):
    token = csrf(client, "/es/contacto/")
    resp = client.post("/es/contacto/", data={"_csrf": token, "website": "http://spam", "name": "Bot",
                                               "phone": "3001234567", "message": "spam", "consent": "1"})
    assert resp.status_code == 303 and rows(app) == []


def test_coffee_order(client, app):
    token = csrf(client, "/es/cafe/")
    resp = client.post("/es/cafe/", data={"_csrf": token, "qty_grano": "2", "qty_molido": "1", "name": "Pedro",
                                          "phone": "3001234567", "city": "Manizales", "consent": "1"})
    assert resp.status_code == 303
    (row,) = rows(app)
    assert json.loads(row["details"])["qty"] == {"grano": 2, "molido": 1}


def test_tour_request(client, app):
    token = csrf(client, "/en/experiences/")
    resp = client.post("/en/experiences/", data={"_csrf": token, "people": "5", "date": future(20), "name": "Sam",
                                                 "email": "sam@example.com", "consent": "1"})
    assert resp.status_code == 303 and resp.headers["Location"].endswith("/en/thank-you/")
    assert rows(app)[0]["estimate"] == 2 * 170_000 + 90_000


# ------------------------------------------------------------------ Precios

def test_room_prices():
    suite, twin, cafe1 = ROOMS_BY_ID["suite"], ROOMS_BY_ID["twin"], ROOMS_BY_ID["cafe-1"]
    assert room_night_price(suite, 1) == 300_000
    assert room_night_price(suite, 3) == 400_000
    assert room_night_price(suite, 4) is None
    assert room_night_price(twin, 3) is None
    assert room_night_price(cafe1, 4) == 300_000
    assert estimate_stay("cafe-2", date(2026, 1, 1), date(2026, 1, 3), 2) == 400_000
    assert estimate_stay("cafe-2", date(2026, 1, 3), date(2026, 1, 3), 2) is None


def test_tour_prices():
    assert estimate_tour(3) is None and estimate_tour(11) is None
    assert estimate_tour(4) == 340_000
    assert estimate_tour(10) == 850_000


def test_live_api(client):
    data = client.get("/api/finca?lang=en").get_json()
    assert set(data) >= {"time", "harvest", "weather"} and data["weather"] is None  # clima desactivado en pruebas
