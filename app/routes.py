"""Páginas públicas, formularios y rutas técnicas (sitemap, robots, redirecciones antiguas)."""
from __future__ import annotations

from datetime import datetime

from flask import (Response, abort, current_app, jsonify, redirect, render_template, request,
                   send_from_directory, session, url_for)

from . import db
from .content import (AMENITIES, BARISTA_TOUR, BUSINESS, COFFEE, FAQ, POLICIES, PROCESS, RATE_NOTE,
                      ROOMS, ROOMS_BY_ID, SPACES, WHERE_TO_BUY)
from .i18n import DEFAULT_LANG, LANGS, META, SLUGS, format_cop, t, tr
from .live import snapshot
from .security import allow, csrf_token
from .seo import abs_url, alternates, json_ld, page_path, sitemap_xml
from .services import (MAX_NIGHTS, Form, estimate_stay, estimate_tour, harvest_status,
                       room_night_price, today_local, whatsapp_link)

FORM_PAGES = {"reservar", "cafe", "experiencias", "contacto"}

# URLs del WordPress anterior -> nuevas (301 conserva el posicionamiento ganado)
LEGACY = {
    "/home/": "/es/",
    "/variedades/": "/es/cafe/",
    "/procesos-del-cafe/": "/es/historia/#proceso",
    "/donde-comprar/": "/es/cafe/#donde-comprar",
    "/historia/": "/es/historia/",
    "/casa-chute/": "/es/casa-chute/",
    "/contacto/": "/es/contacto/",
}


# --------------------------------------------------------------------- helpers

def url_page(key: str, lang: str, anchor: str = "", **query) -> str:
    path = page_path(key, lang)
    if query:
        from urllib.parse import urlencode
        path += "?" + urlencode(query)
    return path + (f"#{anchor}" if anchor else "")


def render_page(key: str, lang: str, status: int = 200, **ctx):
    title, description = META[key][lang]
    other = "en" if lang == "es" else "es"
    ctx.update(
        page=key,
        lang=lang,
        other_lang=other,
        other_lang_url=page_path(key, other),
        meta_title=title,
        meta_description=description,
        canonical=abs_url(page_path(key, lang)),
        hreflangs=alternates(key),
        json_ld=json_ld(key, lang),
        og_image=abs_url(url_for("static", filename=f"img/og-{lang}.jpg")),
        noindex=key == "gracias",
    )
    return render_template(f"{key}.html", **ctx), status


def rate_limited(bucket: str) -> bool:
    return not allow(bucket, limit=6, window=600)


def csrf_failed() -> bool:
    return bool(getattr(request, "csrf_failed", False))


def form_guard(form: Form, lang: str, bucket: str) -> str | None:
    """Devuelve un error global si el envío debe rechazarse."""
    if csrf_failed():
        return t("err.csrf", lang)
    if rate_limited(bucket):
        return t("err.rate", lang)
    return None


def finish(req_id: int, kind: str, lang: str, wa_text: str):
    session["last_request"] = {"id": req_id, "kind": kind, "wa": wa_text}
    return redirect(url_page("gracias", lang), code=303)


# --------------------------------------------------------------------- vistas

def view_home(lang: str):
    return render_page("home", lang, rooms=ROOMS, process=PROCESS, coffee=COFFEE, tour=BARISTA_TOUR)


def view_casa(lang: str):
    return render_page("casa", lang, rooms=ROOMS, spaces=SPACES, faq=FAQ,
                       amenities=[a for a in AMENITIES if a[2]], policies=[p for p in POLICIES if p[2]],
                       booking=_booking_defaults(lang), rate_note=RATE_NOTE)


def _booking_defaults(lang: str) -> dict:
    room_id = request.args.get("room", "")
    return {"room": room_id if room_id in ROOMS_BY_ID else "", "guests": "2",
            "check_in": "", "check_out": "", "name": "", "email": "", "phone": "", "message": ""}


