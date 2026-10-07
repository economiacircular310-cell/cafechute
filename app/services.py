"""Lógica de negocio: precios, validación, temporada de cosecha y enlaces de WhatsApp."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from urllib.parse import quote

from .content import BARISTA_TOUR, BUSINESS, COFFEE, ROOMS_BY_ID
from .i18n import MONTHS_LONG, t

# Colombia no tiene horario de verano: UTC-5 fijo (evita depender de tzdata en Windows)
TZ = timezone(timedelta(hours=-5), "COT")
EMAIL_RE = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,190}\.[a-zA-Z]{2,24}$")
PHONE_RE = re.compile(r"^\+?[\d\s().-]{7,20}$")
MAX_NIGHTS = 60


def today_local() -> date:
    return datetime.now(TZ).date()


# --------------------------------------------------------------- Precios

def room_night_price(room: dict, guests: int) -> int | None:
    """Precio por noche según huéspedes, con las tarifas publicadas. None = no válido."""
    if guests < 1 or guests > room["capacity"]:
        return None
    if guests == 1:
        return room["solo"]
    price = room["pair"]
    extra_guests = guests - 2
    if extra_guests > 0:
        if room["extra"] is None:
            return None
        price += extra_guests * room["extra"]
    return price


def estimate_stay(room_id: str, check_in: date, check_out: date, guests: int) -> int | None:
    room = ROOMS_BY_ID.get(room_id)
    if not room:
        return None
    nights = (check_out - check_in).days
    per_night = room_night_price(room, guests)
    if per_night is None or nights < 1:
        return None
    return per_night * nights


def estimate_tour(people: int) -> int | None:
    if not BARISTA_TOUR["min_people"] <= people <= BARISTA_TOUR["max_people"]:
        return None
    pairs, singles = divmod(people, 2)
    return pairs * BARISTA_TOUR["pair"] + singles * BARISTA_TOUR["person"]


# --------------------------------------------------------------- Cosecha

def harvest_status(lang: str, on: date | None = None) -> dict:
    d = on or today_local()
    months = COFFEE["harvest_months"]
    active = d.month in months
    nxt = next((m for m in sorted(months) if m > d.month), sorted(months)[0])
    label = t("live.harvest_on", lang) if active else t("live.harvest_off", lang, m=MONTHS_LONG[lang][nxt - 1])
    return {"active": active, "month": d.month, "next": nxt, "label": label}


# --------------------------------------------------------------- WhatsApp

def whatsapp_link(text: str) -> str:
    return f"https://wa.me/{BUSINESS['whatsapp']}?text={quote(text)}"


# --------------------------------------------------------------- Validación
@dataclass
class Form:
    data: dict
    errors: dict = field(default_factory=dict)

    def text(self, name: str, lang: str, *, required: bool = True, max_len: int = 200) -> str:
        value = (self.data.get(name) or "").strip()[:max_len]
        if required and not value:
            self.errors[name] = t("err.required", lang)
        return value

    def email(self, lang: str, *, required: bool = False) -> str:
        value = (self.data.get("email") or "").strip()[:254]
        if value and not EMAIL_RE.match(value):
            self.errors["email"] = t("err.email", lang)
        elif required and not value:
            self.errors["email"] = t("err.required", lang)
        return value

    def phone(self, lang: str, *, required: bool = False) -> str:
        value = (self.data.get("phone") or "").strip()[:30]
        if value and not PHONE_RE.match(value):
            self.errors["phone"] = t("err.phone", lang)
        elif required and not value:
            self.errors["phone"] = t("err.required", lang)
        return value

    def integer(self, name: str, lang: str, lo: int, hi: int, err_key: str = "err.required") -> int:
        try:
            value = int(self.data.get(name, ""))
        except (TypeError, ValueError):
            value = 0
        if not lo <= value <= hi:
            self.errors[name] = t(err_key, lang)
        return value

    def date_(self, name: str, lang: str) -> date | None:
        raw = (self.data.get(name) or "").strip()
        try:
            return date.fromisoformat(raw)
        except ValueError:
            self.errors[name] = t("err.required", lang)
            return None

    def consent(self, lang: str) -> None:
        if self.data.get("consent") != "1":
            self.errors["consent"] = t("err.consent", lang)

    def contact_required(self, lang: str, email: str, phone: str) -> None:
        if not email and not phone and "email" not in self.errors and "phone" not in self.errors:
            self.errors["phone"] = t("err.contact", lang)

    @property
    def is_spam(self) -> bool:
        return bool((self.data.get("website") or "").strip())  # honeypot

    @property
    def ok(self) -> bool:
        return not self.errors
