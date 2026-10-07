"""Optimiza las fotos originales y genera los recursos gráficos del sitio.

- Convierte cada foto a WebP en varios anchos (srcset) — la antigua página de
  Casa Chute pesaba 29 MB; aquí cada foto pesa entre 20 y 250 KB.
- Escribe app/static/img/manifest.json con dimensiones, color dominante y
  textos alternativos en español e inglés (SEO + accesibilidad).
- Genera el logo recortado, favicons e imágenes Open Graph (1200x630).

Uso:  python tools/build_images.py            (las originales están en assets/originals)
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "originals"
OUT = ROOT / "app" / "static" / "img"
WIDTHS = (480, 800, 1200, 1600, 2400)
QUALITY = 74

# slug, archivo original, alt ES, alt EN, recorte opcional (fracción de alto a conservar desde arriba)
PHOTOS: list[tuple] = [
    # Paisaje y casa
    ("cafetal-ladera", "Artboard-1-20.jpg", "Ladera sembrada de café en la vereda Alto de la Mina, Chinchiná", "Coffee-planted hillside in Alto de la Mina, Chinchiná"),
    ("casa-panoramica", "10-scaled.jpg", "Casa Chute rodeada de montañas en el Paisaje Cultural Cafetero", "Casa Chute surrounded by the mountains of the Coffee Cultural Landscape"),
    ("casa-jardin", "11-scaled.jpg", "Jardín y casa principal de Casa Chute", "Garden and main house at Casa Chute"),
    ("casa-corredor", "12-scaled.jpg", "Corredor con sillas y plantas frente al jardín", "Porch with chairs and plants facing the garden"),
    ("casa-fachada", "02.jpg", "Fachada blanca con balcones rojos de Casa Chute", "White façade with red balconies at Casa Chute"),
    ("casa-exterior", "01.jpg", "Prado, piscina y casa en Casa Chute", "Lawn, pool and house at Casa Chute"),
    ("casa-balcones", "06.jpg", "Casa de dos pisos con balcones y prado", "Two-storey house with balconies and lawn"),
    ("casa-entrada", "07.jpg", "Entrada de la casa con plantas y corredor", "House entrance with plants and porch"),
    ("casa-piscina-casa", "09.jpg", "Vista de la casa y la piscina", "View of the house and the pool"),
    ("piscina", "05.jpg", "Piscina rodeada de baranda de madera", "Pool surrounded by a wooden railing"),
    ("piscina-vista", "WhatsApp-Image-2021-08-04-at-6.39.04-AM-3.jpeg", "Piscina con vista a las montañas de Caldas", "Pool overlooking the mountains of Caldas"),
    ("atardecer", "IMG-20210522-WA0100.jpg", "Atardecer sobre las montañas desde la finca", "Sunset over the mountains from the farm"),
    ("mecedora", "IMG-20210522-WA0098.jpg", "Mecedora en el corredor con vista al verde", "Rocking chair on the porch overlooking the green"),
    ("taza-con-vista", "IMG-20210522-WA0085.jpg", "Huésped tomando café frente al paisaje", "Guest drinking coffee facing the landscape"),
    # Cocina
    ("cocina-comedor", "cocina-02-scaled.jpg", "Cocina y comedor con mesas de madera", "Kitchen and dining room with wooden tables"),
    ("cocina-barra", "cocina-03-scaled.jpg", "Barra de ladrillo y madera en la cocina", "Brick and wood bar in the kitchen"),
    ("cocina-mesa", "cocina-05-scaled.jpg", "Mesa grande de madera para compartir", "Large wooden table for sharing"),
    ("cocina-cafe", "cocina-06-scaled.jpg", "Cocina equipada con bolsas de Café Chute", "Equipped kitchen with bags of Café Chute"),
    ("cocina-amplia", "cocina-01-scaled.jpg", "Cocina amplia con vigas de madera", "Spacious kitchen with wooden beams"),
    # Habitaciones
    ("hab-cafe2-1", "habitacion-02-01.jpg", "Habitación del Café 2 con cama doble y cojines rojos", "Coffee Room 2 with double bed and red cushions"),
    ("hab-cafe2-2", "habitacion-02-02.jpg", "Baño de la Habitación del Café 2", "Bathroom of Coffee Room 2"),
    ("hab-twin-1", "habitacion-03-01.jpg", "Habitación Twin con dos camas sencillas", "Twin room with two single beds"),
    ("hab-twin-2", "habitacion-03-02.jpg", "Escritorio y camas de la Habitación Twin", "Desk and beds in the Twin room"),
    ("hab-twin-3", "habitacion-03-03.jpg", "Baño de la Habitación Twin", "Bathroom of the Twin room"),
    ("hab-accesible-1", "habitacion-04.jpg", "Habitación Accesible con cama doble y camarote", "Accessible room with double bed and bunk bed"),
    ("hab-accesible-2", "habitacion-04-02.jpg", "Vista general de la Habitación Accesible", "Overview of the Accessible room"),
    ("hab-accesible-bano", "banno-habitacion-04-01-scaled.jpg", "Baño accesible con barras de apoyo", "Accessible bathroom with grab bars"),
    ("hab-junior-1", "habitacion-05-01.jpg", "Habitación Junior con cama doble y sofá", "Junior room with double bed and sofa"),
    ("hab-junior-2", "habitacion-05-02.jpg", "Habitación Junior con luz cálida", "Junior room in warm light"),
    ("hab-junior-3", "habitacion-05-03.jpg", "Baño de la Habitación Junior", "Bathroom of the Junior room"),
    ("suite-1", "suite-04-scaled.jpg", "Suite Panorámica con cama doble y sala", "Panoramic Suite with double bed and lounge"),
    ("suite-2", "suite-05-scaled.jpg", "Suite Panorámica con salida al balcón", "Panoramic Suite opening onto the balcony"),
    ("suite-3", "suite-01.jpg", "Cama de la Suite Panorámica", "Bed in the Panoramic Suite"),
    ("suite-balcon", "suite-mirador-04-scaled.jpg", "Balcón de la suite con hamaca y vista", "Suite balcony with hammock and view"),
    ("suite-terraza", "suite-mirador-05-scaled.jpg", "Terraza privada de la suite con comedor", "Private suite terrace with dining set"),
    ("suite-bano", "banno-suite.jpg", "Baño de la Suite Panorámica", "Bathroom of the Panoramic Suite"),
    # Kiosko y mirador
    ("kiosko", "kiosko-05-scaled.jpg", "Kiosko de techo de teja con sillas junto a la piscina", "Tiled-roof kiosk with chairs next to the pool"),
    ("kiosko-interior", "kiosko-01-scaled.jpg", "Interior del kiosko con mesas y vista", "Inside the kiosk with tables and views"),
    ("kiosko-mesas", "kiosko-02-scaled.jpg", "Mesas del kiosko bajo techo de guadua", "Kiosk tables under a bamboo roof"),
    ("kiosko-vista", "kiosko-03-1-scaled.jpg", "Kiosko abierto a las montañas", "Kiosk open to the mountains"),
    ("mirador-1", "mirador-guadua-01-scaled.jpg", "Mirador de guadua con mesa de madera", "Bamboo lookout with wooden table"),
    ("mirador-2", "mirador-guadua-02-scaled.jpg", "Estructura del mirador de guadua", "Structure of the bamboo lookout"),
    ("mirador-3", "mirador-guadua-04-scaled.jpg", "Pasarela de madera del mirador de guadua", "Wooden walkway of the bamboo lookout"),
    ("mirador-4", "mirador-guadua-06-scaled.jpg", "Terraza del mirador con vista al valle", "Lookout terrace overlooking the valley"),
    ("mirador-5", "mirador-guadua-08-scaled.jpg", "Techos de teja del mirador bajo el cielo azul", "Tiled roofs of the lookout under blue sky"),
    # Café y experiencia
    ("barista", "IMG-20210522-WA0099.jpg", "Barista preparando café en Chemex durante el Barista Show Tour", "Barista brewing Chemex coffee during the Barista Show Tour"),
    ("barra-cafe", "IMG-20210522-WA0096.jpg", "Barra de métodos de café frente al paisaje", "Coffee brewing bar facing the landscape"),
    ("cata", "cafe-8.png", "Tazas de cata con granos de café", "Cupping bowls with coffee beans"),
    ("chemex", "cafe-25.png", "Café filtrado en Chemex servido en taza", "Chemex-brewed coffee served in a cup"),
    ("bolsas", "cafe-2.png", "Bolsas de Café Chute junto a una taza", "Bags of Café Chute next to a cup"),
    ("prensa", "cafe-5.png", "Bolsa de Café Chute con prensa francesa y Chemex", "Café Chute bag with French press and Chemex"),
    ("cosecha-manos", "cafe-15.png", "Manos recolectando cerezas maduras de café", "Hands picking ripe coffee cherries"),
    ("tradicion", "gente-1.png", "Caficultor tomando una taza de café", "Coffee grower drinking a cup of coffee"),
    ("taza-montana", "gente-2.png", "Mujer tomando café entre cafetales", "Woman drinking coffee among coffee trees"),
    ("cereza-mano", "Artboard-4-copy-20.jpg", "Racimo de cerezas de café en la mano", "Bunch of coffee cherries in hand"),
    ("taza-humo", "Artboard-4-copy-2-20.jpg", "Taza de café humeante", "Steaming cup of coffee"),
    ("bolsa-chute", "Artboard-4-copy-3-20.jpg", "Bolsa de Café Chute con su diente de león", "Café Chute bag with its dandelion"),
    ("paso-siembra", "Artboard-9-20.jpg", "Cerezas verdes y maduras en la rama", "Green and ripe cherries on the branch", 0.62),
    ("paso-cosecha", "Artboard-42-20.jpg", "Recolector entre los cafetos", "Picker among the coffee trees", 0.62),
    ("paso-despulpado", "Artboard-46-20.jpg", "Costal lleno de cerezas rojas", "Sack full of red cherries", 0.62),
    ("paso-secado", "Artboard-50-20.jpg", "Café secándose al sol", "Coffee drying in the sun", 0.62),
    ("paso-tostion", "Artboard-54-20.jpg", "Granos tostados saliendo de la tostadora", "Roasted beans leaving the roaster", 0.62),
    ("paso-taza", "empaque.jpg", "Empaque de Café Chute con granos", "Café Chute package with beans", 0.62),
]

GRAPHICS = [
    ("variedades", "Artboard-6.png", "Árbol genealógico del café: del tronco etíope a la variedad Bourbon", "Coffee family tree: from the Ethiopian trunk to the Bourbon variety"),
    ("mapa-ubicacion", "location-map.png", "Mapa: Casa Chute en la vereda Alto de la Mina, al occidente de Chinchiná, entre Palestina y Santa Rosa", "Map: Casa Chute in Alto de la Mina, west of Chinchiná, between Palestina and Santa Rosa"),
]

CHERRY = (163, 38, 30)
ESPRESSO = (31, 19, 13)
PARCHMENT = (244, 236, 223)


def dominant_color(im: Image.Image) -> str:
    small = im.convert("RGB").resize((24, 24), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(3))
    r, g, b = small.resize((1, 1), Image.Resampling.BOX).getpixel((0, 0))
    return f"#{r:02x}{g:02x}{b:02x}"


def save_variants(slug: str, im: Image.Image, lossless: bool = False) -> dict:
    im = ImageOps.exif_transpose(im)
    has_alpha = im.mode in ("RGBA", "LA", "P") and lossless
    im = im.convert("RGBA" if has_alpha else "RGB")
    widths = [w for w in WIDTHS if w < im.width] + [min(im.width, WIDTHS[-1])]
    widths = sorted(set(widths))
    files = []
    for w in widths:
        h = round(im.height * w / im.width)
        variant = im.resize((w, h), Image.Resampling.LANCZOS) if w != im.width else im
        name = f"{slug}-{w}.webp"
        if lossless:
            variant.save(OUT / name, "WEBP", quality=90, method=6)
        else:
            variant.save(OUT / name, "WEBP", quality=QUALITY, method=6)
        files.append({"w": w, "file": name, "kb": round((OUT / name).stat().st_size / 1024)})
    return {"w": im.width if im.width <= WIDTHS[-1] else WIDTHS[-1],
            "h": round(im.height * min(im.width, WIDTHS[-1]) / im.width),
            "color": dominant_color(im), "variants": files}


def build_photos(manifest: dict) -> None:
    for entry in PHOTOS + GRAPHICS:
        slug, src, alt_es, alt_en, *rest = entry
        im = Image.open(SRC / src)
        if rest:
            keep = rest[0]
            im = im.crop((0, 0, im.width, int(im.height * keep)))
        lossless = src.endswith(".png") and entry in GRAPHICS
        data = save_variants(slug, im, lossless=lossless)
        data["alt"] = {"es": alt_es, "en": alt_en}
        manifest[slug] = data
        total = sum(v["kb"] for v in data["variants"])
        print(f"{slug:22s} {data['w']}x{data['h']}  {len(data['variants'])} tamaños  {total} KB")


def build_logo() -> None:
    logo = Image.open(SRC / "logo-chute.png").convert("RGBA")
    logo = logo.crop(logo.getbbox())
    logo.thumbnail((900, 900), Image.Resampling.LANCZOS)
    # Silueta blanca: el color real se aplica desde CSS con mask-image.
    alpha = logo.getchannel("A")
    white = Image.new("RGBA", logo.size, (255, 255, 255, 0))
    white.putalpha(alpha)
    white.save(OUT / "logo-chute.png", optimize=True)  # para la imagen OG
    white.save(OUT / "logo-chute.webp", "WEBP", lossless=True, method=6)  # máscara CSS del logo
    print("logo-chute.png", logo.size)


def font(size: int, italic: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        ROOT / "app" / "static" / "fonts" / f"fraunces-{'italic' if italic else 'normal'}-latin.woff2",
        Path("C:/Windows/Fonts/georgiai.ttf" if italic else "C:/Windows/Fonts/georgia.ttf"),
    ]
    for c in candidates:
        try:
            f = ImageFont.truetype(str(c), size)
            try:
                f.set_variation_by_axes([96, 600])  # opsz, wght
            except Exception:
                pass
            return f
        except Exception:
            continue
    return ImageFont.load_default(size)


def draw_dandelion(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float, color, width: int = 2) -> None:
    import math
    n = 22
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        d.line((cx, cy, x2, y2), fill=color, width=width)
        for da in (-0.35, 0, 0.35):
            x3 = x2 + r * 0.22 * math.cos(a + da)
            y3 = y2 + r * 0.22 * math.sin(a + da)
            d.line((x2, y2, x3, y3), fill=color, width=max(1, width - 1))
    d.ellipse((cx - r * 0.12, cy - r * 0.12, cx + r * 0.12, cy + r * 0.12), fill=color)


def build_favicons() -> None:
    for size in (32, 180, 192, 512):
        scale = 4
        S = size * scale
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, S - 1, S - 1), radius=S * 0.22, fill=ESPRESSO + (255,))
        draw_dandelion(d, S / 2, S / 2, S * 0.30, PARCHMENT + (255,), width=max(2, S // 70))
        im = im.resize((size, size), Image.Resampling.LANCZOS)
        name = "favicon-32.png" if size == 32 else f"icon-{size}.png"
        im.save(OUT / name)
    Image.open(OUT / "icon-192.png").save(ROOT / "app" / "static" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("favicons ok")


def build_og(slug: str, src_slug: str, title: str, subtitle: str) -> None:
    W, H = 1200, 630
    base = Image.open(OUT / f"{src_slug}-1600.webp").convert("RGB")
    base = ImageOps.fit(base, (W, H), Image.Resampling.LANCZOS, centering=(0.5, 0.55))
    shade = Image.new("L", (W, H))
    for x in range(W):
        v = int(235 * max(0, 1 - x / (W * 0.85)))
        ImageDraw.Draw(shade).line((x, 0, x, H), fill=v)
    dark = Image.new("RGB", (W, H), ESPRESSO)
    base = Image.composite(dark, base, shade)
    d = ImageDraw.Draw(base)
    logo = Image.open(OUT / "logo-chute.png")
    logo.thumbnail((260, 120))
    base.paste(logo, (72, 64), logo)
    d.text((72, 250), title, font=font(64), fill=PARCHMENT, spacing=6)
    d.text((72, 470), subtitle, font=font(30, italic=True), fill=(217, 164, 65))
    draw_dandelion(d, W - 140, 110, 54, PARCHMENT + (180,), width=2)
    base.save(OUT / f"og-{slug}.jpg", quality=84, optimize=True, progressive=True)
    print("og", slug)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest: dict = {}
    build_photos(manifest)
    build_logo()
    build_favicons()
    build_og("es", "cafetal-ladera", "Despierta donde\nnace tu café.", "Casa Chute · Café Chute — Chinchiná, Caldas")
    build_og("en", "cafetal-ladera", "Wake up where\nyour coffee is born.", "Casa Chute · Café Chute — Chinchiná, Colombia")
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(v["kb"] for m in manifest.values() for v in m["variants"])
    print(f"\n{len(manifest)} imágenes, {total/1024:.1f} MB en total (todas las variantes)")


if __name__ == "__main__":
    main()
