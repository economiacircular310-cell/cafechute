"""Acceso al manifiesto de imágenes generado por tools/build_images.py."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

MANIFEST = Path(__file__).resolve().parent / "static" / "img" / "manifest.json"


@lru_cache(maxsize=1)
def manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def image(slug: str) -> dict | None:
    return manifest().get(slug)


def srcset(slug: str, static_url) -> str:
    img = image(slug)
    if not img:
        return ""
    return ", ".join(f"{static_url('img/' + v['file'])} {v['w']}w" for v in img["variants"])


def best(slug: str, target: int = 960) -> str | None:
    img = image(slug)
    if not img:
        return None
    variants = img["variants"]
    for v in variants:
        if v["w"] >= target:
            return v["file"]
    return variants[-1]["file"]