def view_reservar(lang: str):
    if request.method == "GET":
        return render_page("reservar", lang, rooms=ROOMS, booking=_booking_defaults(lang), errors={})

    form = Form(request.form.to_dict())
    global_error = form_guard(form, lang, "booking")
    if form.is_spam:
        return redirect(url_page("gracias", lang), code=303)
    room_id = form.text("room", lang, max_len=20)
    if room_id not in ROOMS_BY_ID:
        form.errors["room"] = t("err.room", lang)
    check_in, check_out = form.date_("check_in", lang), form.date_("check_out", lang)
    guests = form.integer("guests", lang, 1, 10, "err.guests")
    name = form.text("name", lang, max_len=120)
    email, phone = form.email(lang), form.phone(lang)
    form.contact_required(lang, email, phone)
    message = form.text("message", lang, required=False, max_len=1500)
    form.consent(lang)

    estimate = None
    if check_in and check_out:
        nights = (check_out - check_in).days
        if check_in < today_local() or nights < 1 or nights > MAX_NIGHTS:
            form.errors["check_out"] = t("err.dates", lang)
    room = ROOMS_BY_ID.get(room_id)
    if room and guests and room_night_price(room, guests) is None:
        form.errors["guests"] = t("err.guests", lang)
    if form.ok and room:
        estimate = estimate_stay(room_id, check_in, check_out, guests)

    if global_error or not form.ok:
        return render_page("reservar", lang, status=400 if global_error else 422, rooms=ROOMS,
                           booking=form.data, errors=form.errors, global_error=global_error or t("err.form", lang))

    nights = (check_out - check_in).days
    details = {"room": room_id, "room_name": tr(room["name"], "es"), "check_in": check_in.isoformat(),
               "check_out": check_out.isoformat(), "nights": nights, "guests": guests}
    req_id = db.create_request(kind="estancia", lang=lang, name=name, email=email, phone=phone,
                               details=details, estimate=estimate, message=message)
    wa = (f"{'Hola, Casa Chute. Quiero reservar' if lang == 'es' else 'Hi Casa Chute! I would like to book'}: "
          f"{tr(room['name'], lang)} · {check_in:%d/%m/%Y} → {check_out:%d/%m/%Y} · {guests} "
          f"{t('book.guests', lang).lower()} · {format_cop(estimate, lang)} COP (#{req_id})")
    return finish(req_id, "estancia", lang, wa)


def view_cafe(lang: str):
    ctx = dict(coffee=COFFEE, process=PROCESS, where=WHERE_TO_BUY,
               price=current_app.config.get("COFFEE_PRICE_COP"))
    if request.method == "GET":
        return render_page("cafe", lang, order={}, errors={}, **ctx)

    form = Form(request.form.to_dict())
    global_error = form_guard(form, lang, "order")
    if form.is_spam:
        return redirect(url_page("gracias", lang), code=303)
    qty = {fid: form.integer(f"qty_{fid}", lang, 0, 50) for fid, _ in COFFEE["formats"]}
    if sum(qty.values()) < 1:
        form.errors["qty_grano"] = t("err.qty", lang)
    name = form.text("name", lang, max_len=120)
    email = form.email(lang)
    phone = form.phone(lang, required=True)
    city = form.text("city", lang, max_len=80)
    address = form.text("address", lang, required=False, max_len=250)
    notes = form.text("message", lang, required=False, max_len=1000)
    form.consent(lang)
    if global_error or not form.ok:
        return render_page("cafe", lang, status=400 if global_error else 422, order=form.data,
                           errors=form.errors, global_error=global_error or t("err.form", lang), **ctx)

    price = ctx["price"]
    total = price * sum(qty.values()) if price else None
    details = {"qty": qty, "city": city, "address": address, "unit_price": price}
    req_id = db.create_request(kind="cafe", lang=lang, name=name, email=email, phone=phone,
                               details=details, estimate=total, message=notes)
    parts = [f"{n} × {tr(lbl, lang).lower()}" for fid, lbl in COFFEE["formats"] if (n := qty[fid])]
    wa = f"{t('wa.coffee', lang)} {', '.join(parts)} (500 g) · {city} (#{req_id})"
    return finish(req_id, "cafe", lang, wa)


