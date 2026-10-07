""""Ahora en la finca": hora local, clima en vivo (Open-Meteo, sin clave) y temporada de cosecha.

El clima se pide desde el servidor y se guarda en caché 20 minutos; si el servicio
falla, la web sigue funcionando y simplemente no muestra el dato.
"""
from __future__ import annotations

import json
import threading
import time
import urllib.request
from datetime import datetime

from .content import BUSINESS
from .services import TZ, harvest_status

_CACHE: dict = {"at": 0.0, "data": None}
_LOCK = threading.Lock()
TTL = 20 * 60

API = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}"
    "&current=temperature_2m,weather_code,is_day&daily=sunrise,sunset"
    "&timezone=America%2FBogota&forecast_days=1"
)

# Códigos WMO -> (icono, es, en)
WMO = {
    0: ("sun", "Despejado", "Clear sky"),
    1: ("sun", "Mayormente despejado", "Mostly clear"),
    2: ("cloud-sun", "Parcialmente nublado", "Partly cloudy"),
    3: ("cloud", "Nublado", "Overcast"),
    45: ("fog", "Neblina", "Fog"), 48: ("fog", "Neblina", "Fog"),
    51: ("rain", "Llovizna", "Drizzle"), 53: ("rain", "Llovizna", "Drizzle"), 55: ("rain", "Llovizna", "Drizzle"),
    61: ("rain", "Lluvia ligera", "Light rain"), 63: ("rain", "Lluvia", "Rain"), 65: ("rain", "Lluvia fuerte", "Heavy rain"),
    80: ("rain", "Chubascos", "Showers"), 81: ("rain", "Chubascos", "Showers"), 82: ("rain", "Aguacero", "Downpour"),
    95: ("storm", "Tormenta", "Thunderstorm"), 96: ("storm", "Tormenta", "Thunderstorm"), 99: ("storm", "Tormenta", "Thunderstorm"),
}


def _fetch_weather() -> dict | None:
    url = API.format(lat=BUSINESS["lat"], lng=BUSINESS["lng"])
    req = urllib.request.Request(url, headers={"User-Agent": "cafechute-web/1.0"})
    with urllib.request.urlopen(req, timeout=3) as resp:
        raw = json.loads(resp.read())
    cur = raw["current"]
    code = int(cur.get("weather_code", 3))
    icon, es, en = WMO.get(code, ("cloud", "Variable", "Variable"))
    if icon == "sun" and not cur.get("is_day", 1):
        icon = "moon"
    return {
        "temp": round(cur["temperature_2m"]),
        "icon": icon,
        "desc": {"es": es, "en": en},
        "sunrise": raw["daily"]["sunrise"][0][-5:],
        "sunset": raw["daily"]["sunset"][0][-5:],
    }


def weather(enabled: bool = True) -> dict | None:
    if not enabled:
        return None
    with _LOCK:
        if _CACHE["data"] is not None and time.time() - _CACHE["at"] < TTL:
            return _CACHE["data"]
    try:
        data = _fetch_weather()
    except Exception:
        data = _CACHE["data"]  # último dato bueno, o None
    with _LOCK:
        _CACHE.update(at=time.time(), data=data)
    return data


def snapshot(lang: str, weather_enabled: bool = True) -> dict:
    now = datetime.now(TZ)
    w = weather(weather_enabled)
    return {
        "time": now.strftime("%H:%M"),
        "iso": now.isoformat(timespec="minutes"),
        "harvest": harvest_status(lang, now.date()),
        "weather": {**w, "desc": w["desc"][lang]} if w else None,
    }
