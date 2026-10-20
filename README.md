# SparUmzug — website deliveries

Site for SparUmzug / MAE Umzug & Entrümpelung (live: https://mae-umzug-entruempelung.de,
preview: https://spar-umzug.vercel.app). Built with Lovable — **no source code exists**,
only the compiled bundle, so all changes are patched into the minified JS and new pages
are added as static HTML next to the SPA.

## Folders
- `website/` — the full site, ready to serve (upload contents to Hostinger `public_html/`)
- `sparumzug-deploy-oct21.zip` — current deployment zip; `sparumzug-deploy-sept16.zip` — previous (files at zip root, incl. .htaccess)
- `sparumzug-deploy-july26.zip` — previous (July 26) deployment, kept as rollback
- `backup-live-2026-07-26/` — the site as it was live before July 26
- `tools/` — reproducible build scripts:
  - `patch-bundle.py` — applies all price/WhatsApp/footer patches to
    `src-bundle-july26.js` → `website/assets/index-mae-v3.js`
  - `build-pages.py` + `cities.json` — generates the 23 city pages, the Preise page
    and `sitemap.xml` (edit cities.json / templates, re-run)
  - `whatsapp-message.txt` — the pre-filled WhatsApp text (shared by both scripts)
  - `serve.js` — local preview with SPA fallback (`node tools/serve.js` → :8765)
- `whatsapp-autoreply-for-client.txt` — the auto-reply text the client must paste into
  WhatsApp Business (cannot be set from the website)

## Delivery 2026-10-21 (client screenshots) — `sparumzug-deploy-oct21.zip`
- **Search Console "Nicht gefunden (404)"**: live Hostinger returned 404 for every SPA route
  (/calculator, /about, …) because the .htaccess rewrite wasn't active — and sitemap.xml listed them.
  Fix: `build-pages.py` now writes `<route>/index.html` (SPA shell with own title/description/
  canonical) for all 8 SPA routes; sitemap uses `/route/` URLs; .htaccess adds `ErrorDocument 404`.
  Homepage canonical/JSON-LD moved from deutschland-sparumzug.de to mae-umzug-entruempelung.de.
- **Calculator**: Parkplatz-Entfernung split into Beladestelle (Auszug) + Entladestelle (Einzug),
  1 €/m each; Wohnzimmer + Stuhl (5 €) + Fernseher (20 €, Mit/Ohne Montage toggle);
  quote e-mail now shows both distances and the Montage choice (also for kitchen items).
- Bundle renamed `index-mae-v4.js` (cache-bust).

## Delivery 2026-09-16 (client PDF "Aenderung Sf7ah")

### Calculator prices (homepage estimator + /calculator)
| Item | Old | New |
|---|---|---|
| Entfernung pro km | 0,75 € | **0,60 €** |
| Etage mit Aufzug (pro Etage, je Adresse) | 30 € | **20 €** |
| Etage ohne Aufzug (pro Etage, je Adresse) | 50 € | **30 €** |
| Montage / Demontage | 150 € | **80 €** |
| Verpackung / Einpacken / Umwickeln / Auspacken | 100 € | **80 €** |
| Reinigung | 100 € | 100 € (unchanged, per client) |
| Entrümpelung | 200 € | 200 € (unchanged, per client) |
| Halteverbotszone (je Adresse) | 150 € | **80 €** (aligned with new price page "ab 80 €") |
| Möbelinventar | — | **−10 € each**; items already ≤ 10 € unchanged (52 lowered, 21 kept) |
| Grundkosten | 150 € | 150 € (unchanged) |
| Küche Teil/Komplett, Kartons, Parkabstand | — | unchanged |

Also fixed stale labels on /services: "Ab €1,50/km" → "Ab €0,60/km" (DE + EN).

### New pages (static HTML, same look as the SPA)
- `/umzugskosten/` — Preise page (PDF pages 7–11, incl. FAQ schema)
- `/umzugsunternehmen-<stadt>/` — 23 city pages using the 3 PDF templates
  (A = Essen, B = Oberhausen, C = Düsseldorf; other cities rotate A/B/C).
  Every page links to `/calculator` (hero button, calculator card ×2, CTA band)
  and to the Preise page, and lists the other cities.
- `sitemap.xml` (+ referenced in robots.txt)

### Navigation
- SPA footer: new "Umzugsunternehmen in Ihrer Stadt" row (all 23 cities) + "Preise"
- SPA mobile menu: "Preise". Desktop nav intentionally NOT changed — a 6th link
  overflows the header at ≤1440 px.

### WhatsApp
- Floating button + footer icon now open WhatsApp with a pre-filled quote checklist
  (see `tools/whatsapp-message.txt`).
- The client's "Automatische Antwort" text is delivered in
  `whatsapp-autoreply-for-client.txt` — it must be set in WhatsApp Business.

## Delivery 2026-07-26
Prices: Grundkosten flat 150 €, 0,75 €/km, Verpackung/Einpacken/Auspacken/Umwickeln/
Reinigung 100 €, all furniture −5 €. Favicon replaced with the "SU" logo.
