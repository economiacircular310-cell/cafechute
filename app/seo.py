"""SEO técnico: URLs canónicas, hreflang, datos estructurados Schema.org y sitemap."""
from __future__ import annotations

import json
from datetime import date

from flask import current_app, has_request_context, request, url_for

from .content import AMENITIES, BARISTA_TOUR, BUSINESS, COFFEE, FAQ, ROOMS
from .i18n import INDEXABLE, LANGS, META, SLUGS, tr
from .images import best


def page_path(key: str, lang: str) -> str:
    slug = SLUGS[key][lang]
    return f"/{lang}/" + (f"{slug}/" if slug else "")


def abs_url(path: str) -> str:
    base = current_app.config.get("SITE_URL") or (request.host_url.rstrip("/") if has_request_context() else "")
    return base + path


def alternates(key: str) -> list[tuple[str, str]]:
    alts = [(lang, abs_url(page_path(key, lang))) for lang in LANGS]
    alts.append(("x-default", abs_url(page_path(key, "es"))))
    return alts


def img_url(slug: str, width: int = 1600) -> str:
    return abs_url(url_for("static", filename="img/" + (best(slug, width) or "og-es.jpg")))


def _address() -> dict:
    return {
        "@type": "PostalAddress",
        "streetAddress": BUSINESS["street"],
        "addressLocality": BUSINESS["locality"],
        "addressRegion": BUSINESS["region"],
        "addressCountry": BUSINESS["country"],
    }


def _org(lang: str) -> dict:
    return {
        "@type": "Organization",
        "@id": abs_url("/#org"),
        "name": BUSINESS["name"],
        "alternateName": BUSINESS["brand"],
        "url": abs_url(page_path("home", lang)),
        "logo": abs_url(url_for("static", filename="img/icon-512.png")),
        "email": BUSINESS["email"],
        "telephone": BUSINESS["phone_e164"],
        "sameAs": [BUSINESS["instagram"], BUSINESS["facebook"]],
        "address": _address(),
    }


def _breadcrumb(key: str, lang: str) -> dict:
    items = [{"@type": "ListItem", "position": 1, "name": "Casa Chute", "item": abs_url(page_path("home", lang))}]
    if key != "home":
        items.append({"@type": "ListItem", "position": 2, "name": META[key][lang][0].split(" · ")[0],
                      "item": abs_url(page_path(key, lang))})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def _lodging(lang: str) -> dict:
    prices = [r["solo"] for r in ROOMS] + [r["pair"] for r in ROOMS]
    return {
        "@type": "LodgingBusiness",
        "@id": abs_url("/#lodging"),
        "name": BUSINESS["name"],
        "description": META["casa"][lang][1],
        "url": abs_url(page_path("casa", lang)),
        "image": [img_url(s) for s in ("casa-panoramica", "piscina-vista", "suite-1", "kiosko")],
        "telephone": BUSINESS["phone_e164"],
        "email": BUSINESS["email"],
        "address": _address(),
        "geo": {"@type": "GeoCoordinates", "latitude": BUSINESS["lat"], "longitude": BUSINESS["lng"]},
        "hasMap": BUSINESS["google_maps"],
        "priceRange": f"COP {min(prices):,} – {max(prices):,}".replace(",", "."),
        "currenciesAccepted": "COP",
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": tr(label, lang), "value": True}
            for _icon, label, confirmed in AMENITIES if confirmed
        ],
        "containsPlace": [
            {"@type": "HotelRoom", "name": tr(r["name"], lang),
             "occupancy": {"@type": "QuantitativeValue", "maxValue": r["capacity"]}}
            for r in ROOMS
        ],
        "parentOrganization": {"@id": abs_url("/#org")},
    }


def _product(lang: str) -> dict:
    data = {
        "@type": "Product",
        "name": COFFEE["name"],
        "brand": {"@type": "Brand", "name": BUSINESS["brand"]},
        "description": META["cafe"][lang][1],
        "image": [img_url(s) for s in ("bolsas", "prensa", "bolsa-chute")],
        "weight": {"@type": "QuantitativeValue", "value": COFFEE["weight_g"], "unitCode": "GRM"},
        "countryOfOrigin": {"@type": "Country", "name": "Colombia"},
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Variedad" if lang == "es" else "Variety", "value": COFFEE["variety"]},
            {"@type": "PropertyValue", "name": "Notas" if lang == "es" else "Notes",
             "value": ", ".join(tr(n["name"], lang) for n in COFFEE["notes"])},
        ],
    }
    price = current_app.config.get("COFFEE_PRICE_COP")
    if price:
        data["offers"] = {"@type": "Offer", "price": price, "priceCurrency": "COP",
                          "availability": "https://schema.org/InStock",
                          "url": abs_url(page_path("cafe", lang))}
    return data


def _tour(lang: str) -> dict:
    return {
        "@type": "TouristTrip",
        "name": BARISTA_TOUR["name"],
        "description": tr(BARISTA_TOUR["summary"], lang),
        "provider": {"@id": abs_url("/#org")},
        "image": [img_url("barista")],
        "offers": [
            {"@type": "Offer", "price": BARISTA_TOUR["person"], "priceCurrency": "COP",
             "description": "Por persona" if lang == "es" else "Per person"},
            {"@type": "Offer", "price": BARISTA_TOUR["pair"], "priceCurrency": "COP",
             "description": "Por pareja" if lang == "es" else "Per couple"},
        ],
    }


def _faq(lang: str) -> dict:
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": tr(q, lang),
             "acceptedAnswer": {"@type": "Answer", "text": tr(a, lang)}}
            for q, a in FAQ
        ],
    }


def json_ld(key: str, lang: str) -> str:
    graph: list[dict] = [_org(lang), _breadcrumb(key, lang)]
    if key == "home":
        graph.append({"@type": "WebSite", "@id": abs_url("/#web"), "name": "Casa Chute · Café Chute",
                      "url": abs_url(page_path("home", lang)), "inLanguage": lang,
                      "publisher": {"@id": abs_url("/#org")}})
        graph.append(_lodging(lang))
    elif key in ("casa", "reservar"):
        graph.append(_lodging(lang))
        if key == "casa":
            graph.append(_faq(lang))
    elif key == "cafe":
        graph.append(_product(lang))
    elif key == "experiencias":
        graph.append(_tour(lang))
    payload = {"@context": "https://schema.org", "@graph": graph}
    # Escapar "<" impide cerrar el <script> desde los datos
    return json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")


def sitemap_xml() -> str:
    today = date.today().isoformat()
    rows = []
    for key in INDEXABLE:
        alts = alternates(key)
        for lang in LANGS:
            links = "".join(f'<xhtml:link rel="alternate" hreflang="{hl}" href="{href}"/>' for hl, href in alts)
            prio = "1.0" if key == "home" else "0.8" if key in ("casa", "cafe", "reservar") else "0.5"
            rows.append(f"<url><loc>{abs_url(page_path(key, lang))}</loc>{links}<lastmod>{today}</lastmod><priority>{prio}</priority></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
            + "".join(rows) + "</urlset>")