def view_experiencias(lang: str):
    ctx = dict(tour=BARISTA_TOUR, spaces=SPACES)
    if request.method == "GET":
        return render_page("experiencias", lang, req={"people": "4"}, errors={}, **ctx)

    form = Form(request.form.to_dict())
    global_error = form_guard(form, lang, "tour")
    if form.is_spam:
        return redirect(url_page("gracias", lang), code=303)
    people = form.integer("people", lang, BARISTA_TOUR["min_people"], BARISTA_TOUR["max_people"], "err.people")
    when = form.date_("date", lang)
    if when and when < today_local():
        form.errors["date"] = t("err.dates", lang)
    name = form.text("name", lang, max_len=120)
    email, phone = form.email(lang), form.phone(lang)
    form.contact_required(lang, email, phone)
    message = form.text("message", lang, required=False, max_len=1500)
    form.consent(lang)
    if global_error or not form.ok:
        return render_page("experiencias", lang, status=400 if global_error else 422, req=form.data,
                           errors=form.errors, global_error=global_error or t("err.form", lang), **ctx)

    estimate = estimate_tour(people)
    req_id = db.create_request(kind="tour", lang=lang, name=name, email=email, phone=phone,
                               details={"people": people, "date": when.isoformat()}, estimate=estimate,
                               message=message)
    wa = f"{t('wa.tour', lang)} {people} · {when:%d/%m/%Y} · {format_cop(estimate, lang)} COP (#{req_id})"
    return finish(req_id, "tour", lang, wa)


def view_contacto(lang: str):
    if request.method == "GET":
        topic = request.args.get("tema", "estancia")
        return render_page("contacto", lang, msg={"topic": topic}, errors={})

    form = Form(request.form.to_dict())
    global_error = form_guard(form, lang, "contact")
    if form.is_spam:
        return redirect(url_page("gracias", lang), code=303)
    topic = form.data.get("topic") if form.data.get("topic") in ("estancia", "cafe", "tour", "otro") else "otro"
    name = form.text("name", lang, max_len=120)
    email, phone = form.email(lang), form.phone(lang)
    form.contact_required(lang, email, phone)
    message = form.text("message", lang, max_len=3000)
    form.consent(lang)
    if global_error or not form.ok:
        return render_page("contacto", lang, status=400 if global_error else 422, msg=form.data,
                           errors=form.errors, global_error=global_error or t("err.form", lang))
    req_id = db.create_request(kind="mensaje", lang=lang, name=name, email=email, phone=phone,
                               details={"topic": topic}, estimate=None, message=message)
    return finish(req_id, "mensaje", lang, f"{t('wa.default', lang)} (#{req_id})")


def view_historia(lang: str):
    return render_page("historia", lang, process=PROCESS, coffee=COFFEE)


def view_privacidad(lang: str):
    return render_page("privacidad", lang)


def view_gracias(lang: str):
    last = session.get("last_request")
    wa = whatsapp_link(last["wa"]) if last else whatsapp_link(t("wa.default", lang))
    return render_page("gracias", lang, last=last, wa_summary=wa)


VIEWS = {
    "home": view_home, "casa": view_casa, "cafe": view_cafe, "experiencias": view_experiencias,
    "historia": view_historia, "contacto": view_contacto, "reservar": view_reservar,
    "privacidad": view_privacidad, "gracias": view_gracias,
}


# --------------------------------------------------------------------- registro

