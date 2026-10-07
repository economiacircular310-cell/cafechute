# Montar la demo en el VPS de Contabo (con Termius)

Tiempo estimado: 10 minutos. Probado para Ubuntu 22.04 / 24.04 y Debian 12.

El instalador deja todo listo: Python, la app con Gunicorn como servicio del sistema (arranca sola
si el VPS se reinicia), Caddy como servidor web con **HTTPS automático**, y el **modo demo** activado
(Google no indexa la prueba, así no compite con la web actual de Casa Chute).

---

## 0. ¿Con dominio o solo con la IP?

| Opción | Resultado | Qué necesitas |
|---|---|---|
| **A. Subdominio** (recomendado para presentar) | `https://propuesta.tudominio.com` con candado | Un registro DNS tipo **A** apuntando a la IP del VPS |
| **B. sslip.io** (HTTPS sin comprar dominio) | `https://casachute.123-45-67-89.sslip.io` con candado | Nada: el nombre ya apunta a tu IP |
| **C. Solo IP** | `http://123.45.67.89` (sin candado) | Nada |

Para la opción A, en el panel de DNS de tu dominio crea:

```
Tipo: A    Nombre: propuesta    Valor: IP-DE-TU-VPS    TTL: 300
```

Espera a que resuelva (unos minutos). Puedes comprobarlo en https://dnschecker.org.

Para la opción B, escribe tu IP con guiones: para `169.58.230.60` el nombre es
`casachute.169-58-230-60.sslip.io`.

> No uses `www.cafechute.com` para la demo: es la web actual del cliente.

**¿Tu VPS ya tiene Nginx con otros sitios?** El instalador lo detecta. No instala Caddy ni toca tus
otros sitios: solo añade `/etc/nginx/sites-available/cafechute`. Con dominio o sslip.io pide el
certificado con certbot; sin dominio, la demo queda en `http://IP:8088`.

---

## 1. Subir el ZIP con Termius

1. Abre Termius → tu host del VPS de Contabo → pestaña **SFTP**.
2. Arrastra `cafechute-web.zip` a la carpeta `/root` del servidor.

## 2. Instalar

En Termius abre la **terminal** del VPS y pega:

```bash
apt-get update && apt-get install -y unzip
cd /root && unzip -o cafechute-web.zip -d cafechute-web && cd cafechute-web
```

Luego **una** de estas líneas:

```bash
# Opción A — con subdominio y HTTPS
bash deploy/instalar.sh propuesta.tudominio.com

# Opción B — HTTPS con sslip.io (cambia la IP por la tuya)
bash deploy/instalar.sh casachute.169-58-230-60.sslip.io

# Opción C — solo con la IP
bash deploy/instalar.sh
```

Si quieres que la demo pida usuario y clave (usuario `cliente`), antepón la clave:

```bash
DEMO_CLAVE='cafe2026' bash deploy/instalar.sh propuesta.tudominio.com
```

Al terminar verás la URL de la web y del panel.

## 3. Panel de administración

La contraseña del panel `/admin` se genera sola y se guarda en el VPS:

```bash
cat /root/CREDENCIALES-ADMIN-CASACHUTE.txt
```

Desde el panel se ven las solicitudes de reserva, pedidos de café, tours y mensajes que lleguen
por la web, y se exportan a Excel (CSV).

---

## Comandos útiles

| Para… | Comando |
|---|---|
| Ver si está funcionando | `systemctl status cafechute` |
| Ver los registros en vivo | `journalctl -u cafechute -f` |
| Reiniciar la app | `systemctl restart cafechute` |
| Cambiar la configuración | `nano /opt/cafechute/.env` y luego `systemctl restart cafechute` |
| Actualizar a una versión nueva | Sube el ZIP nuevo, descomprímelo en otra carpeta y ejecuta `bash deploy/actualizar.sh` |
| Copia de la base de datos | `cp /opt/cafechute/instance/cafechute.sqlite3 /root/` |

## Si algo falla

- **El HTTPS no funciona con el dominio**: el DNS aún no apunta al VPS. Comprueba con
  `dig +short propuesta.tudominio.com` (debe salir la IP del VPS) y luego `systemctl restart caddy`.
- **Ya tienes Nginx**: se usa automáticamente (ver arriba). Si `nginx -t` falla por la configuración
  de otro sitio, el instalador no recarga Nginx: corrige ese sitio y vuelve a ejecutarlo.
- **Tienes Apache en el puerto 80**: la demo quedará en `http://IP:8088` con Caddy. Para HTTPS,
  detén Apache (`systemctl disable --now apache2`) y vuelve a ejecutar el instalador.
- **No carga desde fuera**: si activaste un cortafuegos en el panel de Contabo, abre los puertos 80 y 443
  (y 8088 si usas la opción sin dominio).
- **Error 502**: la app no arrancó. Mira `journalctl -u cafechute -n 50`.

---

## Pasar de demo a producción (cuando el cliente apruebe)

1. Apunta el DNS de `cafechute.com` y `www.cafechute.com` (registros A) a la IP del VPS.
2. En `/opt/cafechute/.env` completa `RNT_NUMBER`, `LEGAL_ID`, `COFFEE_PRICE_COP` (ver README → Pendientes)
   y, si la demo tenía clave, vacía `DEMO_USER=` y `DEMO_PASSWORD=`.
3. Ejecuta desde la carpeta del proyecto (conserva datos y contraseña del panel):
   ```bash
   DEMO=0 bash deploy/instalar.sh www.cafechute.com
   ```
   `cafechute.com` redirigirá automáticamente a `https://www.cafechute.com`.
4. Las URL antiguas de WordPress ya redirigen solas a las nuevas (301), sin perder posicionamiento.
5. Da de alta el sitio en Google Search Console y envía `https://www.cafechute.com/sitemap.xml`.
