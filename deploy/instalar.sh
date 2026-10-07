#!/usr/bin/env bash
# =============================================================================
#  Casa Chute · Café Chute — instalador para VPS Ubuntu / Debian (p. ej. Contabo)
#
#  Uso (como root, desde la carpeta descomprimida del proyecto):
#    bash deploy/instalar.sh                         → la web queda en http://IP-DEL-VPS
#    bash deploy/instalar.sh demo.tudominio.com      → https://demo.tudominio.com (HTTPS automático)
#
#  Opcional: pedir usuario y clave para ver la demo (usuario: cliente)
#    DEMO_CLAVE='una-clave' bash deploy/instalar.sh demo.tudominio.com
#
#  Producción (sin modo demo):
#    DEMO=0 bash deploy/instalar.sh www.cafechute.com
#
#  Se puede volver a ejecutar sin perder datos: conserva .env y la base de datos.
# =============================================================================
set -euo pipefail

DOMINIO="${1:-}"
DEMO_CLAVE="${DEMO_CLAVE:-}"
DEMO="${DEMO:-1}"
APP_DIR=/opt/cafechute
APP_USER=cafechute
APP_PORT="${APP_PORT:-8710}"     # puerto interno (solo 127.0.0.1); cámbialo con APP_PORT=XXXX si está ocupado
FALLBACK_PORT=8088               # si el 80 está ocupado por otro servidor web
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

log()  { printf '\n\033[1;33m==> %s\033[0m\n' "$*"; }
ok()   { printf '\033[1;32m    ✔ %s\033[0m\n' "$*"; }
warn() { printf '\033[1;31m    ! %s\033[0m\n' "$*"; }

[ "$(id -u)" -eq 0 ] || { echo "Ejecuta este script como root (o con sudo)."; exit 1; }
[ -f "$SRC_DIR/wsgi.py" ] || { echo "No encuentro wsgi.py: ejecuta el script desde la carpeta del proyecto."; exit 1; }
. /etc/os-release
echo "Sistema detectado: ${PRETTY_NAME:-desconocido}"
if [ -n "$DOMINIO" ]; then echo "Dominio: $DOMINIO (HTTPS automático)"; else echo "Sin dominio: se servirá por la IP del VPS (HTTP)"; fi

# ----------------------------------------------------------------------------- paquetes
log "Instalando paquetes del sistema"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y -q
apt-get install -y -q python3 python3-venv python3-pip rsync curl gnupg ca-certificates \
  debian-keyring debian-archive-keyring apt-transport-https >/dev/null
python3 -c 'import sys; assert sys.version_info >= (3, 9), "Se necesita Python 3.9 o superior"' \
  || { warn "Python 3.9+ requerido (usa Ubuntu 22.04/24.04 o Debian 12)."; exit 1; }
ok "Python $(python3 -c 'import platform; print(platform.python_version())')"

# ----------------------------------------------------------------------------- código
log "Copiando la aplicación a $APP_DIR"
id -u "$APP_USER" >/dev/null 2>&1 || useradd --system --home-dir "$APP_DIR" --shell /usr/sbin/nologin "$APP_USER"
mkdir -p "$APP_DIR"
if [ "$SRC_DIR" != "$APP_DIR" ]; then
  rsync -a --delete \
    --exclude '.venv/' --exclude 'instance/' --exclude '.env' \
    --exclude '__pycache__/' --exclude '.pytest_cache/' --exclude 'dist/' --exclude 'assets/originals/' \
    "$SRC_DIR"/ "$APP_DIR"/
fi
mkdir -p "$APP_DIR/instance"
ok "Código copiado"

log "Creando el entorno de Python e instalando dependencias"
[ -x "$APP_DIR/.venv/bin/python" ] || python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/pip" install -q --upgrade pip
"$APP_DIR/.venv/bin/pip" install -q -r "$APP_DIR/requirements.txt"
ok "Dependencias instaladas"

