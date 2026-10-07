# Casa Chute · Café Chute — nueva web (Python / Flask)

Rediseño completo de cafechute.com a partir de la auditoría de octubre de 2026.
Bilingüe (ES/EN), rápido, seguro, medible y pensado para **convertir**: reservar una
estancia, pedir café o solicitar el Barista Show Tour® en dos clics.

## Arrancar en local

```bash
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python run.py
```

Abre http://127.0.0.1:5000 (redirige a `/es/` o `/en/` según el idioma del navegador).

Pruebas automáticas (49 pruebas: páginas, SEO, seguridad, formularios, precios):

```bash
.venv\Scripts\python -m pytest -q
```

## Qué resuelve de la auditoría

| Problema detectado | Solución en esta web |
|---|---|
| WordPress 5.8 y plugins de 2020–21 sin actualizar | Flask 3 con 3 dependencias, sin plugins de terceros ni panel expuesto |
| Usuario administrador visible (`/wp-json/wp/v2/users`) | No hay usuarios públicos; panel `/admin` con contraseña cifrada, límite de intentos y `noindex` |
| Sin cabeceras de seguridad | CSP estricta (sin scripts ni estilos en línea), HSTS, X-Frame-Options, nosniff, Referrer y Permissions-Policy |
| Casa Chute pesaba **29 MB** (LCP 28 s) | ~0,6 MB: WebP en 5 tamaños con `srcset`, carga diferida, video y mapa solo al hacer clic |
| Sin meta descripciones, sin H1, sin Open Graph | Title y descripción únicos por página e idioma, un H1 por página, Open Graph con imagen propia (1200×630) |
| Sin datos estructurados | Schema.org: `LodgingBusiness`, `HotelRoom`, `Product`, `TouristTrip`, `FAQPage`, `BreadcrumbList` |
| Solo en español | Español e inglés con URLs traducidas y `hreflang` |
| No se podía reservar ni comprar | Calculadora de estancia con tarifas reales + solicitud de reserva, pedido de café y solicitud del tour |
| Teléfono y correo no clicables, sin formulario | `tel:`, `mailto:`, WhatsApp con mensaje prellenado y formularios con validación |
| Enlaces a @chutecasa (no existe) y a cuentas vacías | Enlaces a **@casa.chute** (la cuenta activa) y al Facebook de Casa Chute |
| Sin política de datos (Ley 1581) | Página de política de datos y casilla de autorización con fecha registrada |
| Sin medición | GA4 opcional con banner de consentimiento y evento de clic en WhatsApp |
| Sin favicon, textos con faltas | Favicon y app icons propios; textos corregidos (Escríbenos, Tostión, más…) |
| URLs antiguas | Redirecciones 301 desde `/variedades/`, `/procesos-del-cafe/`, `/donde-comprar/`, `/historia/`, `/casa-chute/`, `/contacto/` |

**Lighthouse (móvil, servidor de producción local):**

| Página | Antes | Ahora |
|---|---|---|
| Home | Rendimiento 76 · SEO 92 · Accesibilidad 96 | Rendimiento ~89 · SEO 100 · Accesibilidad 100 · Buenas prácticas 100 |
| Casa Chute | Rendimiento 60 · LCP 28,1 s · 29 MB | Rendimiento ~87 · LCP ~3,9 s · 0,6 MB |
| Café | — | Rendimiento 95 |
| Escritorio (home / casa) | 93 | 99 / 98 |

## Lo que la hace distinta

- **Semillas de diente de león** (el símbolo de la bolsa de Chute) flotando en el hero, en `<canvas>`.
- **"Mira madurar tu café"**: una lente circular fija cuyo anillo pasa de verde a rojo cereza y a tostado mientras recorres los seis pasos, de la siembra a la taza.
- **"Ahora en la finca"**: hora de Chinchiná, clima real (Open-Meteo, sin clave), amanecer y atardecer, y si la finca está en cosecha.
- **Calendario de cosecha** en anillo con el mes actual marcado.
- **Arcos** en las fotos, como las puertas y ventanas de la casa, y **curvas de nivel** generadas en Python que evocan el mapa de la vereda.
- Todo respeta `prefers-reduced-motion`.

## Estructura

