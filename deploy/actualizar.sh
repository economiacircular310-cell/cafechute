#!/usr/bin/env bash
# =============================================================================
#  Casa Chute — actualizar una instalación existente con una versión nueva.
#
#  1. Sube el nuevo cafechute-web.zip al VPS y descomprímelo en una carpeta nueva.
#  2. Desde esa carpeta:   bash deploy/actualizar.sh
#
#  Conserva .env, la base de datos (instance/) y el entorno de Python.
# =============================================================================
set -euo pipefail

APP_DIR=/opt/cafechute
APP_USER=cafechute
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_PORT="$(grep -o '127.0.0.1:[0-9]*' /etc/systemd/system/cafechute.service 2>/dev/null | head -1 | cut -d: -f2)"
APP_PORT="${APP_PORT:-8710}"

[ "$(id -u)" -eq 0 ] || { echo "Ejecuta este script como root (o con sudo)."; exit 1; }
[ -d "$APP_DIR/.venv" ] || { echo "No hay instalación en $APP_DIR. Usa primero deploy/instalar.sh"; exit 1; }

echo "==> Copia de seguridad de la base de datos"
mkdir -p /root/backups-cafechute
[ -f "$APP_DIR/instance/cafechute.sqlite3" ] && cp "$APP_DIR/instance/cafechute.sqlite3" "/root/backups-cafechute/cafechute-$(date +%Y%m%d-%H%M%S).sqlite3"

echo "==> Copiando código nuevo"
rsync -a --delete \
  --exclude '.venv/' --exclude 'instance/' --exclude '.env' \
  --exclude '__pycache__/' --exclude '.pytest_cache/' --exclude 'dist/' --exclude 'assets/originals/' \
  "$SRC_DIR"/ "$APP_DIR"/

echo "==> Dependencias"
"$APP_DIR/.venv/bin/pip" install -q -r "$APP_DIR/requirements.txt"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"
chmod 600 "$APP_DIR/.env"

echo "==> Reiniciando"
systemctl restart cafechute
sleep 2
if curl -fsS -o /dev/null "http://127.0.0.1:$APP_PORT/robots.txt"; then
  echo "✔ Actualizado y funcionando."
else
  echo "! La aplicación no responde. Revisa: journalctl -u cafechute -n 50"; exit 1
fi
