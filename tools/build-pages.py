#!/usr/bin/env python3
"""
Generate the static SEO pages that live next to the SPA:
  website/umzugsunternehmen-<city>/index.html   (23 city pages, 3 templates)
  website/umzugskosten/index.html               (Preise page)
  website/sitemap.xml

Content = client's change request PDF (Aenderung Sf7ah, 2026-09-16).
Re-run after editing cities.json or the templates below:
    python3 tools/build-pages.py
"""
import json, html, pathlib, datetime
from urllib.parse import quote

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent / "website"
BASE_URL = "https://mae-umzug-entruempelung.de"
PHONE_DISPLAY = "0176 66879641"
PHONE_TEL = "tel:017666879641"
EMAIL = "sparumzug@outlook.de"
WA_NUMBER = "4917666879641"
WA_MESSAGE = (HERE / "whatsapp-message.txt").read_text(encoding="utf-8").strip()
WA_URL = f"https://wa.me/{WA_NUMBER}?text={quote(WA_MESSAGE)}"
CITIES = json.loads((HERE / "cities.json").read_text(encoding="utf-8"))
TODAY = datetime.date.today().isoformat()

# ---------------------------------------------------------------- icons
I = {
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
 "checkc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
 "calc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path d="M16 10h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8 18h.01"/></svg>',
 "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>',
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/></svg>',
 "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>',
 "box": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>',
 "euro": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 10h12"/><path d="M4 14h9"/><path d="M19 6a7.7 7.7 0 0 0-5.2-2A7.9 7.9 0 0 0 6 12c0 4.4 3.5 8 7.8 8 2 0 3.8-.8 5.2-2"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/></svg>',
 "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
 "trash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>',
 "building": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/></svg>',
 "star": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
}

