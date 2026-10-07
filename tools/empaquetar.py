"""Genera dist/cafechute-web.zip listo para subir al servidor.

- Excluye el entorno virtual, las fotos originales, la base de datos local y secretos (.env).
- Normaliza los saltos de línea a LF (los scripts .sh fallan en Linux con CRLF de Windows).
- Marca los .sh como ejecutables dentro del ZIP.

Uso:  python tools/empaquetar.py
"""
from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist" / "cafechute-web.zip"
EXCLUDE_DIRS = {".venv", "__pycache__", ".pytest_cache", "dist", "instance", ".claude", ".git"}
EXCLUDE_PATHS = {"assets/originals"}
EXCLUDE_FILES = {".env", "CREDENCIALES-ADMIN.txt"}
TEXT_EXT = {".py", ".html", ".css", ".js", ".md", ".txt", ".sh", ".json", ".webmanifest", ".xml", ".svg", ".example"}
TEXT_NAMES = {".gitignore", ".gitattributes", "requirements.txt"}


def included(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if any(part in EXCLUDE_DIRS for part in path.relative_to(ROOT).parts):
        return False
    if any(rel == p or rel.startswith(p + "/") for p in EXCLUDE_PATHS):
        return False
    return path.name not in EXCLUDE_FILES and path.suffix != ".pyc"


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)
    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and included(p))
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files:
            rel = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            if path.suffix in TEXT_EXT or path.name in TEXT_NAMES:
                data = data.replace(b"\r\n", b"\n")
            info = zipfile.ZipInfo(rel, date_time=(2026, 10, 7, 12, 0, 0))
            info.create_system = 3  # Unix: conserva los permisos al descomprimir
            info.external_attr = ((0o100755 if path.suffix == ".sh" else 0o100644) << 16)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)
    print(f"{OUT}  ·  {len(files)} archivos  ·  {OUT.stat().st_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
