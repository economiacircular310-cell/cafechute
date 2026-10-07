"""Contenido del negocio: única fuente de verdad para páginas, formularios, Schema.org y precios.

Todo texto visible es un dict {"es": ..., "en": ...}. Los datos marcados con
`confirmed=False` NO se muestran hasta que el negocio los confirme (ver README → Pendientes).
"""
from __future__ import annotations

BUSINESS = {
    "name": "Casa Chute",
    "brand": "Café Chute",
    "tagline": {
        "es": "El empujón que necesitas para empezar y terminar el día.",
        "en": "The boost you need to start and end your day.",
    },
    "phone_display": "+57 310 287 4797",
    "phone_e164": "+573102874797",
    "whatsapp": "573102874797",
    "email": "casachute@gmail.com",
    "street": "Vereda Alto de la Mina",
    "farm": "Finca La Carolina",
    "locality": "Chinchiná",
    "region": "Caldas",
    "country": "CO",
    "country_name": {"es": "Colombia", "en": "Colombia"},
    "lat": 4.9537409,
    "lng": -75.6613846,
    "plus_code": "X83Q+FC Chinchiná, Caldas",
    "google_maps": "https://maps.google.com/?cid=14007078133178930760",
    "directions": "https://www.google.com/maps/dir/?api=1&destination=4.9537409,-75.6613846",
    "instagram": "https://www.instagram.com/casa.chute/",
    "instagram_handle": "@casa.chute",
    "facebook": "https://www.facebook.com/people/Casa-Chute/100075866970748/",
    "youtube_id": "zVsxAX_f-Mo",
    "timezone": "America/Bogota",
    "unesco_year": 2011,
}

# ---------------------------------------------------------------------------
# Habitaciones — tarifas por noche en COP, tal como las publica Casa Chute.
# solo = 1 persona · pair = pareja · extra = persona adicional (None = no aplica)
# ---------------------------------------------------------------------------
ROOMS = [
    {
        "id": "suite",
        "name": {"es": "Suite Panorámica", "en": "Panoramic Suite"},
        "capacity": 3,
        "solo": 300_000, "pair": 350_000, "extra": 50_000,
        "photos": ["suite-1", "suite-balcon", "suite-terraza", "suite-2", "suite-3", "suite-bano"],
        "summary": {
            "es": "La habitación más amplia de la casa: sala, balcón con hamaca y una terraza con comedor frente a las montañas.",
            "en": "The most spacious room in the house: lounge, a balcony with hammock and a terrace with dining set facing the mountains.",
        },
        "features": {
            "es": ["Balcón con hamaca", "Terraza con comedor", "Sala", "Baño privado"],
            "en": ["Balcony with hammock", "Terrace with dining set", "Lounge", "Private bathroom"],
        },
        "featured": True,
    },
    {
        "id": "junior",
        "name": {"es": "Habitación Junior", "en": "Junior Room"},
        "capacity": 2,
        "solo": 180_000, "pair": 250_000, "extra": 50_000,
        "photos": ["hab-junior-1", "hab-junior-2", "hab-junior-3"],
        "summary": {
            "es": "Cama doble, sofá y vigas de madera: luz cálida para descansar después de un día de finca.",
            "en": "Double bed, sofa and wooden beams: warm light to rest after a day on the farm.",
        },
        "features": {"es": ["Cama doble", "Sofá", "Baño privado"], "en": ["Double bed", "Sofa", "Private bathroom"]},
        "featured": True,
    },
    {
        "id": "accesible",
        "name": {"es": "Habitación Accesible", "en": "Accessible Room"},
        "capacity": 3,
        "solo": 180_000, "pair": 250_000, "extra": 50_000,
        "photos": ["hab-accesible-1", "hab-accesible-2", "hab-accesible-bano"],
        "summary": {
            "es": "Pensada para que todos disfruten la finca: baño con barras de apoyo y espacio para moverse con comodidad.",
            "en": "Designed so everyone can enjoy the farm: bathroom with grab bars and room to move around comfortably.",
        },
        "features": {
            "es": ["Baño con barras de apoyo", "Cama doble y camarote", "Hasta 3 huéspedes"],
            "en": ["Bathroom with grab bars", "Double bed and bunk bed", "Up to 3 guests"],
        },
        "featured": False,
    },
    {
        "id": "twin",
        "name": {"es": "Habitación Twin", "en": "Twin Room"},
        "capacity": 2,
        "solo": 180_000, "pair": 250_000, "extra": None,
        "photos": ["hab-twin-1", "hab-twin-2", "hab-twin-3"],
        "summary": {
            "es": "Dos camas sencillas y escritorio: ideal para amigos, hermanos o compañeros de viaje.",
            "en": "Two single beds and a desk: ideal for friends, siblings or travel companions.",
        },
        "features": {"es": ["Dos camas sencillas", "Escritorio", "Baño privado"], "en": ["Two single beds", "Desk", "Private bathroom"]},
        "featured": True,
    },
    {
        "id": "cafe-1",
        "name": {"es": "Habitación del Café 1", "en": "Coffee Room 1"},
        "capacity": 4,
        "solo": 120_000, "pair": 200_000, "extra": 50_000,
        "photos": [],
        "summary": {
            "es": "La más grande para grupos y familias, con la tarifa más económica de la casa.",
            "en": "The largest for groups and families, at the house's most affordable rate.",
        },
        "features": {"es": ["Hasta 4 huéspedes", "Ideal para familias"], "en": ["Up to 4 guests", "Ideal for families"]},
        "featured": False,
    },
    {
        "id": "cafe-2",
        "name": {"es": "Habitación del Café 2", "en": "Coffee Room 2"},
        "capacity": 2,
        "solo": 120_000, "pair": 200_000, "extra": None,
        "photos": ["hab-cafe2-1", "hab-cafe2-2"],
        "summary": {
            "es": "Cama doble con los tonos rojos del café maduro. Sencilla, acogedora y al mejor precio.",
            "en": "A double bed dressed in the reds of ripe coffee. Simple, cosy and best-priced.",
        },
        "features": {"es": ["Cama doble", "Baño privado"], "en": ["Double bed", "Private bathroom"]},
        "featured": False,
    },
]
ROOMS_BY_ID = {r["id"]: r for r in ROOMS}

