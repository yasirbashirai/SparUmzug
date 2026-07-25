# mae-umzug-v2

Patched production build of the SparUmzug / MAE moving-company website
(live at https://mae-umzug-entruempelung.de/).

No source code exists for this site (built with Lovable, only the compiled
`dist/` was available), so pricing updates are patched directly into the
minified bundle `dist/assets/index-mae-v2p1.js` (renamed from
`index-2q_isVEQ.js` for cache-busting).

## Price changes applied 2026-07-26 (client request)

| Item | Old | New |
|---|---|---|
| Grundkosten (all apartment sizes) | 200–1000 € | flat 150 € |
| Entfernung pro km | 1,50 € | 0,75 € |
| Verpackung / Einpacken / Auspacken / Umwickeln / Reinigung | 150 € each | 100 € each |
| Alle Möbelstücke | — | each −5 € (floor 0 €) |

Unchanged: Montage 150 €, Demontage 150 €, Entrümpelung 200 €, floors,
Halteverbot, kitchen, boxes/bags, parking distance.

Applies to both the homepage mini-estimator and the /calculator page.

## Deploy

Upload the contents of `dist/` to Hostinger (replaces the current site).