def e(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- layout
def nav(active):
    links = [("/", "Startseite"), ("/about", "Über Uns"), ("/services", "Leistungen"),
             ("/umzugskosten/", "Preise"), ("/calculator", "Kostenrechner"), ("/contact", "Kontakt")]
    def a():
        out = []
        for h, t in links:
            cls = ' class="is-active"' if h == active else ""
            out.append(f'<a href="{h}"{cls}>{t}</a>')
        return "".join(out)
    return f'''<nav class="nav" aria-label="Hauptnavigation"><div class="container">
<div class="nav__row">
  <a href="/" class="brand" aria-label="SparUmzug Startseite"><span class="brand__logo">SU</span><span class="brand__name">SparUmzug</span></a>
  <div class="nav__links">{a()}</div>
  <div class="nav__right">
    <a href="{PHONE_TEL}" class="nav__phone">{I["phone"]}{PHONE_DISPLAY}</a>
    <a href="/contact" class="btn btn--accent">Kostenloses Angebot</a>
  </div>
  <button class="nav__toggle" type="button" aria-label="Menü öffnen" aria-expanded="false" onclick="var m=document.getElementById('mnav');var o=m.classList.toggle('is-open');this.setAttribute('aria-expanded',o)">{I["menu"]}</button>
</div>
<div class="nav__mobile" id="mnav">{a()}<a href="{PHONE_TEL}" class="nav__phone">{I["phone"]}{PHONE_DISPLAY}</a><a href="/contact" class="btn btn--accent">Kostenloses Angebot</a></div>
</div></nav>'''

def footer(current_slug=None):
    cities = "".join(
        f'<a href="/umzugsunternehmen-{c["slug"]}/">Umzugsunternehmen {e(c["name"])}</a>' for c in CITIES)
    return f'''<footer class="footer"><div class="container section">
<div class="footer__grid">
  <div>
    <div class="brand"><span class="brand__logo">SU</span><span class="brand__name">SparUmzug</span></div>
    <p class="footer__desc">Professionelle Umzugslösungen, die Ihren Umzug einfach, erschwinglich und stressfrei gestalten.</p>
    <div class="social">
      <a href="{WA_URL}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">{I["wa"]}</a>
      <a href="https://www.facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook">{I["fb"]}</a>
      <a href="https://www.instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram">{I["ig"]}</a>
    </div>
  </div>
  <div><h4>Schnellzugriff</h4><ul>
    <li><a href="/">Startseite</a></li><li><a href="/about">Über Uns</a></li><li><a href="/services">Leistungen</a></li>
    <li><a href="/calculator">Kostenrechner</a></li><li><a href="/umzugskosten/">Preise</a></li><li><a href="/contact">Kontakt</a></li></ul></div>
  <div><h4>Rechtliches</h4><ul>
    <li><a href="/impressum">Impressum</a></li><li><a href="/agb">AGB</a></li>
    <li><a href="/widerruf">Widerrufsbelehrung</a></li><li><a href="/datenschutz">Datenschutz</a></li></ul></div>
  <div><h4>Kontakt</h4><ul>
    <li><a href="{PHONE_TEL}">{I["phone"]}{PHONE_DISPLAY}</a></li>
    <li><a href="mailto:{EMAIL}">{I["mail"]}{EMAIL}</a></li>
    <li>{I["pin"]}Moers, NRW, Deutschland</li></ul></div>
</div>
<div class="footer__cities"><h4>Umzugsunternehmen in Ihrer Stadt</h4><div>{cities}</div></div>
<div class="footer__bottom"><p>© {datetime.date.today().year} SparUmzug. Alle Rechte vorbehalten.</p><p>Fair. Zuverlässig. Professionelle Umzugsservices.</p></div>
</div></footer>
<div class="wa-float"><a href="{WA_URL}" target="_blank" rel="noopener noreferrer" class="wa-float__btn" aria-label="Angebot per WhatsApp anfordern"><span class="wa-float__ping"></span>{I["wa"]}</a><span class="wa-float__tip">Angebot per WhatsApp anfordern</span></div>'''

def page(*, title, description, canonical, body, jsonld, active):
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="SparUmzug">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="/assets/pages.css">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
{nav(active)}
<main>
{body}
</main>
{footer()}
</body>
</html>
'''

# ---------------------------------------------------------------- shared blocks
def chips(items, icon="check", cls=""):
    return '<div class="chips">' + "".join(f'<span class="chip {cls}">{I[icon]}{e(x)}</span>' for x in items) + "</div>"

def checks(items, cols3=False):
    return f'<div class="checks{" checks--3" if cols3 else ""}">' + "".join(f'<div class="check">{I["checkc"]}<span>{e(x)}</span></div>' for x in items) + "</div>"

def calc_card(city=None):
    where = f" in {e(city)}" if city else ""
    return f'''<aside class="calc-card">
<div class="card__icon">{I["calc"]}</div>
<h3>Umzugskosten{where} sofort berechnen</h3>
<p>Mit unserem Online-Kostenrechner erhalten Sie in wenigen Minuten eine unverbindliche Kostenschätzung für Ihren Umzug.</p>
<ul><li>{I["check"]}Entfernung, Wohnungsgröße &amp; Etagen</li><li>{I["check"]}Möbelinventar &amp; Zusatzleistungen</li><li>{I["check"]}Kostenlos &amp; ohne Anmeldung</li></ul>
<a href="/calculator" class="btn btn--accent btn--lg">Kosten berechnen {I["arrow"]}</a>
</aside>'''

def cta_block(h, p, city=None):
    return f'''<section class="section cta"><div class="container">
<h2 class="h2">{e(h)}</h2>
<p>{e(p)}</p>
<div class="cta__actions">
  <a href="/calculator" class="btn btn--accent btn--lg">{I["calc"]}Kostenrechner starten</a>
  <a href="{WA_URL}" target="_blank" rel="noopener noreferrer" class="btn btn--whatsapp btn--lg">{I["wa"]}Angebot per WhatsApp</a>
  <a href="/contact" class="btn btn--outline btn--lg">Kontaktformular</a>
</div>
<div class="cta__contact"><a href="{PHONE_TEL}">{I["phone"]}{PHONE_DISPLAY}</a><a href="mailto:{EMAIL}">{I["mail"]}{EMAIL}</a></div>
</div></section>'''

def other_cities(current):
    links = "".join(
        f'<a class="chip chip--link" href="/umzugsunternehmen-{c["slug"]}/">{I["pin"]}{e(c["name"])}</a>'
        for c in CITIES if c["slug"] != current)
    return f'''<section class="section section--card"><div class="container">
<span class="eyebrow">Weitere Standorte</span>
<h2 class="h2">SparUmzug in Ihrer Nähe</h2>
<p class="lead">Wir sind in ganz Nordrhein-Westfalen und darüber hinaus für Sie im Einsatz. Wählen Sie Ihre Stadt:</p>
<div class="chips">{links}</div>
<p class="lead" style="margin-top:1.5rem">Alle Preise auf einen Blick finden Sie auf unserer Seite <a href="/umzugskosten/" style="color:var(--primary);font-weight:700;text-decoration:underline">Umzugskosten &amp; Preise</a>.</p>
</div></section>'''

def hero(c, h1, sub, badge):
    return f'''<section class="hero"><div class="container">
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Startseite</a> › Umzugsunternehmen {e(c["name"])}</nav>
<span class="badge">{I["pin"]}{e(badge)}</span>
<h1>{e(h1)}</h1>
<p>{e(sub)}</p>
<div class="hero__actions">
  <a href="/calculator" class="btn btn--accent btn--lg">{I["calc"]}Kosten berechnen</a>
  <a href="{WA_URL}" target="_blank" rel="noopener noreferrer" class="btn btn--outline btn--lg">{I["wa"]}Angebot per WhatsApp</a>
</div>
<div class="hero__meta"><a href="{PHONE_TEL}">{I["phone"]}{PHONE_DISPLAY}</a><span>{I["pin"]}{e(c["name"])} &amp; Umgebung</span><span>{I["shield"]}Versicherter Transport</span></div>
</div></section>'''

# ---------------------------------------------------------------- template A (Essen)
def template_a(c):
    n, adj = c["name"], c["adj"]
    services = ["Privatumzüge", "Firmenumzüge", "Büroumzüge", "Seniorenumzüge", "Möbelmontage und Demontage",
                "Küchenmontage", "Verpackungsservice", "Entrümpelungen", "Haushaltsauflösungen", "Transportservice"]
    why = ["Transparente Festpreise", "Kostenlose Besichtigung", "Kurzfristige Termine",
           "Professionelle Umzugshelfer", "Versicherungsschutz für Ihr Umzugsgut", "Deutschlandweite Umzüge"]
    body = hero(c, f"Umzugsunternehmen {n} – Günstig, Professionell und Zuverlässig umziehen",
                f"Sie suchen ein zuverlässiges Umzugsunternehmen in {n}? SparUmzug unterstützt Privatpersonen, Familien, Senioren und Unternehmen bei Umzügen jeder Größenordnung.",
                f"Ihr Umzugsunternehmen in {n}")
    body += f'''<section class="section"><div class="container split">
<div class="prose">
<span class="eyebrow">Über uns</span>
<h2 class="h2">Ihr erfahrenes Umzugsunternehmen in {e(n)}</h2>
<p>Sie suchen ein zuverlässiges Umzugsunternehmen in {e(n)}? SparUmzug unterstützt Privatpersonen, Familien, Senioren und Unternehmen bei Umzügen jeder Größenordnung. Ob innerhalb von {e(n)}, {e(c["region"])} oder deutschlandweit – wir sorgen für einen reibungslosen und stressfreien Umzug.</p>
<p>Mit unserer langjährigen Erfahrung, fairen Preisen und professionellen Umzugshelfern gehören wir zu den zuverlässigen Ansprechpartnern für Umzüge in {e(n)} und Umgebung.</p>
</div>
{calc_card(n)}
</div></section>
<section class="section section--muted"><div class="container">
<span class="eyebrow">Leistungen</span>
<h2 class="h2">Unsere Leistungen in {e(n)}</h2>
<p class="lead">Ein erfolgreicher Umzug beginnt mit einer professionellen Planung. Deshalb bieten wir Ihnen ein umfassendes Leistungspaket:</p>
{chips(services)}
</div></section>
<section class="section section--card"><div class="container">
<span class="eyebrow">Einsatzgebiet</span>
<h2 class="h2">Umzüge in allen {e(adj)} Stadtteilen</h2>
<p class="lead">Wir sind in ganz {e(n)} tätig:</p>
{chips(c["districts"], "pin", "chip--district")}
</div></section>
<section class="section section--muted"><div class="container">
<span class="eyebrow">Ihre Vorteile</span>
<h2 class="h2">Warum SparUmzug in {e(n)}?</h2>
{checks(why, cols3=True)}
<p class="lead" style="margin-top:1.5rem">Unser Ziel ist es, Ihren Umzug in {e(n)} so einfach wie möglich zu gestalten.</p>
</div></section>
<section class="section section--card"><div class="container split">
<div class="prose">
<span class="eyebrow">Preise</span>
<h2 class="h2">Kosten für einen Umzug in {e(n)}</h2>
<p>Die Kosten hängen von Wohnungsgröße, Entfernung und Zusatzleistungen ab. Bereits kleine Umzüge können kostengünstig durchgeführt werden. Gerne erstellen wir Ihnen ein individuelles und unverbindliches Angebot.</p>
<p>Eine Übersicht unserer Einstiegspreise finden Sie auf der Seite <a href="/umzugskosten/" style="color:var(--primary);font-weight:700;text-decoration:underline">Umzugskosten &amp; Preise</a>. Für eine sofortige Schätzung nutzen Sie unseren Online-Kostenrechner.</p>
</div>
{calc_card(n)}
</div></section>
'''
    body += cta_block(f"Jetzt kostenloses Umzugsangebot in {n} anfordern",
                      f"Kontaktieren Sie SparUmzug noch heute und erhalten Sie eine faire und transparente Kostenschätzung für Ihren Umzug in {n}.")
    body += other_cities(c["slug"])
    return body

# ---------------------------------------------------------------- template B (Oberhausen)
def template_b(c):
    n = c["name"]
    services = ["Privatumzüge", "Firmenumzüge", "Möbeltransporte", "Seniorenumzüge", "Haushaltsauflösungen",
                "Entrümpelungen", "Möbelmontagen", "Verpackungsservice"]
    adv = [("euro", "Faire und transparente Preise", "Bei uns erhalten Sie eine klare Kostenübersicht ohne versteckte Gebühren."),
           ("users", "Erfahrene Umzugshelfer", "Unser Team behandelt Ihre Möbel und persönlichen Gegenstände mit größter Sorgfalt."),
           ("clock", "Flexible Terminvergabe", "Auch kurzfristige Umzugstermine sind nach Verfügbarkeit möglich."),
           ("truck", "Moderne Fahrzeuge", "Unsere Transportfahrzeuge sind für kleine und große Umzüge optimal ausgestattet.")]
    cards = "".join(f'<div class="card"><div class="card__icon">{I[i]}</div><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i, t, p in adv)
    body = hero(c, f"Umzugsunternehmen {n} – Ihr zuverlässiger Partner für stressfreie Umzüge",
                f"Als erfahrenes Umzugsunternehmen in {n} übernimmt SparUmzug sämtliche Aufgaben rund um Ihren Wohnungs- oder Firmenumzug.",
                f"Umzüge in {n} und Umgebung")
    body += f'''<section class="section"><div class="container split">
<div class="prose">
<span class="eyebrow">Über uns</span>
<h2 class="h2">Professionelle Umzüge in {e(n)}</h2>
<p>Ein Umzug bedeutet oft viel Organisation und Zeitaufwand. Als erfahrenes Umzugsunternehmen in {e(n)} übernimmt SparUmzug sämtliche Aufgaben rund um Ihren Wohnungs- oder Firmenumzug.</p>
<p>Wir unterstützen Sie von der Planung bis zur Durchführung und sorgen dafür, dass Ihr Umzug sicher und termingerecht erfolgt.</p>
</div>
{calc_card(n)}
</div></section>
<section class="section section--muted"><div class="container">
<span class="eyebrow">Leistungen</span>
<h2 class="h2">Unsere Leistungen in {e(n)}</h2>
<p class="lead">Für unsere Kunden in {e(n)} bieten wir:</p>
{chips(services)}
</div></section>
<section class="section section--card"><div class="container">
<span class="eyebrow">Einsatzgebiet</span>
<h2 class="h2">Umzugsservice in allen Stadtteilen</h2>
<p class="lead">Wir sind in ganz {e(n)} für Sie tätig:</p>
{chips(c["districts"], "pin", "chip--district")}
</div></section>
<section class="section section--muted"><div class="container">
<span class="eyebrow">Ihre Vorteile</span>
<h2 class="h2">Ihre Vorteile mit SparUmzug</h2>
<div class="grid grid--4" style="margin-top:1.5rem">{cards}</div>
</div></section>
<section class="section section--card"><div class="container split">
<div class="prose">
<span class="eyebrow">Entrümpelung</span>
<h2 class="h2">Entrümpelung und Haushaltsauflösung in {e(n)}</h2>
<p>Neben klassischen Umzügen übernehmen wir auch professionelle Entrümpelungen von Wohnungen, Häusern, Kellern, Garagen und Gewerbeobjekten.</p>
<p>Unsere Einstiegspreise für Umzüge, Entrümpelungen und Zusatzleistungen finden Sie auf der Seite <a href="/umzugskosten/" style="color:var(--primary);font-weight:700;text-decoration:underline">Umzugskosten &amp; Preise</a>.</p>
</div>
<div class="card"><div class="card__icon">{I["trash"]}</div><h3>Fachgerechte Entsorgung</h3><p>Wohnungen, Häuser, Keller, Garagen und Gewerbeobjekte – wir räumen, sortieren und entsorgen fachgerecht.</p><p style="margin-top:1rem"><a href="/contact" class="btn btn--primary">Entrümpelung anfragen</a></p></div>
</div></section>
'''
    body += cta_block(f"Jetzt Angebot für Ihren Umzug in {n} sichern",
                      "Fordern Sie noch heute ein kostenloses und unverbindliches Angebot an. Wir beraten Sie persönlich und finden die passende Lösung für Ihren Umzug.")
    body += other_cities(c["slug"])
    return body

# ---------------------------------------------------------------- template C (Düsseldorf)
def template_c(c):
    n = c["name"]
    services = ["Wohnungsumzügen", "Hausumzügen", "Büroumzügen", "Firmenumzügen", "Seniorenumzügen",
                "Möbeltransporten", "Entrümpelungen", "Haushaltsauflösungen", "Möbelmontage"]
    why = [("clock", "Schnelle Angebotserstellung", "Wir erstellen Ihnen kurzfristig ein unverbindliches Angebot."),
           ("star", "Hohe Kundenzufriedenheit", "Freundlichkeit, Zuverlässigkeit und Sorgfalt stehen bei uns an erster Stelle."),
           ("users", "Individuelle Lösungen", "Jeder Umzug wird individuell geplant und auf Ihre Bedürfnisse abgestimmt."),
           ("euro", "Starke Preis-Leistung", "Wir bieten günstige Preise ohne Qualitätsverlust.")]
    cards = "".join(f'<div class="card"><div class="card__icon">{I[i]}</div><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i, t, p in why)
    if c["slug"] == "duesseldorf":
        intro1 = "Düsseldorf gehört zu den gefragtesten Wohn- und Wirtschaftsstandorten Deutschlands. Wenn Sie einen Umzug innerhalb Düsseldorfs oder in eine andere Stadt planen, benötigen Sie ein erfahrenes Umzugsunternehmen."
    else:
        intro1 = f"{n} gehört zu den gefragten Wohn- und Wirtschaftsstandorten {c['regionName']}. Wenn Sie einen Umzug innerhalb von {n} oder in eine andere Stadt planen, benötigen Sie ein erfahrenes Umzugsunternehmen."
    body = hero(c, f"Umzugsunternehmen {n} – Professionelle Umzüge zum fairen Preis",
                f"SparUmzug bietet Ihnen professionelle Umzugslösungen für Privatpersonen, Familien und Unternehmen in {n} zu fairen Preisen.",
                f"Ihr Umzug in {n} mit SparUmzug")
    body += f'''<section class="section"><div class="container split">
<div class="prose">
<span class="eyebrow">Über uns</span>
<h2 class="h2">Ihr Umzug in {e(n)} mit SparUmzug</h2>
<p>{e(intro1)}</p>
<p>SparUmzug bietet Ihnen professionelle Umzugslösungen für Privatpersonen, Familien und Unternehmen zu fairen Preisen.</p>
</div>
{calc_card(n)}
</div></section>
<section class="section section--muted"><div class="container">
<span class="eyebrow">Leistungen</span>
<h2 class="h2">Unsere Umzugsleistungen in {e(n)}</h2>
<p class="lead">Wir unterstützen Sie bei:</p>
{chips(services)}
</div></section>
<section class="section section--card"><div class="container">
<span class="eyebrow">Einsatzgebiet</span>
<h2 class="h2">Umzüge in allen {e(c["adj"])} Stadtteilen</h2>
<p class="lead">Unser Service ist in allen Bezirken verfügbar:</p>
{chips(c["districts"], "pin", "chip--district")}
</div></section>
<section class="section section--muted"><div class="container">
<span class="eyebrow">Ihre Vorteile</span>
<h2 class="h2">Warum Kunden aus {e(n)} SparUmzug wählen</h2>
<div class="grid grid--4" style="margin-top:1.5rem">{cards}</div>
</div></section>
<section class="section section--card"><div class="container grid grid--2" style="gap:2rem">
<div class="card"><div class="card__icon">{I["building"]}</div><h3>Firmenumzüge in {e(n)}</h3><p>Wir unterstützen Unternehmen jeder Größe bei Standortwechseln und Büroumzügen. Unsere erfahrenen Mitarbeiter sorgen dafür, dass Ausfallzeiten minimiert werden und der Geschäftsbetrieb schnell wieder aufgenommen werden kann.</p></div>
<div class="card"><div class="card__icon">{I["trash"]}</div><h3>Entrümpelungen in {e(n)}</h3><p>Neben Umzügen übernehmen wir professionelle Entrümpelungen von Wohnungen, Häusern, Kellern, Garagen und Gewerbeobjekten inklusive fachgerechter Entsorgung.</p></div>
</div></section>
<section class="section section--muted"><div class="container split">
<div class="prose">
<span class="eyebrow">Preise</span>
<h2 class="h2">Was kostet ein Umzug in {e(n)}?</h2>
<p>Die Kosten hängen von Wohnungsgröße, Umzugsvolumen, Entfernung und gewünschten Zusatzleistungen ab. Unsere Einstiegspreise finden Sie auf der Seite <a href="/umzugskosten/" style="color:var(--primary);font-weight:700;text-decoration:underline">Umzugskosten &amp; Preise</a> – oder Sie berechnen Ihre Kosten direkt online.</p>
</div>
{calc_card(n)}
</div></section>
'''
    body += cta_block(f"Kostenloses Angebot für Ihren Umzug in {n}",
                      f"Planen Sie einen Umzug in {n}? Kontaktieren Sie SparUmzug und lassen Sie sich unverbindlich beraten.")
    body += other_cities(c["slug"])
    return body

TEMPLATES = {"A": template_a, "B": template_b, "C": template_c}
TITLES = {"A": "Umzugsunternehmen {n} – Günstig, Professionell und Zuverlässig umziehen | SparUmzug",
          "B": "Umzugsunternehmen {n} – Ihr zuverlässiger Partner für stressfreie Umzüge | SparUmzug",
          "C": "Umzugsunternehmen {n} – Professionelle Umzüge zum fairen Preis | SparUmzug"}

def city_page(c):
    n = c["name"]
    url = f"{BASE_URL}/umzugsunternehmen-{c['slug']}/"
    desc = (f"Umzugsunternehmen {n}: SparUmzug bietet günstige Privat- und Firmenumzüge, Entrümpelungen und Möbeltransporte in {n} und Umgebung. "
            f"Kostenloses Angebot, faire Preise und Online-Kostenrechner.")
    jsonld = {
        "@context": "https://schema.org", "@type": "MovingCompany", "name": "SparUmzug",
        "url": url, "telephone": "+49-176-66879641", "email": EMAIL, "priceRange": "€€",
        "description": f"Umzugsunternehmen in {n} – Privatumzüge, Firmenumzüge, Entrümpelungen und Möbeltransporte.",
        "address": {"@type": "PostalAddress", "addressLocality": "Moers", "addressRegion": "NRW", "addressCountry": "DE"},
        "areaServed": [{"@type": "City", "name": n}] + [{"@type": "Place", "name": f"{n} {d}" if d != n else d} for d in c["districts"]],
    }
    return page(title=TITLES[c["template"]].format(n=n), description=desc, canonical=url,
                body=TEMPLATES[c["template"]](c), jsonld=jsonld, active=None)

# ---------------------------------------------------------------- Preise page
def preise_page():
    url = f"{BASE_URL}/umzugskosten/"
    def price_card(title, price, fit, leist, featured=False):
        li = lambda xs: "".join("<li>" + I["check"] + e(x) + "</li>" for x in xs)
        fit_html = "<h4>Geeignet für</h4><ul>" + li(fit) + "</ul>" if fit else ""
        feat = " price-card--featured" if featured else ""
        return f'''<div class="price-card{feat}">
<h3>{e(title)}</h3><div class="price">ab {price} €<small>*</small></div>
{fit_html}<h4>Leistungen</h4><ul>{li(leist)}</ul>
<div class="btn-wrap"><a href="/calculator" class="btn btn--primary" style="width:100%">Kosten berechnen</a></div></div>'''
    cards = (price_card("1-Zimmer-Umzug", "249", ["Studentenwohnungen", "Apartments", "Single-Haushalte"],
                        ["Transportfahrzeug", "Be- und Entladen", "Sicherer Möbeltransport"])
             + price_card("2-Zimmer-Umzug", "449", [], ["Umzugshelfer", "Transportfahrzeug", "Möbeltransport", "Standardausstattung"], featured=True)
             + price_card("3-Zimmer-Umzug", "699", [], ["Mehrere Umzugshelfer", "Größeres Fahrzeug", "Fachgerechter Transport"])
             + price_card("4-Zimmer-Umzug oder Haus", "999", [], ["Komplettservice", "Professioneller Möbeltransport", "Individuelle Umzugsplanung"]))
    hourly = [("2 Helfer + Transporter", "69 € bis 79 € pro Stunde*"), ("3 Helfer + LKW", "89 € bis 109 € pro Stunde*"), ("4 Helfer + LKW", "ab 119 € pro Stunde*")]
    extras = [("Küchenmontage", "ab 99 €*"), ("Verpackungsservice", "ab 49 €*"), ("Halteverbotszone", "ab 80 €*"),
              ("Möbellift / Außenaufzug", "auf Anfrage*"), ("Endreinigung", "ab 149 €*"), ("Entrümpelung", "ab 18 €/m³*")]
    def table(rows, h1, h2):
        return f'<div class="table-wrap"><table class="rate-table"><thead><tr><th>{h1}</th><th>{h2}</th></tr></thead><tbody>' + \
               "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in rows) + "</tbody></table></div>"
    factors = ["Wohnungsgröße", "Umzugsvolumen", "Entfernung", "Anzahl der Etagen", "Aufzug vorhanden oder nicht", "Laufwege zum Fahrzeug",
               "Möbelmontagen", "Verpackungsservice", "Halteverbotszone", "Entrümpelungsarbeiten", "Sondertransporte (z. B. Klaviere, Tresore)"]
    zusatz = ["Halteverbotszonen", "Möbellifte", "Lange Tragewege", "Zusätzliche Etagen ohne Aufzug", "Entsorgungskosten",
              "Behördliche Gebühren", "Verpackungsmaterial", "Wartezeiten aufgrund von Zugangsproblemen"]
    faq = [("Was kostet ein Umzug in NRW?", "Die Kosten hängen von Wohnungsgröße, Entfernung, Umzugsvolumen und gewünschten Zusatzleistungen ab."),
           ("Sind die Preise verbindlich?", "Nur ein schriftlich bestätigter Festpreis ist verbindlich. Ein Kostenvoranschlag dient grundsätzlich der Orientierung."),
           ("Kann ich ein kostenloses Angebot erhalten?", "Ja. Die Angebotserstellung ist bei SparUmzug kostenlos und unverbindlich."),
           ("Gibt es versteckte Kosten?", "Nein. Alle bekannten Kosten werden vor Auftragsbeginn transparent kommuniziert.")]
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    ul = lambda xs, two=False: f'<ul class="bullets{" bullets--2" if two else ""}">' + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ul>"

    body = f'''<section class="hero"><div class="container">
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Startseite</a> › Umzugskosten &amp; Preise</nav>
<span class="badge">{I["euro"]}Umzugskosten &amp; Preise</span>
<h1>Transparente Preise für Ihren Umzug</h1>
<p>Sie möchten wissen, was ein Umzug kostet? Bei SparUmzug erhalten Sie faire und transparente Preise für Umzüge, Entrümpelungen, Haushaltsauflösungen und Möbeltransporte.</p>
<div class="hero__actions">
  <a href="/calculator" class="btn btn--accent btn--lg">{I["calc"]}Kosten berechnen</a>
  <a href="{WA_URL}" target="_blank" rel="noopener noreferrer" class="btn btn--outline btn--lg">{I["wa"]}Angebot per WhatsApp</a>
</div>
<div class="hero__meta"><a href="{PHONE_TEL}">{I["phone"]}{PHONE_DISPLAY}</a><a href="mailto:{EMAIL}">{I["mail"]}{EMAIL}</a></div>
</div></section>

<section class="section"><div class="container split">
<div class="prose">
<span class="eyebrow">Unser Versprechen</span>
<h2 class="h2">Nachvollziehbare Preise ohne versteckte Kosten</h2>
<p>Wir legen großen Wert auf eine nachvollziehbare Preisgestaltung ohne versteckte Kosten. Auf Basis Ihrer Angaben erstellen wir Ihnen ein individuelles und unverbindliches Angebot.</p>
{checks(["Kostenlose Angebotserstellung", "Transparente Kalkulation", "Keine versteckten Gebühren", "Professionelle Umzugshelfer", "Versicherter Transport", "Kurzfristige Termine möglich"])}
</div>
{calc_card()}
</div></section>

<section class="section section--muted"><div class="container center">
<span class="eyebrow">Preisübersicht</span>
<h2 class="h2">Preisübersicht für Umzüge</h2>
<p class="lead">Einstiegspreise für Standardleistungen – der genaue Preis richtet sich nach Ihrem individuellen Umzug.</p>
<div class="grid grid--4" style="margin-top:2.5rem;text-align:left">{cards}</div>
</div></section>

<section class="section section--card"><div class="container grid grid--2" style="gap:2.5rem">
<div><span class="eyebrow">Stundenpreise</span><h2 class="h2">Stundenpreise</h2>{table(hourly, "Team", "Preis")}</div>
<div><span class="eyebrow">Zusatzleistungen</span><h2 class="h2">Weitere Leistungen</h2>{table(extras, "Leistung", "Preis")}</div>
</div></section>

<section class="section section--muted"><div class="container grid grid--2" style="gap:2.5rem">
<div><span class="eyebrow">Kostenfaktoren</span><h2 class="h2">Was beeinflusst die Umzugskosten?</h2><p class="lead">Der endgültige Preis richtet sich nach mehreren Faktoren:</p>{ul(factors, True)}</div>
<div><span class="eyebrow">Zusatzkosten</span><h2 class="h2">Mögliche Zusatzkosten</h2><p class="lead">Je nach individueller Situation können zusätzliche Leistungen erforderlich sein. Hierzu zählen beispielsweise:</p>{ul(zusatz)}
<p class="lead" style="margin-top:1rem">Solche Positionen werden vor Auftragsbeginn transparent mit Ihnen abgestimmt. Diese Kostenarten werden auch in Ihren Angebots- und Auftragsunterlagen als mögliche Zusatzkosten ausgewiesen.</p></div>
</div></section>

<section class="section section--card"><div class="container">
<span class="eyebrow">Gut zu wissen</span>
<h2 class="h2">Festpreis oder Kostenvoranschlag?</h2>
<div class="grid grid--2" style="margin-top:1.5rem">
<div class="card"><div class="card__icon">{I["shield"]}</div><h3>Festpreis</h3><p>Bei einem ausdrücklich vereinbarten Festpreis bleibt der Preis unverändert, sofern sich der Leistungsumfang nicht ändert.</p></div>
<div class="card"><div class="card__icon">{I["euro"]}</div><h3>Unverbindlicher Kostenvoranschlag</h3><p>Ein Kostenvoranschlag basiert auf den vorliegenden Informationen und dient der Preisorientierung. Änderungen des Umzugsvolumens oder der Leistungen können zu Mehr- oder Minderkosten führen. Ein entsprechender Hinweis ist auch in Ihrer Kostenvoranschlagsvorlage enthalten.</p></div>
</div>
</div></section>

<section class="section section--muted"><div class="container grid grid--2" style="gap:2.5rem">
<div><span class="eyebrow">FAQ</span><h2 class="h2">Häufig gestellte Fragen zu den Preisen</h2><div class="faq">{faq_html}</div></div>
<div style="display:grid;gap:1.25rem;align-content:start">
<div class="note"><strong>Wichtiger Hinweis zum Preisrechner</strong><p>Die Berechnung dient ausschließlich der unverbindlichen Orientierung und stellt kein verbindliches Angebot dar. Ein verbindlicher Preis wird nach Prüfung Ihrer Angaben und des tatsächlichen Leistungsumfangs erstellt.</p></div>
<div class="note"><strong>Rechtlicher Hinweis</strong><p>* Alle genannten Preise sind Beispiel- bzw. Einstiegspreise für Standardleistungen. Der tatsächliche Preis hängt insbesondere von Umzugsvolumen, Entfernung, Etagen, Laufwegen, Zusatzleistungen und den örtlichen Gegebenheiten ab. Die angegebenen Preise dienen der Orientierung und ersetzen kein individuelles Angebot.</p></div>
{calc_card()}
</div>
</div></section>

<section class="section cta"><div class="container">
<h2 class="h2">Jetzt kostenloses Angebot anfordern</h2>
<p>Kostenlos, unverbindlich und mit schneller Rückmeldung – wir freuen uns auf Ihre Anfrage.</p>
<div class="cta__actions">
  <a href="{PHONE_TEL}" class="btn btn--accent btn--lg">{I["phone"]}Telefon: {PHONE_DISPLAY}</a>
  <a href="{WA_URL}" target="_blank" rel="noopener noreferrer" class="btn btn--whatsapp btn--lg">{I["wa"]}Angebot per WhatsApp anfordern</a>
  <a href="mailto:{EMAIL}" class="btn btn--outline btn--lg">{I["mail"]}{EMAIL}</a>
</div>
{checks(["Kostenlos", "Unverbindlich", "Schnelle Rückmeldung", "Faire Preise"])}
</div></section>
'''
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": "Umzugskosten & Preise | SparUmzug", "url": url,
         "description": "Was kostet ein Umzug? Transparente Umzugspreise für Privat- und Firmenumzüge. Faire Preise, kostenloses Angebot und professionelle Umzugshelfer von SparUmzug."},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "MovingCompany", "name": "SparUmzug", "url": BASE_URL, "telephone": "+49-176-66879641", "email": EMAIL, "priceRange": "€€",
         "address": {"@type": "PostalAddress", "addressLocality": "Moers", "addressRegion": "NRW", "addressCountry": "DE"}}]}
    return page(title="Umzugskosten & Preise | SparUmzug",
                description="Was kostet ein Umzug? Transparente Umzugspreise für Privat- und Firmenumzüge. Faire Preise, kostenloses Angebot und professionelle Umzugshelfer von SparUmzug.",
                canonical=url, body=body, jsonld=jsonld, active="/umzugskosten/")

# ---------------------------------------------------------------- SPA routes
# Hostinger serves its own 404 for /calculator, /about, ... when the .htaccess
# rewrite isn't active (Search Console "Nicht gefunden (404)", Oct 2026).
# Fix that doesn't depend on .htaccess: give every SPA route a real
# <route>/index.html = copy of the SPA shell with its own title/description/
# canonical. The server 301s /about -> /about/; a tiny inline script strips
# the slash again so the React router + active nav state see "/about".
SPA_ROUTES = {
    "about":       ("Über Uns | SparUmzug – Umzugsunternehmen aus Moers",
                    "Lernen Sie SparUmzug kennen: Ihr zuverlässiges Umzugsunternehmen aus Moers für Umzüge, Transporte und Entrümpelungen in NRW und ganz Deutschland."),
    "services":    ("Leistungen | Umzug, Montage, Verpackung & Entrümpelung – SparUmzug",
                    "Umzüge, Möbelmontage, Verpackungsservice, Reinigung und Entrümpelung aus einer Hand. Faire Festpreise ab 0,60 € pro Kilometer."),
    "calculator":  ("Umzugskostenrechner | Umzugskosten online berechnen – SparUmzug",
                    "Berechnen Sie Ihre Umzugskosten in wenigen Schritten: Wohnungsgröße, Entfernung, Etagen, Möbel und Zusatzleistungen. Kostenlos und unverbindlich."),
    "contact":     ("Kontakt | Kostenloses Umzugsangebot anfordern – SparUmzug",
                    "Kontaktieren Sie SparUmzug per Telefon, WhatsApp oder E-Mail und erhalten Sie Ihr kostenloses, unverbindliches Umzugsangebot."),
    "impressum":   ("Impressum | SparUmzug", "Impressum und Anbieterkennzeichnung von SparUmzug – Umzug & Entrümpelung, Moers."),
    "agb":         ("AGB | SparUmzug", "Allgemeine Geschäftsbedingungen von SparUmzug – Umzug & Entrümpelung."),
    "widerruf":    ("Widerrufsbelehrung | SparUmzug", "Widerrufsbelehrung und Widerrufsformular von SparUmzug – Umzug & Entrümpelung."),
    "datenschutz": ("Datenschutzerklärung | SparUmzug", "Datenschutzerklärung von SparUmzug – Umzug & Entrümpelung."),
}

def build_spa_routes():
    import re
    shell = (ROOT / "index.html").read_text(encoding="utf-8")
    out = []
    for slug, (title, desc) in SPA_ROUTES.items():
        url = f"{BASE_URL}/{slug}/"
        h = shell
        h = re.sub(r"<title>.*?</title>", f"<title>{e(title)}</title>", h, count=1)
        h = re.sub(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{e(desc)}" />', h, count=1)
        h = re.sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{url}" />', h, count=1)
        h = re.sub(r'<meta property="og:title" content="[^"]*" />', f'<meta property="og:title" content="{e(title)}" />', h, count=1)
        h = re.sub(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{e(desc)}" />', h, count=1)
        h = h.replace('<script type="module"',
                      f'<script>if(location.pathname==="/{slug}/")history.replaceState(null,"","/{slug}"+location.search+location.hash)</script>\n    <script type="module"', 1)
        assert h.count(url) == 1 and f"<title>{e(title)}</title>" in h, slug
        d = ROOT / slug
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(h, encoding="utf-8")
        out.append(f"/{slug}/")
    return out

# ---------------------------------------------------------------- build
def main():
    written = []
    for c in CITIES:
        d = ROOT / f"umzugsunternehmen-{c['slug']}"
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(city_page(c), encoding="utf-8")
        written.append(f"/umzugsunternehmen-{c['slug']}/")
    (ROOT / "umzugskosten").mkdir(exist_ok=True)
    (ROOT / "umzugskosten" / "index.html").write_text(preise_page(), encoding="utf-8")
    written.append("/umzugskosten/")

    spa = ["/"] + build_spa_routes()
    urls = "".join(f"  <url><loc>{BASE_URL}{p}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in spa + written)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    print(f"built {len(written)} pages + sitemap.xml")

if __name__ == "__main__":
    main()
