"""Idiomas, rutas traducidas, metadatos SEO por página y textos de interfaz."""
from __future__ import annotations

LANGS = ("es", "en")
DEFAULT_LANG = "es"

# Clave de página -> slug por idioma. Slugs traducidos = mejor SEO en cada idioma.
SLUGS = {
    "home": {"es": "", "en": ""},
    "casa": {"es": "casa-chute", "en": "casa-chute"},
    "cafe": {"es": "cafe", "en": "coffee"},
    "experiencias": {"es": "experiencias", "en": "experiences"},
    "historia": {"es": "historia", "en": "our-story"},
    "contacto": {"es": "contacto", "en": "contact"},
    "reservar": {"es": "reservar", "en": "book"},
    "privacidad": {"es": "privacidad", "en": "privacy"},
    "gracias": {"es": "gracias", "en": "thank-you"},
}

# Páginas que aparecen en el sitemap (gracias no se indexa)
INDEXABLE = ("home", "casa", "cafe", "experiencias", "historia", "contacto", "reservar", "privacidad")

META = {
    "home": {
        "es": ("Casa Chute · Finca cafetera y café de origen en Chinchiná, Caldas",
               "Despierta donde nace tu café: hospédate en una finca cafetera familiar del Paisaje Cultural Cafetero y prueba nuestro café Bourbon cultivado a mano."),
        "en": ("Casa Chute · Coffee farm stay & single-origin coffee in Chinchiná, Colombia",
               "Wake up where your coffee is born: stay at a family coffee farm in Colombia's Coffee Cultural Landscape and taste our hand-picked Bourbon."),
    },
    "casa": {
        "es": ("Casa Chute · Alojamiento rural y finca cafetera en Chinchiná",
               "Seis habitaciones con vista a las montañas de Caldas desde $120.000 COP por noche, piscina, kiosko, mirador de guadua y Barista Show Tour®."),
        "en": ("Casa Chute · Rural coffee farm stay in Chinchiná, Caldas",
               "Six rooms overlooking the mountains of Caldas from COP 120,000 per night, with pool, kiosk, bamboo lookout and the Barista Show Tour®."),
    },
    "cafe": {
        "es": ("Café Chute · Café Bourbon de Chinchiná con notas a cacao y panela",
               "Nuestro Bourbon de la Finca La Carolina: notas a cacao recién tostado, panela y fruta amarilla. Bolsa de 500 g en grano o molido."),
        "en": ("Café Chute · Bourbon coffee from Chinchiná with cocoa & panela notes",
               "Our Bourbon from Finca La Carolina: notes of freshly roasted cocoa, panela and yellow fruit. 500 g bag, whole bean or ground."),
    },
    "experiencias": {
        "es": ("Barista Show Tour® y experiencias de café en Chinchiná · Casa Chute",
               "Vive el café de la finca con el Barista Show Tour®: métodos de preparación, cata y paisaje. Grupos de 4 a 10 personas."),
        "en": ("Barista Show Tour® & coffee experiences in Chinchiná · Casa Chute",
               "Experience the farm's coffee with the Barista Show Tour®: brewing methods, cupping and landscape. Groups of 4 to 10 people."),
    },
    "historia": {
        "es": ("Del cultivo a la taza: la historia de Café Chute",
               "De la herencia de los abuelos caficultores nace Café Chute: 2.000 cafetos de Bourbon, cosecha a mano y secado al sol en Chinchiná."),
        "en": ("From field to cup: the story of Café Chute",
               "Born from our coffee-growing grandparents' legacy: 2,000 Bourbon trees, hand-picked and sun-dried in Chinchiná."),
    },
    "contacto": {
        "es": ("Contacto · Casa Chute y Café Chute",
               "Escríbenos por WhatsApp al +57 310 287 4797, por correo o con el formulario. Vereda Alto de la Mina, Chinchiná, Caldas."),
        "en": ("Contact · Casa Chute & Café Chute",
               "Message us on WhatsApp at +57 310 287 4797, by email or with the form. Alto de la Mina, Chinchiná, Caldas, Colombia."),
    },
    "reservar": {
        "es": ("Reserva tu estancia en Casa Chute",
               "Calcula el valor de tu estancia al instante y envía tu solicitud de reserva. Te confirmamos disponibilidad por WhatsApp."),
        "en": ("Book your stay at Casa Chute",
               "Get an instant estimate for your stay and send your booking request. We confirm availability by WhatsApp."),
    },
    "privacidad": {
        "es": ("Política de tratamiento de datos personales · Casa Chute",
               "Cómo tratamos tus datos personales conforme a la Ley 1581 de 2012."),
        "en": ("Privacy policy · Casa Chute",
               "How we handle your personal data under Colombian Law 1581 of 2012."),
    },
    "gracias": {
        "es": ("¡Gracias! · Casa Chute", "Recibimos tu solicitud."),
        "en": ("Thank you! · Casa Chute", "We received your request."),
    },
}