```
app/
  __init__.py      create_app(): compresión, seguridad, rutas, versión de estáticos
  config.py        configuración leída de .env
  content.py       ★ datos del negocio: habitaciones, tarifas, tour, café, FAQ (una sola fuente)
  i18n.py          rutas traducidas, títulos/descripciones SEO y textos ES/EN
  routes.py        páginas, formularios, sitemap, robots, redirecciones 301, /api/finca
  admin.py         panel /admin (solicitudes, estados, exportar CSV)
  services.py      precios, validación, temporada de cosecha, enlaces de WhatsApp
  seo.py           canonical, hreflang, JSON-LD, sitemap
  security.py      CSRF, límite de envíos, cabeceras de seguridad
  live.py          clima en vivo con caché
  art.py           SVG generativo: diente de león, curvas de nivel, anillo de cosecha
  db.py            SQLite (solicitudes)
  templates/       Jinja2
  static/          css, js (sin librerías), fuentes propias, imágenes WebP
tools/
  build_images.py  originales → WebP + manifest + favicons + imágenes Open Graph
  fetch_fonts.py   descarga Fraunces e Inter (licencia OFL) para servirlas localmente
tests/test_app.py
run.py · wsgi.py · manage.py
```

Para cambiar una tarifa, un texto o una foto de habitación basta con editar `app/content.py`:
la web, la calculadora, el panel y Schema.org se actualizan solos.

## Producción / demo en un VPS

Guía paso a paso para un VPS Linux (Contabo + Termius): **[DESPLIEGUE.md](DESPLIEGUE.md)**.

Resumen: sube `cafechute-web.zip` por SFTP, descomprímelo y ejecuta `bash deploy/instalar.sh tu.dominio.com`.
El script instala Python, Gunicorn (servicio systemd) y Caddy (HTTPS automático), genera el `.env` con
clave secreta y contraseña del panel, y activa el modo demo (`noindex`). Para actualizar:
`bash deploy/actualizar.sh`. Para generar el ZIP: `python tools/empaquetar.py`.

Variables nuevas del modo demo (en `.env`): `DEMO_MODE=1` (no indexar), `DEMO_USER` / `DEMO_PASSWORD`
(acceso con clave, opcional). Si `SITE_URL` está vacío, las URL absolutas usan el dominio de cada petición.

## Pendientes que debe confirmar Casa Chute

No se inventó ningún dato. Lo siguiente está **oculto** hasta que se confirme:

- [ ] **Número de RNT** (obligatorio en la publicidad turística) → `RNT_NUMBER` en `.env`.
- [ ] **NIT o cédula** del responsable de datos → `LEGAL_ID`. Revisar la política de datos con un asesor.
- [ ] **Precio de la bolsa de 500 g** → `COFFEE_PRICE_COP` (mientras tanto, "precio por WhatsApp").
- [ ] **Servicios**: wifi, parqueadero, desayuno, mascotas → `AMENITIES` en `content.py` (poner `True`).
- [ ] **Check-in/check-out y política de cancelación** → `POLICIES` en `content.py`.
- [ ] **Fotos de la Habitación del Café 1** (hoy muestra "Fotos próximamente").
- [ ] Verificar que las fotos de cada habitación están bien asignadas (se dedujeron del orden de la web anterior).
- [ ] La Habitación Junior publica "persona adicional $50.000" pero capacidad de 2: confirmar cuál es correcto.
- [ ] Revisar la descripción del Barista Show Tour® (`BARISTA_TOUR` en `content.py`).
- [ ] Actualizar `GOOGLE_RATING` y `GOOGLE_REVIEWS` cuando cambien.
- [ ] Opcional: `GA4_ID` para activar Google Analytics (aparece el banner de cookies).
- [ ] Opcional: correo con dominio propio (p. ej. reservas@cafechute.com) en `BUSINESS["email"]`.

## Regenerar recursos

```bash
.venv\Scripts\python tools\build_images.py   # tras añadir o cambiar fotos en assets/originals
.venv\Scripts\python tools\fetch_fonts.py    # solo si se quieren actualizar las fuentes
```

Las fotos originales (`assets/originals/`, ~40 MB) se descargaron de la web actual de Casa Chute;
úsalas solo con permiso del negocio. No se publican: la web usa las versiones optimizadas de `app/static/img/`.
