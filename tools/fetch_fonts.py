"""Descarga las fuentes (licencia SIL OFL) para servirlas desde el propio dominio.

Servir las fuentes localmente evita peticiones a terceros (privacidad, CSP estricta)
y elimina una conexión extra en la carga inicial.

Uso:  python tools/fetch_fonts.py
"""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app" / "static" / "fonts"
CSS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Fraunces:ital,opsz,wght@0,9..144,300..800;1,9..144,300..800"
    "&family=Inter:wght@400..700&display=swap"
)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
KEEP_SUBSETS = {"latin", "latin-ext"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    css = fetch(CSS_URL).decode()
    blocks = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S)
    out_css: list[str] = []
    for subset, block in blocks:
        if subset not in KEEP_SUBSETS:
            continue
        family = re.search(r"font-family: '([^']+)'", block).group(1)
        style = re.search(r"font-style: (\w+)", block).group(1)
        url = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
        name = f"{family.lower()}-{style}-{subset}.woff2"
        (OUT / name).write_bytes(fetch(url))
        display = "optional" if family == "Inter" else "swap"  # el texto no se repinta al llegar Inter
        out_css.append(block.replace(url, f"../fonts/{name}").replace("font-display: swap", f"font-display: {display}"))
        print("ok", name)
    fonts_css = ("/* Generado por tools/fetch_fonts.py — Fraunces e Inter (SIL Open Font License) */\n"
                 + "\n".join(out_css) + "\n")
    (ROOT / "app" / "static" / "css" / "fonts.css").write_text(fonts_css, encoding="utf-8")  # usado por el panel
    # app.css lleva las @font-face incrustadas: una petición bloqueante menos en la web pública
    app_css = ROOT / "app" / "static" / "css" / "app.css"
    s = app_css.read_text(encoding="utf-8")
    start = s.index("/* @fonts:start */") + len("/* @fonts:start */\n")
    end = s.index("/* @fonts:end */")
    app_css.write_text(s[:start] + fonts_css + s[end:], encoding="utf-8")


if __name__ == "__main__":
    main()