STRINGS: dict[str, dict[str, str]] = {
    # Navegación
    "nav.casa": {"es": "Hospédate", "en": "Stay"},
    "nav.cafe": {"es": "Nuestro café", "en": "Our coffee"},
    "nav.experiencias": {"es": "Experiencias", "en": "Experiences"},
    "nav.historia": {"es": "Historia", "en": "Our story"},
    "nav.contacto": {"es": "Contacto", "en": "Contact"},
    "nav.reservar": {"es": "Reservar", "en": "Book now"},
    "nav.menu": {"es": "Menú", "en": "Menu"},
    "nav.close": {"es": "Cerrar", "en": "Close"},
    "nav.skip": {"es": "Saltar al contenido", "en": "Skip to content"},
    "nav.lang": {"es": "English", "en": "Español"},
    "nav.lang_short": {"es": "EN", "en": "ES"},
    "nav.home": {"es": "Inicio", "en": "Home"},
    # Comunes
    "cta.book": {"es": "Reserva tu estancia", "en": "Book your stay"},
    "cta.coffee": {"es": "Prueba nuestro café", "en": "Taste our coffee"},
    "cta.whatsapp": {"es": "Escríbenos por WhatsApp", "en": "Message us on WhatsApp"},
    "cta.whatsapp_short": {"es": "WhatsApp", "en": "WhatsApp"},
    "cta.see_rooms": {"es": "Ver habitaciones", "en": "See rooms"},
    "cta.directions": {"es": "Cómo llegar", "en": "Get directions"},
    "cta.more": {"es": "Ver más", "en": "See more"},
    "cta.reviews": {"es": "Leer opiniones en Google", "en": "Read Google reviews"},
    "cta.follow": {"es": "Síguenos en Instagram", "en": "Follow us on Instagram"},
    "cta.book_room": {"es": "Reservar esta habitación", "en": "Book this room"},
    "cta.request_tour": {"es": "Solicitar el tour", "en": "Request the tour"},
    "cta.order": {"es": "Hacer pedido", "en": "Place order"},
    "cta.send": {"es": "Enviar mensaje", "en": "Send message"},
    "cta.send_request": {"es": "Enviar solicitud", "en": "Send request"},
    "cta.via_whatsapp": {"es": "O envíala por WhatsApp", "en": "Or send it via WhatsApp"},
    "cta.play_video": {"es": "Ver video de Casa Chute", "en": "Watch the Casa Chute video"},
    "cta.load_map": {"es": "Cargar mapa interactivo", "en": "Load interactive map"},
    "cta.back_home": {"es": "Volver al inicio", "en": "Back to home"},
    "wa.default": {"es": "Hola, Casa Chute. Quiero más información.", "en": "Hi Casa Chute! I'd like more information."},
    "wa.coffee": {"es": "Hola, Casa Chute. Quiero pedir Café Chute.", "en": "Hi Casa Chute! I'd like to order Café Chute."},
    "wa.tour": {"es": "Hola, Casa Chute. Quiero información del Barista Show Tour®.", "en": "Hi Casa Chute! I'd like information about the Barista Show Tour®."},
    "per_night": {"es": "por noche", "en": "per night"},
    "from": {"es": "Desde", "en": "From"},
    "guests_up_to": {"es": "Hasta {n} huéspedes", "en": "Up to {n} guests"},
    "solo": {"es": "1 persona", "en": "1 guest"},
    "pair": {"es": "Pareja", "en": "Couple"},
    "extra": {"es": "Persona adicional", "en": "Extra guest"},
    "na": {"es": "No aplica", "en": "Not available"},
    "photos_soon": {"es": "Fotos próximamente", "en": "Photos coming soon"},
    "photo_n": {"es": "Foto {i} de {n}", "en": "Photo {i} of {n}"},
    "prev": {"es": "Anterior", "en": "Previous"},
    "next": {"es": "Siguiente", "en": "Next"},
    "gallery": {"es": "Galería", "en": "Gallery"},
    "rating_google": {"es": "en Google", "en": "on Google"},
    "reviews": {"es": "opiniones", "en": "reviews"},
    # Ahora en la finca
    "live.title": {"es": "Ahora en la finca", "en": "Right now at the farm"},
    "live.time": {"es": "Hora local", "en": "Local time"},
    "live.weather": {"es": "Clima", "en": "Weather"},
    "live.sunrise": {"es": "Amanecer", "en": "Sunrise"},
    "live.sunset": {"es": "Atardecer", "en": "Sunset"},
    "live.harvest_on": {"es": "En plena cosecha", "en": "Harvest in full swing"},
    "live.harvest_off": {"es": "Próxima cosecha: {m}", "en": "Next harvest: {m}"},
    "live.season": {"es": "Temporada", "en": "Season"},
    # Home
    "home.kicker": {"es": "Finca cafetera familiar · Chinchiná, Caldas", "en": "Family coffee farm · Chinchiná, Colombia"},
    "home.h1_a": {"es": "Despierta donde", "en": "Wake up where"},
    "home.h1_b": {"es": "nace tu café.", "en": "your coffee is born."},
    "home.lead": {
        "es": "Casa Chute es una finca cafetera en pleno Paisaje Cultural Cafetero. Duerme entre cafetales, vive el Barista Show Tour® y llévate a casa el Bourbon que cultivamos a mano.",
        "en": "Casa Chute is a coffee farm in the heart of Colombia's Coffee Cultural Landscape. Sleep among coffee trees, join the Barista Show Tour® and take home the Bourbon we grow by hand.",
    },
    "home.scroll": {"es": "Desliza", "en": "Scroll"},
    "home.two_ways": {"es": "Dos maneras de vivir Chute", "en": "Two ways to live Chute"},
    "home.stay_title": {"es": "Quédate en la finca", "en": "Stay on the farm"},
    "home.stay_text": {"es": "Seis habitaciones, piscina, kiosko y un mirador de guadua frente a las montañas de Caldas.", "en": "Six rooms, a pool, a kiosk and a bamboo lookout facing the mountains of Caldas."},
    "home.coffee_title": {"es": "Llévate la finca a casa", "en": "Take the farm home"},
    "home.coffee_text": {"es": "Bourbon de 2.000 cafetos, cosechado a mano y secado al sol. Notas a cacao, panela y fruta amarilla.", "en": "Bourbon from 2,000 trees, hand-picked and sun-dried. Notes of cocoa, panela and yellow fruit."},
    "home.stat_rating": {"es": "en Google", "en": "on Google"},
    "home.stat_trees": {"es": "cafetos de Bourbon", "en": "Bourbon coffee trees"},
    "home.stat_rooms": {"es": "habitaciones", "en": "rooms"},
    "home.stat_unesco": {"es": "Paisaje Cultural Cafetero, Patrimonio UNESCO", "en": "Coffee Cultural Landscape, UNESCO World Heritage"},
    "home.process_kicker": {"es": "Del grano a la taza", "en": "From bean to cup"},
    "home.process_title": {"es": "Mira madurar tu café", "en": "Watch your coffee ripen"},
    "home.process_lead": {"es": "Cada paso ocurre aquí, a unos metros de tu habitación.", "en": "Every step happens here, a few metres from your room."},
    "home.rooms_kicker": {"es": "Casa Chute", "en": "Casa Chute"},
    "home.rooms_title": {"es": "Duerme con la tranquilidad del campo", "en": "Sleep in the quiet of the countryside"},
    "home.rooms_lead": {"es": "y levántate con la energía de una taza de café.", "en": "and wake up to the energy of a cup of coffee."},
    "home.price_toggle": {"es": "Ver precio para", "en": "Show price for"},
    "home.tour_kicker": {"es": "Experiencia insignia", "en": "Signature experience"},
    "home.tour_title": {"es": "Barista Show Tour®", "en": "Barista Show Tour®"},
    "home.calendar_title": {"es": "El año en la finca", "en": "A year on the farm"},
    "home.calendar_lead": {"es": "Dos cosechas al año. Si nos visitas en temporada, la finca está en plena actividad.", "en": "Two harvests a year. Visit in season and you'll find the farm in full swing."},
    "home.harvest": {"es": "Cosecha", "en": "Harvest"},
    "home.today": {"es": "Hoy", "en": "Today"},
    "home.location_title": {"es": "En el corazón del Eje Cafetero", "en": "In the heart of the Coffee Region"},
    "home.location_text": {
        "es": "Vereda Alto de la Mina, al occidente de Chinchiná, entre Manizales y Pereira. Un paisaje inscrito como Patrimonio de la Humanidad por la UNESCO en 2011.",
        "en": "Alto de la Mina, west of Chinchiná, between Manizales and Pereira — a landscape inscribed as UNESCO World Heritage in 2011.",
    },
    "home.final_title": {"es": "Tu próximo amanecer huele a café.", "en": "Your next sunrise smells of coffee."},
    "home.insta_title": {"es": "La finca, día a día", "en": "The farm, day by day"},
    # Casa
    "casa.kicker": {"es": "Alojamiento turístico rural", "en": "Rural farm stay"},
    "casa.h1": {"es": "Casa Chute", "en": "Casa Chute"},
    "casa.lead": {
        "es": "Duerme con la tranquilidad del campo y levántate con la energía de una taza de café. Una casa familiar entre cafetales, con vista a las montañas de Caldas.",
        "en": "Sleep in the quiet of the countryside and wake up to the energy of a cup of coffee. A family home among coffee trees, overlooking the mountains of Caldas.",
    },
    "casa.amenities": {"es": "Lo que encontrarás", "en": "What you'll find"},
    "casa.rooms": {"es": "Habitaciones y tarifas", "en": "Rooms and rates"},
    "casa.spaces": {"es": "Los espacios", "en": "The spaces"},
    "casa.video": {"es": "Conoce Casa Chute en un minuto", "en": "Discover Casa Chute in one minute"},
    "casa.policies": {"es": "Antes de llegar", "en": "Before you arrive"},
    "casa.faq": {"es": "Preguntas frecuentes", "en": "Frequently asked questions"},
    "casa.where": {"es": "Cómo llegar", "en": "How to get here"},
    "casa.where_text": {
        "es": "Desde Chinchiná, toma la vía hacia La Quiebra – Naranjal y sube hasta la vereda Alto de la Mina. Al reservar te enviamos la ubicación exacta por WhatsApp.",
        "en": "From Chinchiná, take the road towards La Quiebra – Naranjal and drive up to Alto de la Mina. When you book, we send you the exact location by WhatsApp.",
    },
    # Estimador / reservas
    "book.title": {"es": "Calcula tu estancia", "en": "Estimate your stay"},
    "book.lead": {"es": "Elige habitación, fechas y huéspedes. El valor se calcula al instante con nuestras tarifas publicadas.", "en": "Choose a room, dates and guests. The price is calculated instantly from our published rates."},
    "book.room": {"es": "Habitación", "en": "Room"},
    "book.checkin": {"es": "Llegada", "en": "Check-in"},
    "book.checkout": {"es": "Salida", "en": "Check-out"},
    "book.guests": {"es": "Huéspedes", "en": "Guests"},
    "book.nights": {"es": "noches", "en": "nights"},
    "book.night": {"es": "noche", "en": "night"},
    "book.total": {"es": "Total estimado", "en": "Estimated total"},
    "book.choose_dates": {"es": "Elige tus fechas para ver el total", "en": "Pick your dates to see the total"},
    "book.estimate_note": {"es": "Valor de referencia. Te confirmamos disponibilidad y precio final.", "en": "Reference price. We confirm availability and final price."},
    "book.your_details": {"es": "Tus datos", "en": "Your details"},
    "book.max_guests": {"es": "Esta habitación admite hasta {n} huéspedes.", "en": "This room sleeps up to {n} guests."},
    "book.h1": {"es": "Reserva tu estancia", "en": "Book your stay"},
    "book.page_lead": {"es": "Seis habitaciones entre cafetales, con vista a las montañas de Caldas. Envíanos tu solicitud y te confirmamos disponibilidad por WhatsApp.", "en": "Six rooms among the coffee trees, overlooking the mountains of Caldas. Send us your request and we'll confirm availability by WhatsApp."},
    # Formularios
    "form.name": {"es": "Nombre completo", "en": "Full name"},
    "form.email": {"es": "Correo electrónico", "en": "Email"},
    "form.phone": {"es": "Teléfono / WhatsApp", "en": "Phone / WhatsApp"},
    "form.message": {"es": "Mensaje", "en": "Message"},
    "form.notes": {"es": "Comentarios", "en": "Comments"},
    "form.topic": {"es": "Tema", "en": "Topic"},
    "form.topic.estancia": {"es": "Estancia en Casa Chute", "en": "Stay at Casa Chute"},
    "form.topic.cafe": {"es": "Compra de café", "en": "Buying coffee"},
    "form.topic.tour": {"es": "Barista Show Tour®", "en": "Barista Show Tour®"},
    "form.topic.otro": {"es": "Otro", "en": "Other"},
    "form.city": {"es": "Ciudad", "en": "City"},
    "form.address": {"es": "Dirección de envío", "en": "Shipping address"},
    "form.people": {"es": "Personas", "en": "People"},
    "form.date": {"es": "Fecha deseada", "en": "Preferred date"},
    "form.consent": {
        "es": "Autorizo el tratamiento de mis datos para atender esta solicitud, según la",
        "en": "I authorise the processing of my data to handle this request, under the",
    },
    "form.privacy_link": {"es": "política de datos", "en": "privacy policy"},
    "form.required": {"es": "Obligatorio", "en": "Required"},
    "form.optional": {"es": "opcional", "en": "optional"},
    "err.required": {"es": "Este campo es obligatorio.", "en": "This field is required."},
    "err.email": {"es": "Escribe un correo válido.", "en": "Enter a valid email."},
    "err.phone": {"es": "Escribe un teléfono válido.", "en": "Enter a valid phone number."},
    "err.contact": {"es": "Déjanos un correo o un teléfono para responderte.", "en": "Leave an email or phone so we can reply."},
    "err.dates": {"es": "Revisa las fechas: la salida debe ser posterior a la llegada y no en el pasado.", "en": "Check your dates: check-out must be after check-in and not in the past."},
    "err.guests": {"es": "Número de huéspedes no válido para esta habitación.", "en": "Invalid number of guests for this room."},
    "err.room": {"es": "Elige una habitación.", "en": "Choose a room."},
    "err.consent": {"es": "Necesitamos tu autorización para responderte.", "en": "We need your consent to reply."},
    "err.qty": {"es": "Elige al menos una bolsa.", "en": "Choose at least one bag."},
    "err.people": {"es": "El tour es para grupos de 4 a 10 personas.", "en": "The tour is for groups of 4 to 10 people."},
    "err.form": {"es": "Revisa los campos marcados.", "en": "Please check the highlighted fields."},
    "err.csrf": {"es": "La sesión expiró. Vuelve a enviar el formulario.", "en": "Your session expired. Please submit the form again."},
    "err.rate": {"es": "Demasiados envíos seguidos. Intenta de nuevo en unos minutos.", "en": "Too many submissions. Please try again in a few minutes."},
    # Café
    "cafe.kicker": {"es": "Café de origen · Finca La Carolina", "en": "Single origin · Finca La Carolina"},
    "cafe.h1": {"es": "Café Chute", "en": "Café Chute"},
    "cafe.lead": {"es": "Bourbon cultivado en 2.000 cafetos de la vereda Alto de la Mina. Cosechado a mano, secado al sol y tostado en la región.", "en": "Bourbon grown on 2,000 trees in Alto de la Mina. Hand-picked, sun-dried and roasted in the region."},
    "cafe.notes": {"es": "Perfil sensorial", "en": "Tasting profile"},
    "cafe.notes_lead": {"es": "Nuestro Bourbon tiene notas a", "en": "Our Bourbon has notes of"},
    "cafe.format": {"es": "Presentación", "en": "Format"},
    "cafe.bag": {"es": "Bolsa de 500 g", "en": "500 g bag"},
    "cafe.price_ask": {"es": "Precio y envío por WhatsApp", "en": "Price & shipping via WhatsApp"},
    "cafe.order_title": {"es": "Pide tu café", "en": "Order your coffee"},
    "cafe.order_lead": {"es": "Déjanos tu pedido y te confirmamos total y envío. Sin pagos en línea: pagas cuando te confirmamos.", "en": "Leave your order and we'll confirm the total and shipping. No online payment: you pay once we confirm."},
    "cafe.qty": {"es": "Cantidad", "en": "Quantity"},
    "cafe.variety": {"es": "La variedad", "en": "The variety"},
    "cafe.variety_text": {
        "es": "El Bourbon es una variedad de origen etíope. El árbol genealógico del café es grande: este mapa muestra de dónde viene la nuestra.",
        "en": "Bourbon is a variety of Ethiopian origin. Coffee's family tree is large — this map shows where ours comes from.",
    },
    "cafe.where": {"es": "Dónde comprar", "en": "Where to buy"},
    "cafe.facts_origin": {"es": "Origen", "en": "Origin"},
    "cafe.facts_variety": {"es": "Variedad", "en": "Variety"},
    "cafe.facts_process": {"es": "Proceso", "en": "Process"},
    "cafe.facts_process_v": {"es": "Despulpado, fermentado y secado al sol", "en": "Pulped, fermented, sun-dried"},
    "cafe.facts_harvest": {"es": "Cosecha", "en": "Harvest"},
    "cafe.facts_harvest_v": {"es": "Abr–may y ago–oct", "en": "Apr–May & Aug–Oct"},
    # Experiencias
    "exp.kicker": {"es": "Experiencias en la finca", "en": "Farm experiences"},
    "exp.h1": {"es": "El café se vive", "en": "Coffee is meant to be lived"},
    "exp.lead": {"es": "Más que una taza: el ritual, la cata y el paisaje donde nace.", "en": "More than a cup: the ritual, the cupping and the landscape where it's born."},
    "exp.price_person": {"es": "por persona", "en": "per person"},
    "exp.price_pair": {"es": "por pareja", "en": "per couple"},
    "exp.group": {"es": "Grupos de {a} a {b} personas", "en": "Groups of {a} to {b} people"},
    "exp.duration": {"es": "Duración mínima: {h} horas", "en": "Minimum duration: {h} hours"},
    "exp.calc": {"es": "Valor estimado para tu grupo", "en": "Estimated price for your group"},
    "exp.landscape_title": {"es": "Miradores para no hacer nada", "en": "Lookouts for doing nothing at all"},
    "exp.landscape_text": {"es": "El kiosko, el mirador de guadua y los corredores están hechos para mirar el valle, ver caer la tarde y tomarse otro café.", "en": "The kiosk, the bamboo lookout and the porches are made for gazing at the valley, watching the afternoon fade and having another coffee."},
    "exp.harvest_title": {"es": "Ven en cosecha", "en": "Come during harvest"},
    "exp.harvest_text": {"es": "De abril a mayo y de agosto a octubre, la finca está en plena actividad: cerezas rojas en las ramas y café secándose al sol.", "en": "April to May and August to October, the farm is in full swing: red cherries on the branches and coffee drying in the sun."},
    # Historia
    "hist.kicker": {"es": "Nuestra historia", "en": "Our story"},
    "hist.h1": {"es": "Una herencia que se toma a sorbos", "en": "A legacy you sip"},
    "hist.p1": {
        "es": "De la herencia de los abuelos caficultores, de la tradición cafetera y del amor por el campo nace Café Chute: el empujón que necesitas para empezar y terminar el día.",
        "en": "Café Chute was born from our coffee-growing grandparents' legacy, a coffee tradition and a love for the countryside: the boost you need to start and end your day.",
    },
    "hist.p2": {
        "es": "La Finca La Carolina está en la vereda Alto de la Mina, en Chinchiná. Allí cuidamos 2.000 cafetos de Bourbon. Es una finca familiar donde el conocimiento del café se ha heredado de generación en generación, con la pasión y la entrega que caracterizan al campesino colombiano.",
        "en": "Finca La Carolina sits in Alto de la Mina, Chinchiná, where we tend 2,000 Bourbon coffee trees. It's a family farm where coffee know-how has been handed down from generation to generation, with the passion and dedication of the Colombian farmer.",
    },
    "hist.p3": {
        "es": "Chute es el fruto de un lote especial de Bourbon, tratado y cuidado de manera única para que disfrutes una gran taza en tu casa u oficina. Cuidamos el proceso del cultivo a la taza.",
        "en": "Chute is the fruit of a special lot of Bourbon, grown and cared for in a unique way so you can enjoy a great cup at home or at work. We look after every step, from field to cup.",
    },
    "hist.process": {"es": "Cómo llega Café Chute a tu casa", "en": "How Café Chute reaches your home"},
    "hist.unesco": {"es": "Paisaje Cultural Cafetero", "en": "Coffee Cultural Landscape"},
    "hist.unesco_text": {
        "es": "La finca hace parte del Paisaje Cultural Cafetero de Colombia, inscrito en la Lista del Patrimonio Mundial de la UNESCO en 2011.",
        "en": "The farm is part of Colombia's Coffee Cultural Landscape, inscribed on UNESCO's World Heritage List in 2011.",
    },
    # Contacto
    "contact.kicker": {"es": "Hablemos", "en": "Let's talk"},
    "contact.h1": {"es": "Contacto", "en": "Contact"},
    "contact.lead": {"es": "La forma más rápida es WhatsApp. También puedes escribirnos aquí y te respondemos pronto.", "en": "WhatsApp is the fastest way. You can also write to us here and we'll reply soon."},
    "contact.channels": {"es": "Canales directos", "en": "Direct channels"},
    "contact.call": {"es": "Llamar", "en": "Call"},
    "contact.address": {"es": "Dirección", "en": "Address"},
    "contact.form": {"es": "Escríbenos", "en": "Write to us"},
    "contact.map_note": {"es": "El mapa de Google se carga solo si lo pides (sin cookies de terceros hasta entonces).", "en": "The Google map only loads when you ask for it (no third-party cookies until then)."},
    # Gracias
    "thanks.h1": {"es": "¡Gracias! Recibimos tu solicitud", "en": "Thank you! We received your request"},
    "thanks.lead": {"es": "Te responderemos pronto por WhatsApp o correo. Si tienes prisa, escríbenos directamente:", "en": "We'll reply soon by WhatsApp or email. In a hurry? Message us directly:"},
    "thanks.ref": {"es": "Número de solicitud", "en": "Request number"},
    # Footer
    "footer.tagline": {"es": "Finca cafetera familiar en el Paisaje Cultural Cafetero.", "en": "Family coffee farm in the Coffee Cultural Landscape."},
    "footer.explore": {"es": "Explora", "en": "Explore"},
    "footer.contact": {"es": "Contacto", "en": "Contact"},
    "footer.follow": {"es": "Síguenos", "en": "Follow us"},
    "footer.privacy": {"es": "Política de datos", "en": "Privacy policy"},
    "footer.rnt": {"es": "Registro Nacional de Turismo", "en": "National Tourism Registry"},
    "footer.rights": {"es": "Todos los derechos reservados.", "en": "All rights reserved."},
    # Cookies (solo si hay analítica configurada)
    "cookies.text": {"es": "Usamos cookies de analítica para entender qué funciona en la web. Solo se activan si las aceptas.", "en": "We use analytics cookies to learn what works on the site. They're only enabled if you accept."},
    "cookies.accept": {"es": "Aceptar", "en": "Accept"},
    "cookies.reject": {"es": "Rechazar", "en": "Decline"},
    # 404
    "404.title": {"es": "Esta página se fue a secar al sol", "en": "This page went out to dry in the sun"},
    "404.text": {"es": "No encontramos lo que buscas. Quizá te interese:", "en": "We couldn't find what you're looking for. Maybe try:"},
    "500.title": {"es": "Algo se nos regó", "en": "We spilled something"},
    "500.text": {"es": "Tuvimos un problema. Inténtalo de nuevo o escríbenos por WhatsApp.", "en": "Something went wrong. Try again or message us on WhatsApp."},
}

MONTHS = {
    "es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}
MONTHS_LONG = {
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
}


def t(key: str, lang: str, **kwargs) -> str:
    entry = STRINGS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry[DEFAULT_LANG]
    return text.format(**kwargs) if kwargs else text


def tr(value, lang: str):
    """Devuelve la versión en `lang` de un dict {"es","en"}; deja pasar el resto."""
    if isinstance(value, dict) and DEFAULT_LANG in value:
        return value.get(lang, value[DEFAULT_LANG])
    return value


def format_cop(value: int | None, lang: str) -> str:
    if value is None:
        return ""
    s = f"{value:,}"
    return "$" + (s.replace(",", ".") if lang == "es" else s)