def init_app(app) -> None:
    for key in SLUGS:
        for lang in LANGS:
            methods = ["GET", "POST"] if key in FORM_PAGES else ["GET"]
            app.add_url_rule(page_path(key, lang), endpoint=f"{key}_{lang}",
                             view_func=(lambda k=key, l=lang: VIEWS[k](l)), methods=methods)

    @app.context_processor
    def _globals():
        lang = getattr(request, "lang", DEFAULT_LANG)
        return {
            "t": lambda key, **kw: t(key, lang, **kw),
            "tr": lambda value: tr(value, lang),
            "cop": lambda value: format_cop(value, lang),
            "url_page": lambda key, anchor="", **q: url_page(key, lang, anchor, **q),
            "biz": BUSINESS,
            "cfg": app.config,
            "csrf_token": csrf_token,
            "wa": lambda key="wa.default": whatsapp_link(t(key, lang)),
            "harvest": harvest_status(lang),
            "year": datetime.now().year,
            "rooms_by_id": ROOMS_BY_ID,
        }

    @app.before_request
    def _detect_lang():
        first = request.path.strip("/").split("/", 1)[0]
        request.lang = first if first in LANGS else DEFAULT_LANG  # type: ignore[attr-defined]

    @app.route("/")
    def root():
        best = request.accept_languages.best_match(LANGS, default=DEFAULT_LANG)
        resp = redirect(page_path("home", best), code=302)
        resp.headers["Vary"] = "Accept-Language"
        return resp

    for old, new in LEGACY.items():
        app.add_url_rule(old, endpoint=f"legacy_{old.strip('/')}", view_func=(lambda n=new: redirect(n, code=301)))

    @app.route("/api/finca")
    def api_finca():
        lang = request.args.get("lang", DEFAULT_LANG)
        lang = lang if lang in LANGS else DEFAULT_LANG
        resp = jsonify(snapshot(lang, current_app.config.get("LIVE_WEATHER", True)))
        resp.headers["Cache-Control"] = "public, max-age=300"
        return resp

    @app.route("/sitemap.xml")
    def sitemap():
        return Response(sitemap_xml(), mimetype="application/xml")

    @app.route("/robots.txt")
    def robots():
        if current_app.config.get("DEMO_MODE"):
            return Response("User-agent: *\nDisallow: /\n", mimetype="text/plain")
        body = f"User-agent: *\nDisallow: /admin\nDisallow: /api/\n\nSitemap: {abs_url('/sitemap.xml')}\n"
        return Response(body, mimetype="text/plain")

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(app.static_folder, "favicon.ico", max_age=31536000)

    @app.route("/.well-known/security.txt")
    def security_txt():
        expires = datetime.now().replace(year=datetime.now().year + 1).strftime("%Y-%m-%dT00:00:00Z")
        body = f"Contact: mailto:{BUSINESS['email']}\nPreferred-Languages: es, en\nExpires: {expires}\n"
        return Response(body, mimetype="text/plain")

    @app.errorhandler(404)
    def not_found(_e):
        lang = getattr(request, "lang", DEFAULT_LANG)
        return render_template("404.html", lang=lang, other_lang="en" if lang == "es" else "es",
                               other_lang_url=page_path("home", "en" if lang == "es" else "es"),
                               page="404", meta_title=t("404.title", lang), meta_description="",
                               noindex=True, hreflangs=[], canonical="", json_ld="", og_image=""), 404

    @app.errorhandler(400)
    def bad_request(_e):
        lang = getattr(request, "lang", DEFAULT_LANG)
        return render_template("error.html", lang=lang, other_lang="en" if lang == "es" else "es",
                               other_lang_url=page_path("home", "en" if lang == "es" else "es"),
                               page="error", meta_title=t("err.csrf", lang), message=t("err.csrf", lang),
                               meta_description="", noindex=True, hreflangs=[], canonical="",
                               json_ld="", og_image=""), 400

    @app.errorhandler(500)
    def server_error(_e):
        lang = getattr(request, "lang", DEFAULT_LANG)
        return render_template("error.html", lang=lang, other_lang="en" if lang == "es" else "es",
                               other_lang_url=page_path("home", "en" if lang == "es" else "es"),
                               page="error", meta_title=t("500.title", lang), message=t("500.text", lang),
                               meta_description="", noindex=True, hreflangs=[], canonical="",
                               json_ld="", og_image=""), 500