# ----------------------------------------------------------------------------- .env
set_env() {  # set_env CLAVE valor  → reemplaza o añade la línea en .env
  local key="$1" value="$2" file="$APP_DIR/.env"
  "$APP_DIR/.venv/bin/python" - "$file" "$key" "$value" <<'PY'
import sys, pathlib
path, key, value = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
out, done = [], False
for line in lines:
    if line.split("=", 1)[0].strip() == key:
        out.append(f"{key}={value}"); done = True
    else:
        out.append(line)
if not done:
    out.append(f"{key}={value}")
path.write_text("\n".join(out) + "\n", encoding="utf-8")
PY
}

log "Configuración (.env)"
if [ ! -f "$APP_DIR/.env" ]; then
  cp "$APP_DIR/.env.example" "$APP_DIR/.env"
  set_env SECRET_KEY "$("$APP_DIR/.venv/bin/python" -c 'import secrets; print(secrets.token_hex(32))')"
  ADMIN_PW="$("$APP_DIR/.venv/bin/python" -c 'import secrets; print(secrets.token_urlsafe(12))')"
  set_env ADMIN_PASSWORD_HASH "$("$APP_DIR/.venv/bin/python" -c 'import sys; from werkzeug.security import generate_password_hash as g; print(g(sys.argv[1]))' "$ADMIN_PW")"
  ok "Creado .env con clave secreta y contraseña del panel"
else
  ok "Se conserva el .env existente"
fi
set_env DEMO_MODE "$DEMO"
if [ -n "$DOMINIO" ]; then
  set_env SITE_URL "https://$DOMINIO"
  set_env FORCE_HTTPS 1
else
  set_env SITE_URL ""
  set_env FORCE_HTTPS 0
fi
if [ -n "$DEMO_CLAVE" ]; then
  set_env DEMO_USER cliente
  set_env DEMO_PASSWORD "$DEMO_CLAVE"
  ok "Demo protegida con usuario 'cliente'"
fi
chown -R "$APP_USER:$APP_USER" "$APP_DIR"
chmod 600 "$APP_DIR/.env"

# ----------------------------------------------------------------------------- servicio
log "Servicio del sistema (Gunicorn)"
if ss -ltn "( sport = :$APP_PORT )" 2>/dev/null | grep -q LISTEN && ! systemctl is-active --quiet cafechute; then
  warn "El puerto interno $APP_PORT ya lo usa otro programa. Elige otro, por ejemplo:"
  warn "  APP_PORT=8720 bash deploy/instalar.sh $DOMINIO"
  exit 1
fi
cat > /etc/systemd/system/cafechute.service <<EOF
[Unit]
Description=Casa Chute · Café Chute (Flask + Gunicorn)
After=network.target

[Service]
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:$APP_PORT --forwarded-allow-ips 127.0.0.1 --access-logfile - wsgi:app
Restart=always
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=true
ReadWritePaths=$APP_DIR/instance

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --quiet cafechute
systemctl restart cafechute
for _ in $(seq 1 20); do
  curl -fsS -o /dev/null "http://127.0.0.1:$APP_PORT/robots.txt" && break
  sleep 1
done
if curl -fsS -o /dev/null "http://127.0.0.1:$APP_PORT/robots.txt"; then ok "La aplicación responde en 127.0.0.1:$APP_PORT"
else warn "La aplicación no responde. Revisa: journalctl -u cafechute -n 50"; exit 1; fi

# ----------------------------------------------------------------------------- servidor web
IP="$(curl -fsS4 --max-time 5 https://ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')"
OCUPADO="$(ss -ltnp 2>/dev/null | grep -E ':(80|443)\s' || true)"
if printf '%s\n' "$OCUPADO" | grep -q '"nginx"'; then
  WEB=nginx
elif [ -n "$OCUPADO" ] && printf '%s\n' "$OCUPADO" | grep -vq '"caddy"'; then
  WEB=caddy-alt   # Apache u otro servidor: Caddy en un puerto alternativo
else
  WEB=caddy
fi
CHECK_PORT=80
CHECK_HOST=""
OPEN_PORTS="80 443"

