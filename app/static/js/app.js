/* Casa Chute · Café Chute — interacciones (vanilla JS, sin dependencias) */
(() => {
  "use strict";
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const lang = document.body.dataset.lang || "es";
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const L = {
    es: { night: "noche", nights: "noches", guests: "huéspedes", guest: "huésped", choose: "Elige tus fechas para ver el total",
          max: "Esta habitación admite hasta {n} huéspedes.", pick: "Elige una habitación", solo: "1 persona", pair: "Pareja",
          wa: "Hola, Casa Chute. Quiero reservar", photo: "Foto {i} de {n}" },
    en: { night: "night", nights: "nights", guests: "guests", guest: "guest", choose: "Pick your dates to see the total",
          max: "This room sleeps up to {n} guests.", pick: "Choose a room", solo: "1 guest", pair: "Couple",
          wa: "Hi Casa Chute! I would like to book", photo: "Photo {i} of {n}" },
  }[lang];
  const fmt = (n) => "$" + Math.round(n).toLocaleString(lang === "es" ? "es-CO" : "en-US");
  const tpl = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => o[k]);

  /* ---------------------------------------------------- Colores de carga en imágenes */
  $$("img.ph[data-color]").forEach((img) => {
    if (!img.complete) img.style.backgroundColor = img.dataset.color;
  });

  /* ---------------------------------------------------- Cabecera */
  const header = $("[data-header]");
  let lastY = window.scrollY;
  const onScroll = () => {
    const y = window.scrollY;
    header?.classList.toggle("is-scrolled", y > 40);
    if (header && !document.body.classList.contains("nav-open")) {
      header.classList.toggle("is-hidden", y > 500 && y > lastY + 4);
      if (y < lastY - 4) header.classList.remove("is-hidden");
    }
    lastY = y;
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const toggle = $("[data-nav-toggle]");
  const nav = $("[data-nav]");
  const setNav = (open) => {
    nav.classList.toggle("is-open", open);
    document.body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    if (open) $("a", nav)?.focus();
  };
  toggle?.addEventListener("click", () => setNav(!nav.classList.contains("is-open")));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && nav?.classList.contains("is-open")) { setNav(false); toggle.focus(); } });
  $$("a", nav || document.createElement("div")).forEach((a) => a.addEventListener("click", () => setNav(false)));

  /* ---------------------------------------------------- Aparición al hacer scroll */
  if ("IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    const fold = window.innerHeight;
    const below = $$(".reveal").filter((el) => el.getBoundingClientRect().top > fold);
    below.forEach((el) => { el.classList.add("reveal--wait"); io.observe(el); });
  }

  /* ---------------------------------------------------- Semillas de diente de león (hero) */
  const canvas = $("[data-seeds]");
  if (canvas && !reduceMotion) {
    const ctx = canvas.getContext("2d");
    let w, h, dpr, seeds = [], running = true, raf;
    const resize = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    const spawn = (initial) => {
      const originX = w * 0.82, originY = h * 0.38;
      return {
        x: initial ? Math.random() * w : originX + (Math.random() - 0.5) * 120,
        y: initial ? Math.random() * h : originY + (Math.random() - 0.5) * 120,
        vx: -(0.25 + Math.random() * 0.6), vy: -(0.05 + Math.random() * 0.35),
        size: 7 + Math.random() * 9, rot: Math.random() * Math.PI * 2, vr: (Math.random() - 0.5) * 0.01,
        phase: Math.random() * Math.PI * 2, alpha: 0.25 + Math.random() * 0.5,
      };
    };
    const drawSeed = (s) => {
      ctx.save();
      ctx.translate(s.x, s.y); ctx.rotate(s.rot);
      ctx.globalAlpha = s.alpha;
      ctx.strokeStyle = "#fbf7f0"; ctx.lineWidth = 0.8;
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, s.size); ctx.stroke();       // tallo
      ctx.fillStyle = "#e8c06e"; ctx.beginPath(); ctx.ellipse(0, s.size + 1.5, 1.2, 2, 0, 0, Math.PI * 2); ctx.fill(); // aquenio
      for (let i = -4; i <= 4; i++) {                                                 // vilano
        const a = -Math.PI / 2 + i * 0.32;
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * s.size * 0.8, Math.sin(a) * s.size * 0.8); ctx.stroke();
      }
      ctx.restore();
    };
    const tick = (t) => {
      ctx.clearRect(0, 0, w, h);
      seeds.forEach((s, i) => {
        s.x += s.vx + Math.sin(t / 1800 + s.phase) * 0.25;
        s.y += s.vy + Math.cos(t / 2200 + s.phase) * 0.18;
        s.rot += s.vr;
        if (s.x < -30 || s.y < -30) seeds[i] = spawn(false);
        drawSeed(s);
      });
      if (running) raf = requestAnimationFrame(tick);
    };
    resize();
    seeds = Array.from({ length: Math.round(Math.min(46, w / 28)) }, () => spawn(true));
    window.addEventListener("resize", resize);
    new IntersectionObserver(([en]) => {
      running = en.isIntersecting;
      if (running) raf = requestAnimationFrame(tick); else cancelAnimationFrame(raf);
    }).observe(canvas);
  }

  /* ---------------------------------------------------- Ahora en la finca */
  const live = $("[data-live]");
  if (live) {
    const icons = { sun: "sun", moon: "moon", cloud: "cloud", "cloud-sun": "cloud-sun", rain: "rain", fog: "fog", storm: "storm" };
    const clock = () => {
      const now = new Date();
      const t = new Intl.DateTimeFormat(lang === "es" ? "es-CO" : "en-US", { hour: "numeric", minute: "2-digit", timeZone: "America/Bogota" }).format(now);
      $$("[data-live-time]").forEach((el) => (el.textContent = t));
    };
    clock(); setInterval(clock, 30000);
    fetch(`/api/finca?lang=${lang}`, { headers: { Accept: "application/json" } })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => {
        if (!d || !d.weather) return;
        $$("[data-live]").forEach((box) => {
          const w = d.weather;
          $("[data-live-temp]", box).textContent = `${w.temp} °C`;
          $("[data-live-desc]", box).textContent = w.desc;
          const use = $("[data-live-icon] use", box);
          if (use) use.setAttribute("href", `#i-${icons[w.icon] || "cloud"}`);
          $("[data-live-weather]", box).hidden = false;
          if (w.sunrise) {
            $("[data-live-sunrise]", box).textContent = w.sunrise;
            $("[data-live-sunset]", box).textContent = w.sunset;
            $("[data-live-sun]", box).hidden = false;
          }
        });
      })
      .catch(() => {});
  }

  /* ---------------------------------------------------- Del grano a la taza (lente que madura) */
  const story = $("[data-story]");
  if (story) {
    const stages = ["#7fa34a", "#c9b43a", "#e08a2e", "#c0392b", "#7a4128", "#d9a441"];
    const steps = $$("[data-step]", story);
    const photos = $$("[data-lens-photo]", story);
    const lens = $("[data-lens]", story);
    const prog = $("[data-lens-progress]", story);
    const num = $("[data-lens-num]", story);
    const C = 2 * Math.PI * 96;
    const activate = (i) => {
      steps.forEach((s, k) => s.classList.toggle("is-active", k === i));
      photos.forEach((p, k) => p.classList.toggle("is-active", k === i));
      lens.style.setProperty("--stage", stages[i] || stages[0]);
      prog.style.strokeDashoffset = String(C * (1 - (i + 1) / steps.length));
      num.textContent = String(i + 1).padStart(2, "0");
    };
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) activate(Number(en.target.dataset.step)); });
    }, { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach((s) => io.observe(s));
    activate(0);
  }

  /* ---------------------------------------------------- Contadores */
  if (!reduceMotion && "IntersectionObserver" in window) {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        const el = en.target, end = Number(el.dataset.count), t0 = performance.now();
        const step = (t) => {
          const p = Math.min(1, (t - t0) / 1400), v = Math.round(end * (1 - Math.pow(1 - p, 3)));
          el.textContent = v.toLocaleString(lang === "es" ? "es-CO" : "en-US");
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
        cio.unobserve(el);
      });
    }, { threshold: 0.6 });
    $$("[data-count]").forEach((el) => cio.observe(el));
  }

  /* ---------------------------------------------------- Precio por persona / pareja */
  const priceToggle = $("[data-price-toggle]");
  priceToggle?.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-mode]");
    if (!btn) return;
    const mode = btn.dataset.mode;
    $$("button", priceToggle).forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    $$(".room-card").forEach((card) => {
      const el = $("[data-price]", card), lbl = $("[data-price-label]", card);
      el.classList.add("is-swapping");
      setTimeout(() => {
        el.textContent = mode === "solo" ? card.dataset.solo : card.dataset.pair;
        lbl.textContent = mode === "solo" ? L.solo : L.pair;
        el.classList.remove("is-swapping");
      }, 180);
    });
  });

  /* ---------------------------------------------------- Carril horizontal */
  $$("[data-rail]").forEach((rail) => {
    const track = $("[data-rail-track]", rail);
    const by = () => (track.querySelector(".rail__item")?.offsetWidth || 300) + 24;
    $("[data-rail-prev]", rail)?.addEventListener("click", () => track.scrollBy({ left: -by(), behavior: reduceMotion ? "auto" : "smooth" }));
    $("[data-rail-next]", rail)?.addEventListener("click", () => track.scrollBy({ left: by(), behavior: reduceMotion ? "auto" : "smooth" }));
  });

  /* ---------------------------------------------------- Steppers (+ / −) */
  $$(".stepper").forEach((st) => {
    const input = $("input", st);
    const bump = (d) => {
      const min = Number(input.min || 0), max = Number(input.max || 99);
      input.value = String(Math.min(max, Math.max(min, (Number(input.value) || 0) + d)));
      input.dispatchEvent(new Event("input", { bubbles: true }));
    };
    $("[data-step-down]", st)?.addEventListener("click", () => bump(-1));
    $("[data-step-up]", st)?.addEventListener("click", () => bump(1));
  });

  /* ---------------------------------------------------- Fechas mínimas (hoy en Colombia) */
  const todayCO = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Bogota" }).format(new Date());
  const addDays = (iso, n) => { const d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };
  $$("input[type=date][data-min-today], input[data-checkin]").forEach((i) => (i.min = todayCO));

  /* ---------------------------------------------------- Calculadora de estancia */
  const booking = $("[data-booking]");
  if (booking) {
    const rooms = JSON.parse(booking.dataset.rooms || "[]");
    const room = $("[data-room]", booking), ci = $("[data-checkin]", booking), co = $("[data-checkout]", booking);
    const guests = $("[data-guests]", booking), hint = $("[data-cap-hint]", booking);
    const sRoom = $("[data-sum-room]", booking), sCalc = $("[data-sum-calc]", booking);
    const sTotal = $("[data-sum-total]", booking), sWa = $("[data-sum-wa]", booking);
    const nightPrice = (r, g) => {
      if (g < 1 || g > r.capacity) return null;
      if (g === 1) return r.solo;
      if (g > 2 && r.extra == null) return null;
      return r.pair + Math.max(0, g - 2) * (r.extra || 0);
    };
    const update = () => {
      const r = rooms.find((x) => x.id === room.value);
      if (ci.value) co.min = addDays(ci.value, 1);
      if (ci.value && co.value && co.value <= ci.value) co.value = addDays(ci.value, 1);
      if (r) {
        guests.max = r.capacity;
        if (Number(guests.value) > r.capacity) guests.value = r.capacity;
        hint.textContent = tpl(L.max, { n: r.capacity });
      }
      const g = Number(guests.value) || 1;
      sRoom.textContent = r ? r.name : L.pick;
      const nights = ci.value && co.value ? Math.round((new Date(co.value) - new Date(ci.value)) / 864e5) : 0;
      const per = r ? nightPrice(r, g) : null;
      let text = L.choose, total = null;
      if (r && per && nights > 0) {
        total = per * nights;
        text = `${fmt(per)} × ${nights} ${nights === 1 ? L.night : L.nights} · ${g} ${g === 1 ? L.guest : L.guests}`;
      } else if (r && per) {
        text = `${fmt(per)} / ${L.night} · ${g} ${g === 1 ? L.guest : L.guests} — ${L.choose.toLowerCase()}`;
      }
      sCalc.textContent = text;
      sTotal.textContent = total ? `${fmt(total)} COP` : "—";
      const dfmt = (iso) => iso.split("-").reverse().join("/");
      const msg = r ? `${L.wa}: ${r.name}${ci.value ? " · " + dfmt(ci.value) : ""}${co.value ? " → " + dfmt(co.value) : ""} · ${g} ${g === 1 ? L.guest : L.guests}${total ? " · " + fmt(total) + " COP" : ""}` : L.wa;
      sWa.href = `https://wa.me/${booking.dataset.wa}?text=${encodeURIComponent(msg)}`;
    };
    [room, ci, co, guests].forEach((el) => el.addEventListener("input", update));
    room.addEventListener("change", update);
    update();
  }

  /* ---------------------------------------------------- Calculadora del tour */
  const tour = $("[data-tour]");
  const people = $("[data-people]");
  if (tour && people) {
    const upd = () => {
      const n = Number(people.value), min = Number(tour.dataset.min), max = Number(tour.dataset.max);
      const total = n >= min && n <= max ? Math.floor(n / 2) * Number(tour.dataset.pair) + (n % 2) * Number(tour.dataset.person) : null;
      $("[data-tour-total]", tour).textContent = total ? fmt(total) : "—";
    };
    people.addEventListener("input", upd); upd();
  }

  /* ---------------------------------------------------- Pedido de café */
  const order = $("[data-order]");
  if (order && order.dataset.price) {
    const out = $("[data-order-total]", order);
    const upd = () => {
      const q = $$("[data-qty]", order).reduce((a, i) => a + (Number(i.value) || 0), 0);
      out.textContent = q ? `${fmt(q * Number(order.dataset.price))} COP` : "—";
    };
    $$("[data-qty]", order).forEach((i) => i.addEventListener("input", upd)); upd();
  }

  /* ---------------------------------------------------- Evitar doble envío */
  $$("form").forEach((f) => f.addEventListener("submit", () => {
    const b = $("button[type=submit]", f);
    if (b && f.checkValidity()) setTimeout(() => (b.disabled = true), 0);
  }));

  /* ---------------------------------------------------- Pestañas de espacios */
  $$("[data-tabs]").forEach((box) => {
    const tabs = $$("[role=tab]", box);
    const select = (tab) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        $("#" + t.getAttribute("aria-controls")).hidden = !on;
      });
    };
    tabs.forEach((t, i) => {
      t.addEventListener("click", () => select(t));
      t.addEventListener("keydown", (e) => {
        const d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (d) { const n = tabs[(i + d + tabs.length) % tabs.length]; select(n); n.focus(); }
      });
    });
  });

  /* ---------------------------------------------------- Galería (lightbox) */
  const lb = $("[data-lightbox]");
  if (lb && typeof lb.showModal === "function") {
    const imgEl = $("[data-lb-img]", lb), cap = $("[data-lb-cap]", lb);
    let items = [], idx = 0;
    const show = (i) => {
      idx = (i + items.length) % items.length;
      imgEl.src = items[idx].href; imgEl.alt = items[idx].caption;
      cap.textContent = `${items[idx].caption} · ${tpl(L.photo, { i: idx + 1, n: items.length })}`;
    };
    document.addEventListener("click", (e) => {
      const trg = e.target.closest("[data-gallery]");
      if (!trg) return;
      const t = $(`template[data-gallery-items="${trg.dataset.gallery}"]`);
      if (!t) return;
      items = $$("a", t.content).map((a) => ({ href: a.getAttribute("href"), caption: a.dataset.caption }));
      show(Number(trg.dataset.index) || 0);
      lb.showModal();
    });
    $("[data-lb-close]", lb).addEventListener("click", () => lb.close());
    $("[data-lb-prev]", lb).addEventListener("click", () => show(idx - 1));
    $("[data-lb-next]", lb).addEventListener("click", () => show(idx + 1));
    lb.addEventListener("keydown", (e) => { if (e.key === "ArrowRight") show(idx + 1); if (e.key === "ArrowLeft") show(idx - 1); });
    lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
  }

  /* ---------------------------------------------------- YouTube y mapa solo al hacer clic */
  $$("[data-youtube]").forEach((btn) => btn.addEventListener("click", () => {
    const f = document.createElement("iframe");
    f.src = `https://www.youtube-nocookie.com/embed/${btn.dataset.youtube}?autoplay=1&rel=0`;
    f.title = "Casa Chute"; f.allow = "autoplay; encrypted-media; picture-in-picture"; f.allowFullscreen = true;
    btn.replaceChildren(f);
  }, { once: true }));
  $$("[data-map-load]").forEach((btn) => btn.addEventListener("click", () => {
    const box = btn.closest("[data-map]");
    const f = document.createElement("iframe");
    f.src = `https://www.google.com/maps?q=${box.dataset.map}&z=13&output=embed`;
    f.title = "Google Maps — Casa Chute"; f.loading = "lazy"; f.referrerPolicy = "no-referrer-when-downgrade";
    box.replaceChildren(f);
  }, { once: true }));

  /* ---------------------------------------------------- Analítica opcional (solo con consentimiento) */
  const gaId = document.body.dataset.ga;
  const banner = $("[data-cookie]");
  const loadGA = () => {
    if (!gaId || window.gtag) return;
    const s = document.createElement("script");
    s.async = true; s.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date()); window.gtag("config", gaId, { anonymize_ip: true });
  };
  if (gaId && banner) {
    let choice = null;
    try { choice = localStorage.getItem("cc-consent"); } catch (_) {}
    if (choice === "yes") loadGA(); else if (choice !== "no") banner.hidden = false;
    $("[data-cookie-accept]", banner).addEventListener("click", () => { try { localStorage.setItem("cc-consent", "yes"); } catch (_) {} banner.hidden = true; loadGA(); });
    $("[data-cookie-reject]", banner).addEventListener("click", () => { try { localStorage.setItem("cc-consent", "no"); } catch (_) {} banner.hidden = true; });
  }
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-track]");
    if (a && window.gtag) window.gtag("event", "contact_click", { method: a.dataset.track, page: location.pathname });
  });
})();
