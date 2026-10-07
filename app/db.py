"""SQLite: solicitudes de reserva, pedidos de café y mensajes. Sin ORM: consultas parametrizadas."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS requests (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  TEXT    NOT NULL,
    kind        TEXT    NOT NULL CHECK (kind IN ('estancia', 'tour', 'cafe', 'mensaje')),
    lang        TEXT    NOT NULL,
    name        TEXT    NOT NULL,
    email       TEXT,
    phone       TEXT,
    details     TEXT    NOT NULL,      -- JSON con los datos específicos de cada tipo
    estimate    INTEGER,               -- valor estimado en COP calculado en el servidor
    message     TEXT,
    consent_at  TEXT    NOT NULL,      -- Ley 1581: momento de la autorización
    status      TEXT    NOT NULL DEFAULT 'nueva' CHECK (status IN ('nueva', 'en_proceso', 'cerrada'))
);
CREATE INDEX IF NOT EXISTS idx_requests_created ON requests (created_at DESC);
"""

KINDS = ("estancia", "tour", "cafe", "mensaje")
STATUSES = ("nueva", "en_proceso", "cerrada")


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        path = Path(current_app.config["DATABASE"])
        path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
    return g.db


def close_db(_exc=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    get_db().executescript(SCHEMA)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_request(*, kind: str, lang: str, name: str, email: str | None, phone: str | None,
                   details: dict, estimate: int | None, message: str | None) -> int:
    db = get_db()
    cur = db.execute(
        "INSERT INTO requests (created_at, kind, lang, name, email, phone, details, estimate, message, consent_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (now_iso(), kind, lang, name, email or None, phone or None,
         json.dumps(details, ensure_ascii=False), estimate, message or None, now_iso()),
    )
    db.commit()
    return cur.lastrowid


def list_requests(kind: str | None = None, status: str | None = None, limit: int = 500) -> list[sqlite3.Row]:
    sql = "SELECT * FROM requests WHERE 1=1"
    args: list = []
    if kind in KINDS:
        sql += " AND kind = ?"
        args.append(kind)
    if status in STATUSES:
        sql += " AND status = ?"
        args.append(status)
    sql += " ORDER BY created_at DESC LIMIT ?"
    args.append(limit)
    return get_db().execute(sql, args).fetchall()


def counts() -> dict:
    rows = get_db().execute("SELECT kind, status, COUNT(*) AS n FROM requests GROUP BY kind, status").fetchall()
    out: dict = {k: {"total": 0, "nueva": 0} for k in KINDS}
    for r in rows:
        out[r["kind"]]["total"] += r["n"]
        if r["status"] == "nueva":
            out[r["kind"]]["nueva"] += r["n"]
    return out


def set_status(req_id: int, status: str) -> None:
    if status not in STATUSES:
        raise ValueError("estado no válido")
    db = get_db()
    db.execute("UPDATE requests SET status = ? WHERE id = ?", (status, req_id))
    db.commit()


def init_app(app) -> None:
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
