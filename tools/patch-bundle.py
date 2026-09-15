#!/usr/bin/env python3
"""
Patch the minified SparUmzug bundle (no source exists — Lovable build).
Input : tools/src-bundle-july26.js  (July-26 build, unpatched source of truth)
Output: website/assets/index-mae-v3.js    (Sept-16 build)

Changes (client request 2026-09-16):
  1. Entfernung 0,75 €/km  -> 0,60 €/km (homepage estimator + calculator)
  2. Etagenzuschlag pro Etage: mit Aufzug 30 -> 20 €, ohne Aufzug 50 -> 30 €
  3. Zusätzliche Leistungen 80 € each (Montage/Demontage 150->80,
     Verpackung/Einpacken/Umwickeln/Auspacken 100->80); Reinigung 100 and
     Entrümpelung 200 unchanged
  4. Möbelinventar: every item -10 €, items already <= 10 € stay fixed
  5. Halteverbotszone 150 -> 80 € (aligns with new price page "ab 80 €")
  6. Services page label "Ab €1,50/km" -> "Ab €0,60/km" (EN too)
  7. WhatsApp float button: new pre-filled message (quote checklist)
  8. Mobile nav: "Preise" link (-> /umzugskosten/), footer: Preise + Standorte row
"""
import re, sys, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent / "website"
SRC = HERE / "src-bundle-july26.js"
DST = ROOT / "assets" / "index-mae-v3.js"
s = SRC.read_text(encoding="utf-8")
orig = s

def rep(old, new, count):
    global s
    n = s.count(old)
    assert n == count, f"expected {count} of {old!r}, found {n}"
    s = s.replace(old, new)

# 1. km price ------------------------------------------------------------
rep('t*.75', 't*.6', 2)          # homepage estimator (calc + label)
rep('const re=i*.75;', 'const re=i*.6;', 1)   # calculator page

# 2. floors --------------------------------------------------------------
rep('const ut=d>0?w?d*30:d*50:0,ue=m>0?b?m*30:m*50:0',
    'const ut=d>0?w?d*20:d*30:0,ue=m>0?b?m*20:m*30:0', 1)

# 3. additional services -------------------------------------------------
rep('p.includes("assembly")&&(Pe+=150),p.includes("disassembly")&&(Pe+=150),'
    'p.includes("packaging")&&(Pe+=100),p.includes("packing")&&(Pe+=100),'
    'p.includes("wrapping")&&(Pe+=100),p.includes("unpacking")&&(Pe+=100),'
    'p.includes("cleaning")&&(Pe+=100),p.includes("clearance")&&(Pe+=200)',
    'p.includes("assembly")&&(Pe+=80),p.includes("disassembly")&&(Pe+=80),'
    'p.includes("packaging")&&(Pe+=80),p.includes("packing")&&(Pe+=80),'
    'p.includes("wrapping")&&(Pe+=80),p.includes("unpacking")&&(Pe+=80),'
    'p.includes("cleaning")&&(Pe+=100),p.includes("clearance")&&(Pe+=200)', 1)

# 5. Halteverbot ---------------------------------------------------------
rep('let Tr=0;R&&(Tr+=150),I&&(Tr+=150);', 'let Tr=0;R&&(Tr+=80),I&&(Tr+=80);', 1)

# 4. inventory: -10 € on every item > 10 €, <= 10 stays --------------------
start = s.index('[M,A]=v.useState([{id:"bedroom"')
end = s.index(']),[R,U]=v.useState(!1)', start)
inv = s[start:end]
changed = []
def lower(m):
    p = int(m.group(1))
    np_ = p - 10 if p > 10 else p
    changed.append((p, np_))
    return f'price:{np_},'
inv_new = re.sub(r'price:(\d+),', lower, inv)
assert len(changed) == 73, len(changed)
s = s[:start] + inv_new + s[end:]

# 6. services page km label ------------------------------------------------
rep('pricing:"Ab €1,50/km"', 'pricing:"Ab €0,60/km"', 1)
rep('pricing:"From €1.50/km"', 'pricing:"From €0.60/km"', 1)
rep('"Transparente Preise (€1,50/km)"', '"Transparente Preise (0,60 €/km)"', 1)
rep('"Transparent pricing (€1.50/km)"', '"Transparent pricing (€0.60/km)"', 1)
rep('"Entfernungsbasierte Preise (1,00 € – 1,50 € pro Kilometer)"', '"Entfernungsbasierte Preise (0,60 € pro Kilometer)"', 1)
rep('"Distance-based pricing (€1.00–€1.50 per kilometer)"', '"Distance-based pricing (€0.60 per kilometer)"', 1)