RATE_NOTE = {
    "es": "Tarifas por noche en pesos colombianos (COP). Sujetas a disponibilidad, temporada y condiciones del servicio. Aplican restricciones.",
    "en": "Nightly rates in Colombian pesos (COP). Subject to availability, season and service conditions. Restrictions apply.",
}

# ---------------------------------------------------------------------------
# Experiencias
# ---------------------------------------------------------------------------
BARISTA_TOUR = {
    "id": "barista-show-tour",
    "name": "Barista Show Tour®",
    "person": 90_000,
    "pair": 170_000,
    "min_people": 4,
    "max_people": 10,
    "min_hours": 4,
    "photos": ["barista", "cata", "chemex", "prensa", "barra-cafe", "taza-montana"],
    "summary": {
        "es": "Una experiencia de al menos cuatro horas alrededor del café de la finca: métodos de preparación, cata y la historia de cada taza.",
        "en": "An experience of at least four hours built around the farm's coffee: brewing methods, cupping and the story behind every cup.",
    },
    "moments": {
        "es": [
            ("El show", "Un barista prepara el café de la finca en Chemex, prensa francesa y otros métodos, frente al paisaje."),
            ("La cata", "Aprende a reconocer las notas de cacao, panela y fruta amarilla de nuestro Bourbon."),
            ("La historia", "Del cafetal a la taza: cómo se cultiva, se cosecha y se seca el café que estás tomando."),
        ],
        "en": [
            ("The show", "A barista brews the farm's coffee with Chemex, French press and other methods, facing the landscape."),
            ("The cupping", "Learn to recognise the cocoa, panela and yellow-fruit notes of our Bourbon."),
            ("The story", "From field to cup: how the coffee you're drinking is grown, picked and dried."),
        ],
    },
}

# ---------------------------------------------------------------------------
# Espacios y comodidades
# ---------------------------------------------------------------------------
SPACES = [
    {"id": "exteriores", "name": {"es": "La casa y sus jardines", "en": "The house and gardens"},
     "photos": ["casa-panoramica", "casa-jardin", "casa-fachada", "casa-corredor", "casa-entrada", "casa-balcones"]},
    {"id": "piscina", "name": {"es": "Piscina", "en": "Pool"},
     "photos": ["piscina-vista", "piscina", "casa-exterior", "casa-piscina-casa"]},
    {"id": "kiosko", "name": {"es": "Kiosko", "en": "Kiosk"},
     "photos": ["kiosko", "kiosko-interior", "kiosko-vista", "kiosko-mesas"]},
    {"id": "mirador", "name": {"es": "Mirador de guadua", "en": "Bamboo lookout"},
     "photos": ["mirador-4", "mirador-1", "mirador-3", "mirador-2", "mirador-5"]},
    {"id": "cocina", "name": {"es": "Cocina y comedor", "en": "Kitchen and dining room"},
     "photos": ["cocina-mesa", "cocina-comedor", "cocina-barra", "cocina-cafe", "cocina-amplia"]},
    {"id": "paisaje", "name": {"es": "El paisaje", "en": "The landscape"},
     "photos": ["atardecer", "taza-con-vista", "mecedora", "cafetal-ladera"]},
]