if [ "$WEB" = "nginx" ]; then
  # ------------------------------------------------------------------ Nginx existente
  log "Servidor web: Nginx (ya instalado; se añade un sitio sin tocar los demás)"
  systemctl disable --now caddy >/dev/null 2>&1 || true
  if [ -n "$DOMINIO" ]; then
    NGX_LISTEN="listen 80;
    listen [::]:80;"
    NGX_NAMES="$DOMINIO"
    [ "${DOMINIO#www.}" != "$DOMINIO" ] && NGX_NAMES="$DOMINIO ${DOMINIO#www.}"
    CHECK_HOST="$DOMINIO"
  else
    NGX_LISTEN="listen $FALLBACK_PORT;
    listen [::]:$FALLBACK_PORT;"
    NGX_NAMES="_"
    CHECK_PORT="$FALLBACK_PORT"
    OPEN_PORTS="$FALLBACK_PORT"
  fi
  cat > /etc/nginx/sites-available/cafechute <<EOF
# Generado por deploy/instalar.sh — Casa Chute
server {
    $NGX_LISTEN
    server_name $NGX_NAMES;
    client_max_body_size 1m;
    gzip on;
    gzip_types text/css application/javascript text/javascript image/svg+xml application/json application/xml;

    location /static/ {
        alias $APP_DIR/app/static/;
        add_header Cache-Control "public, max-age=31536000, immutable";
        access_log off;
    }

    location / {
        proxy_pass http://127.0.0.1:$APP_PORT;
        proxy_set_header Host \$http_host;
        proxy_set_header X-Forwarded-Host \$http_host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
  ln -sf /etc/nginx/sites-available/cafechute /etc/nginx/sites-enabled/cafechute
  nginx -t 2>/dev/null || { nginx -t; warn "La configuración de Nginx tiene errores (ver arriba). No se recargó."; exit 1; }
  systemctl reload nginx
  sleep 2
  ok "Sitio añadido a Nginx"
  if [ -n "$DOMINIO" ]; then
    log "Certificado HTTPS (Let's Encrypt con certbot)"
    apt-get install -y -q certbot python3-certbot-nginx >/dev/null
    CERT_ARGS=(-d "$DOMINIO")
    [ "${DOMINIO#www.}" != "$DOMINIO" ] && CERT_ARGS+=(-d "${DOMINIO#www.}")
    if certbot --nginx "${CERT_ARGS[@]}" --redirect --non-interactive --agree-tos --register-unsafely-without-email; then
      set_env FORCE_HTTPS 1
      URL="https://$DOMINIO"
      ok "HTTPS activo"
    else
      warn "No se pudo emitir el certificado: ¿el DNS de $DOMINIO apunta a $IP? La web queda en http://$DOMINIO"
      set_env FORCE_HTTPS 0
      URL="http://$DOMINIO"
    fi
    systemctl restart cafechute
    sleep 2
  else
    set_env FORCE_HTTPS 0
    systemctl restart cafechute
    sleep 2
    URL="http://$IP:$FALLBACK_PORT"
  fi
else
  # ------------------------------------------------------------------ Caddy
  log "Servidor web (Caddy, con HTTPS automático)"
  if ! command -v caddy >/dev/null 2>&1; then
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --batch --yes --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' -o /etc/apt/sources.list.d/caddy-stable.list
    chmod o+r /usr/share/keyrings/caddy-stable-archive-keyring.gpg /etc/apt/sources.list.d/caddy-stable.list
    apt-get update -y -q && apt-get install -y -q caddy >/dev/null
  fi
  ok "Caddy $(caddy version | awk '{print $1}')"

  SITE_ADDR=":80"
  URL="http://$IP"
  if [ -n "$DOMINIO" ]; then SITE_ADDR="$DOMINIO"; URL="https://$DOMINIO"; CHECK_HOST="$DOMINIO"; fi
  if [ "$WEB" = "caddy-alt" ]; then
    warn "Otro programa usa el puerto 80/443 (¿Apache?). Caddy escuchará en el puerto $FALLBACK_PORT sin HTTPS."
    warn "Para usar el dominio con HTTPS, detén ese servidor (p. ej. systemctl disable --now apache2) y vuelve a ejecutar."
    SITE_ADDR="http://:$FALLBACK_PORT"
    URL="http://$IP:$FALLBACK_PORT"
    CHECK_PORT="$FALLBACK_PORT"
    CHECK_HOST=""
    OPEN_PORTS="$FALLBACK_PORT"
    set_env FORCE_HTTPS 0
    systemctl restart cafechute
  fi

  # Con www.dominio.com, el dominio sin www redirige a él
  APEX_BLOCK=""
  if [ "$SITE_ADDR" = "$DOMINIO" ] && [ "${DOMINIO#www.}" != "$DOMINIO" ]; then
    APEX_BLOCK="${DOMINIO#www.} {
	redir https://$DOMINIO{uri} permanent
}"
  fi

  cat > /etc/caddy/Caddyfile <<EOF
# Generado por deploy/instalar.sh — Casa Chute
$APEX_BLOCK

$SITE_ADDR {
	encode zstd gzip

	# Archivos estáticos servidos directamente por Caddy (más rápido)
	handle_path /static/* {
		root * $APP_DIR/app/static
		header Cache-Control "public, max-age=31536000, immutable"
		file_server
	}

	handle {
		reverse_proxy 127.0.0.1:$APP_PORT
	}

	header -Server
	log {
		output file /var/log/caddy/cafechute.log
	}
}
EOF
  mkdir -p /var/log/caddy && chown -R caddy:caddy /var/log/caddy 2>/dev/null || true
  caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile >/dev/null 2>&1 \
    || { caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile; warn "Caddyfile no válido"; exit 1; }
  systemctl enable --quiet caddy
  systemctl restart caddy
  sleep 3
  ok "Caddy configurado"
fi

# ----------------------------------------------------------------------------- cortafuegos
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active"; then
  for p in $OPEN_PORTS; do ufw allow "$p/tcp" >/dev/null; done
  ok "Puertos abiertos en ufw: $OPEN_PORTS"
fi

# ----------------------------------------------------------------------------- comprobación final
CURL_ARGS=(-fsS -o /dev/null --max-time 10)
[ -n "$CHECK_HOST" ] && CURL_ARGS+=(-H "Host: $CHECK_HOST")
if curl "${CURL_ARGS[@]}" "http://127.0.0.1:$CHECK_PORT/robots.txt"; then
  WEB_OK=1
else
  WEB_OK=0
fi

# ----------------------------------------------------------------------------- resumen
if [ -n "${ADMIN_PW:-}" ]; then   # solo en la primera instalación
  (
    umask 077
    {
      echo "Panel de administración de Casa Chute"
      echo "URL:        $URL/admin"
      echo "Contraseña: $ADMIN_PW"
      echo "Para cambiarla: cd $APP_DIR && .venv/bin/python manage.py hash-password"
      echo "y pega el resultado en ADMIN_PASSWORD_HASH dentro de $APP_DIR/.env (luego: systemctl restart cafechute)"
    } > /root/CREDENCIALES-ADMIN-CASACHUTE.txt
  )
fi

if [ "$WEB_OK" = "1" ]; then
  printf '\n\033[1;32m================  Casa Chute está en línea  ================\033[0m\n'
else
  printf '\n\033[1;31m====  Instalado, pero el servidor web no responde todavía  ====\033[0m\n'
  echo "  Revisa: journalctl -u cafechute -n 30   y   systemctl status ${WEB%-alt}"
fi
echo "  Web:            $URL/es/   ·   $URL/en/"
echo "  Panel:          $URL/admin   (contraseña: cat /root/CREDENCIALES-ADMIN-CASACHUTE.txt)"
[ -n "$DEMO_CLAVE" ] && echo "  Acceso demo:    usuario 'cliente' y la clave que indicaste"
if [ "$DEMO" = "1" ]; then
  echo "  Modo demo:      activo (Google no la indexa). Para producción: DEMO=0 bash deploy/instalar.sh www.cafechute.com"
else
  echo "  Modo demo:      desactivado (producción)"
fi
if [ -n "$DOMINIO" ]; then
  echo "  Nota: el certificado HTTPS requiere que el DNS de $DOMINIO apunte a $IP."
fi
echo "  Logs:           journalctl -u cafechute -f"
echo "  Reiniciar:      systemctl restart cafechute"