# 7. WhatsApp pre-filled message ------------------------------------------
wa_msg = (pathlib.Path(__file__).parent / "whatsapp-message.txt").read_text(encoding="utf-8").strip().replace("\n", "\\n")
rep('encodeURIComponent("Hallo! Ich interessiere mich für Ihre Umzugsservices.")',
    f'encodeURIComponent("{wa_msg}")', 1)
# footer WhatsApp icon: same pre-filled text
rep('href:"https://wa.me/4917666879641",target:"_blank"',
    f'href:"https://wa.me/4917666879641?text="+encodeURIComponent("{wa_msg}"),target:"_blank"', 1)

# 8. nav + footer links ------------------------------------------------------
cities = json.loads((pathlib.Path(__file__).parent / "cities.json").read_text(encoding="utf-8"))
link_cls = "text-primary-foreground/80 hover:text-accent transition-colors duration-200 text-sm"
city_links = ",".join(
    f'a.jsx("a",{{href:"/umzugsunternehmen-{c["slug"]}/",className:"{link_cls}",children:"Umzugsunternehmen {c["name"]}"}},"{c["slug"]}")'
    for c in cities)
standorte = ('a.jsxs("div",{className:"mt-16 pt-8 border-t border-primary-foreground/20",children:['
             'a.jsx("h4",{className:"font-display font-bold text-lg mb-6",children:"Umzugsunternehmen in Ihrer Stadt"}),'
             f'a.jsx("div",{{className:"flex flex-wrap gap-4",children:[{city_links}]}})]}}),')
rep('a.jsx("div",{className:"mt-16 pt-8 border-t border-primary-foreground/20",children:a.jsxs("div",{className:"flex flex-col md:flex-row justify-between items-center gap-4"',
    standorte + 'a.jsx("div",{className:"mt-16 pt-8 border-t border-primary-foreground/20",children:a.jsxs("div",{className:"flex flex-col md:flex-row justify-between items-center gap-4"', 1)

# footer quick links: add Preise (plain <a>, it's a static page outside the SPA router)
rep('children:t.map(r=>a.jsx("li",{children:a.jsx(Ae,{to:r.href,className:"text-primary-foreground/80 hover:text-accent transition-colors duration-200",children:e(r.labelKey)})},r.href))})',
    'children:[t.map(r=>a.jsx("li",{children:a.jsx(Ae,{to:r.href,className:"text-primary-foreground/80 hover:text-accent transition-colors duration-200",children:e(r.labelKey)})},r.href)),'
    'a.jsx("li",{children:a.jsx("a",{href:"/umzugskosten/",className:"text-primary-foreground/80 hover:text-accent transition-colors duration-200",children:"Preise"})},"preise")]})', 1)

# desktop nav: NOT patched — "Preise" makes the nav overflow at <=1440px; it lives in the mobile menu + footer instead
# mobile nav
rep('children:[o.map(i=>a.jsx(Ae,{to:i.href,onClick:()=>t(!1),className:`px-4 py-3 rounded-lg font-medium transition-all duration-200 ${s(i.href)?"bg-primary text-primary-foreground":"text-foreground hover:bg-muted"}`,children:i.label},i.href)),',
    'children:[o.map(i=>a.jsx(Ae,{to:i.href,onClick:()=>t(!1),className:`px-4 py-3 rounded-lg font-medium transition-all duration-200 ${s(i.href)?"bg-primary text-primary-foreground":"text-foreground hover:bg-muted"}`,children:i.label},i.href)),'
    'a.jsx("a",{href:"/umzugskosten/",className:"px-4 py-3 rounded-lg font-medium transition-all duration-200 text-foreground hover:bg-muted",children:"Preise"},"preise"),', 1)

DST.write_text(s, encoding="utf-8")
print(f"wrote {DST.name}: {len(orig)} -> {len(s)} bytes")
print("inventory items changed:", sum(1 for a,b in changed if a!=b), "kept:", sum(1 for a,b in changed if a==b))