AMENITIES = [
    # icon, texto, confirmado (visible)
    ("pool", {"es": "Piscina", "en": "Swimming pool"}, True),
    ("kiosk", {"es": "Kiosko con vista", "en": "Kiosk with a view"}, True),
    ("bamboo", {"es": "Mirador de guadua", "en": "Bamboo lookout"}, True),
    ("kitchen", {"es": "Cocina y comedor", "en": "Kitchen and dining room"}, True),
    ("garden", {"es": "Jardines y prado", "en": "Gardens and lawn"}, True),
    ("access", {"es": "Habitación accesible", "en": "Accessible room"}, True),
    ("hammock", {"es": "Balcón con hamaca (suite)", "en": "Balcony with hammock (suite)"}, True),
    ("coffee", {"es": "Café de la finca", "en": "Farm-grown coffee"}, True),
    # Pendientes de confirmar con Casa Chute antes de publicarlos:
    ("wifi", {"es": "Wi-Fi", "en": "Wi-Fi"}, False),
    ("parking", {"es": "Parqueadero", "en": "Parking"}, False),
    ("breakfast", {"es": "Desayuno incluido", "en": "Breakfast included"}, False),
    ("pets", {"es": "Se admiten mascotas", "en": "Pets welcome"}, False),
]

POLICIES = [
    ({"es": "Tarifas", "en": "Rates"}, RATE_NOTE, True),
    ({"es": "Barista Show Tour®", "en": "Barista Show Tour®"},
     {"es": "Grupo mínimo de 4 personas (máximo 10) y duración mínima de 4 horas.",
      "en": "Minimum group of 4 people (maximum 10) and a minimum duration of 4 hours."}, True),
    ({"es": "Reservas", "en": "Bookings"},
     {"es": "Tu solicitud no es una reserva confirmada: te respondemos por WhatsApp o correo con disponibilidad y forma de pago.",
      "en": "Your request is not a confirmed booking: we reply by WhatsApp or email with availability and payment details."}, True),
    # Pendientes de confirmar:
    ({"es": "Check-in / check-out", "en": "Check-in / check-out"}, {"es": "", "en": ""}, False),
    ({"es": "Cancelación", "en": "Cancellation"}, {"es": "", "en": ""}, False),
    ({"es": "Mascotas", "en": "Pets"}, {"es": "", "en": ""}, False),
]

# ---------------------------------------------------------------------------
# Café
# ---------------------------------------------------------------------------
COFFEE = {
    "name": "Café Chute · Bourbon",
    "weight_g": 500,
    "formats": [("grano", {"es": "En grano", "en": "Whole bean"}), ("molido", {"es": "Molido", "en": "Ground"})],
    "variety": "Bourbon",
    "trees": 2000,
    "spacing": "3 × 2 m",
    "notes": [
        {"id": "cacao", "name": {"es": "Cacao recién tostado", "en": "Freshly roasted cocoa"}, "color": "#5a3423"},
        {"id": "panela", "name": {"es": "Panela", "en": "Panela (raw cane sugar)"}, "color": "#b5762c"},
        {"id": "fruta", "name": {"es": "Fruta amarilla", "en": "Yellow fruit"}, "color": "#e3b23c"},
    ],
    "harvest_months": [4, 5, 8, 9, 10],
    "drying_days": (10, 25),
    "pickers": 4,
}

