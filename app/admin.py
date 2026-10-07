"""Panel interno: ver y gestionar solicitudes de reserva, pedidos de café, tours y mensajes."""
from __future__ import annotations

import csv
import io
import json
from functools import wraps

from flask import (Blueprint, Response, abort, current_app, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash

from . import db
from .content import ROOMS_BY_ID
from .i18n import format_cop
from .security import allow, csrf_token

bp = Blueprint("admin", __name__, url_prefix="/admin")

KIND_LABEL = {"estancia": "Estancias", "tour": "Barista Show Tour®", "cafe": "Pedidos de café", "mensaje": "Mensajes"}
STATUS_LABEL = {"nueva": "Nueva", "en_proceso": "En proceso", "cerrada": "Cerrada"}


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin.login", next=request.path))
        return view(*args, **kwargs)
    return wrapper


@bp.context_processor
def _ctx():
    return {"csrf_token": csrf_token, "KIND_LABEL": KIND_LABEL, "STATUS_LABEL": STATUS_LABEL,
            "cop": lambda v: format_cop(v, "es") if v else "—", "rooms_by_id": ROOMS_BY_ID}


@bp.route("/login", methods=["GET", "POST"])
def login():
    configured = bool(current_app.config.get("ADMIN_PASSWORD_HASH"))
    error = None
    if request.method == "POST":
        if getattr(request, "csrf_failed", False):
            error = "La sesión expiró, vuelve a intentarlo."
        elif not allow("admin-login", limit=5, window=900):
            error = "Demasiados intentos. Espera 15 minutos."
        elif configured and check_password_hash(current_app.config["ADMIN_PASSWORD_HASH"], request.form.get("password", "")):
            session.clear()
            session["admin"] = True
            session.permanent = True
            nxt = request.args.get("next", "")
            return redirect(nxt if nxt.startswith("/admin") else url_for("admin.dashboard"))
        else:
            error = "Contraseña incorrecta."
    return render_template("admin/login.html", configured=configured, error=error)


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@bp.route("/")
@login_required
def dashboard():
    kind = request.args.get("tipo")
    status = request.args.get("estado")
    rows = db.list_requests(kind, status)
    items = []
    for r in rows:
        d = dict(r)
        d["details"] = json.loads(d["details"])
        items.append(d)
    return render_template("admin/dashboard.html", items=items, counts=db.counts(), kind=kind, status=status)


@bp.route("/solicitud/<int:req_id>/estado", methods=["POST"])
@login_required
def change_status(req_id: int):
    if getattr(request, "csrf_failed", False):
        abort(400)
    try:
        db.set_status(req_id, request.form.get("status", ""))
    except ValueError:
        abort(400)
    return redirect(request.referrer if (request.referrer or "").startswith(request.host_url + "admin") else url_for("admin.dashboard"))


@bp.route("/exportar.csv")
@login_required
def export_csv():
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["id", "fecha", "tipo", "estado", "idioma", "nombre", "correo", "teléfono", "detalles", "valor_estimado_cop", "mensaje"])
    for r in db.list_requests(limit=10_000):
        w.writerow([r["id"], r["created_at"], r["kind"], r["status"], r["lang"], r["name"], r["email"] or "",
                    r["phone"] or "", r["details"], r["estimate"] or "", r["message"] or ""])
    return Response("﻿" + out.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=solicitudes-casa-chute.csv"})