PROCESS = [
    {"id": "siembra", "photo": "paso-siembra", "stage": 0,
     "title": {"es": "Siembra", "en": "Planting"},
     "text": {"es": "Solo 2.000 cafetos de Bourbon, sembrados a 3 por 2 metros. Pocos, para poder cuidarlos uno a uno.",
              "en": "Just 2,000 Bourbon trees, planted 3 by 2 metres apart. Few enough to care for each one."}},
    {"id": "cosecha", "photo": "cosecha-manos", "stage": 1,
     "title": {"es": "Cosecha", "en": "Harvest"},
     "text": {"es": "De abril a mayo y de agosto a octubre, cuatro recolectores escogen a mano solo los granos más maduros.",
              "en": "From April to May and August to October, four pickers hand-select only the ripest cherries."}},
    {"id": "despulpado", "photo": "paso-despulpado", "stage": 2,
     "title": {"es": "Despulpado", "en": "Pulping"},
     "text": {"es": "La tolva y la despulpadora separan la cáscara; el grano queda con su mucílago para fermentar.",
              "en": "The hopper and pulper remove the skin; the bean keeps its mucilage to ferment."}},
    {"id": "secado", "photo": "paso-secado", "stage": 3,
     "title": {"es": "Secado al sol", "en": "Sun drying"},
     "text": {"es": "Al sol, revolviendo al menos cuatro veces al día. Lento y gradual: de 10 a 25 días según el clima.",
              "en": "In the sun, turned at least four times a day. Slow and gradual: 10 to 25 days depending on the weather."}},
    {"id": "tostion", "photo": "paso-tostion", "stage": 4,
     "title": {"es": "Tostión", "en": "Roasting"},
     "text": {"es": "Un tostador aliado de la región tuesta y empaca nuestro café para resaltar sus notas.",
              "en": "A partner roaster from the region roasts and packs our coffee to bring out its notes."}},
    {"id": "taza", "photo": "bolsas", "stage": 5,
     "title": {"es": "Tu taza", "en": "Your cup"},
     "text": {"es": "Bolsa de 500 g, en grano o molido. Cacao recién tostado, panela y fruta amarilla.",
              "en": "500 g bag, whole bean or ground. Freshly roasted cocoa, panela and yellow fruit."}},
]

WHERE_TO_BUY = [
    {"name": "Café al Parque",
     "desc": {"es": "Tienda de café de la asociación Comitur, con café de productores locales. ¡Y por supuesto tu Chute!",
              "en": "The Comitur association's coffee shop, stocking local growers' coffee — and, of course, your Chute!"},
     "address": "Cra. 8 #10-40, Chinchiná, Caldas",
     "maps": "https://www.google.com/maps/search/?api=1&query=Caf%C3%A9+Al+Parque+Cra.+8+%2310-40+Chinchin%C3%A1"},
]

# ---------------------------------------------------------------------------
# Preguntas frecuentes (solo con información confirmada)
# ---------------------------------------------------------------------------
FAQ = [
    ({"es": "¿Dónde queda Casa Chute?", "en": "Where is Casa Chute?"},
     {"es": "En la vereda Alto de la Mina, al occidente de Chinchiná (Caldas), en pleno Paisaje Cultural Cafetero. Desde Chinchiná se sube por la vía hacia La Quiebra – Naranjal. Te enviamos la ubicación exacta por WhatsApp al reservar.",
      "en": "In Alto de la Mina, west of Chinchiná (Caldas), right in the Coffee Cultural Landscape. From Chinchiná, take the road towards La Quiebra – Naranjal. We send you the exact location by WhatsApp when you book."}),
    ({"es": "¿Cómo reservo?", "en": "How do I book?"},
     {"es": "Calcula tu estancia y envíanos la solicitud desde la web o por WhatsApp. Te confirmamos disponibilidad y forma de pago.",
      "en": "Estimate your stay and send us the request from the website or by WhatsApp. We confirm availability and payment details."}),
    ({"es": "¿Las tarifas incluyen a dos personas?", "en": "Do the rates cover two people?"},
     {"es": "Cada habitación tiene tarifa para una persona y para pareja. En las que lo permiten, cada persona adicional suma $50.000 por noche.",
      "en": "Each room has a single and a couple rate. Where allowed, each additional guest adds COP 50,000 per night."}),
    ({"es": "¿Hay habitación para personas con movilidad reducida?", "en": "Is there a room for guests with reduced mobility?"},
     {"es": "Sí, la Habitación Accesible tiene baño con barras de apoyo y capacidad para tres huéspedes.",
      "en": "Yes, the Accessible Room has a bathroom with grab bars and sleeps three."}),
    ({"es": "¿Qué es el Barista Show Tour®?", "en": "What is the Barista Show Tour®?"},
     {"es": "Nuestra experiencia de café de al menos cuatro horas, para grupos de 4 a 10 personas: $90.000 por persona o $170.000 por pareja.",
      "en": "Our coffee experience of at least four hours, for groups of 4 to 10 people: COP 90,000 per person or COP 170,000 per couple."}),
    ({"es": "¿Puedo comprar el café de la finca?", "en": "Can I buy the farm's coffee?"},
     {"es": "Sí: pídelo desde la web o por WhatsApp, o encuéntralo en la tienda Café al Parque de Chinchiná.",
      "en": "Yes: order it on the website or by WhatsApp, or find it at the Café al Parque shop in Chinchiná."}),
    ({"es": "¿Cuándo es la cosecha?", "en": "When is harvest season?"},
     {"es": "De abril a mayo y de agosto a octubre. En esas fechas la finca está en plena actividad.",
      "en": "April to May and August to October. During those months the farm is in full swing."}),
]
