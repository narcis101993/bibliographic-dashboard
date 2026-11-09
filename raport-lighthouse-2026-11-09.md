# Remedieri Lighthouse — 2026-11-09

Raport inițial: `~/Downloads/download.pdf` (desktop, Accesibilitate 94).
Verificare finală: Lighthouse 13.5.0, preset desktop, rulat local pe
`docs/` servit prin HTTP — **Accesibilitate 100**, Performance 91,
`color-contrast` și `aria-allowed-attr` trecute (0 elemente),
`unminified-javascript` trecut (0 elemente), `unused-javascript`
**712 KiB → 62 KiB** economii estimate. JSON complet:
`lighthouse-accessibility-after-2026-11-09.json`.

## 1. Contrast insuficient — REPARAT (`dashboard/styles.css`)

Culori vechi sub pragul WCAG AA 4.5:1 pentru text mic (măsurat):

| Combinație veche | Contrast | Nou | Contrast nou |
|---|---|---|---|
| `--muted-2` #94a3b8 pe alb | 2.56 | #5b6b82 | 5.43 |
| `--ok` #2f8a5b pe `--ok-soft` | 3.77 | #23714a | 5.24 |
| `--warn` #9a6a12 pe `--warn-soft` | 4.21 | #7d560d | 5.83 |
| `--muted` #64748b pe `--surface-2` | ~4.6 (limită) | #55657d | 5.66 |
| `--accent` #2a7396 pe `--accent-soft` | ~4.5 (limită) | #22617f | 5.86 |
| dark `--muted-2` #6b7280 pe suprafață dark | ~3.8 | #94a3b8 | 6.92 |

Schimbări: doar cele 5 variabile de culoare (+ placeholder dark
#6b7280 → #9ca3af, + subliniere linkuri inline, vezi §4). Nicio
schimbare de layout. Culoarea tick-urilor Chart.js din `app.js`
(`chartColors()`) a fost aliniată la noul `--muted` (#55657d).

## 2. Minificare JS — REPARAT (la build)

- `dashboard/app.js` (98,5 KiB, sursă lizibilă, rămâne în repo) este
  minificat la build de `scripts/minify_app_js.py` (terser 5.51.2) în
  `dashboard/app.min.js` (**58,9 KiB**, −39,6 KiB; gzip 23,2 → 17,4 KiB).
  `index.html` încarcă acum `app.min.js`; `sw.js` îl cache-uiește și
  versiunea cache a fost bump-uită la `biblio-dashboard-v3`.
- `dashboard/data/dashboard-data.js` (721 KiB) era deja JSON compact pe o
  singură linie — minificarea nu mai aduce nimic acolo.
- Workflow-ul GitHub Actions regenerează `app.min.js` înainte de sync-ul
  `dashboard/` → `docs/` (pas nou „Rebuild minified JS + trimmed
  Chart.js bundle"), deci o editare viitoare în `app.js` nu poate rămâne
  nemimificată pe site.
- Testul smoke (`tests/test_app_js_smoke.js`) verifică acum fișierul
  livrat, `app.min.js`.

## 3. JS nefolosit (712 KiB) — REPARAT parțial, restul e Chart.js core

Ce se încărca fără folosire: `vendor/chart.umd.min.js` (201 KiB) conține
toate tipurile de grafice Chart.js (line, pie, polar, radar, scatter,
bubble), scale logaritmice/de timp, decimation, filler și pluginul title.
Aplicația folosește **doar bar + doughnut, cu legend + tooltip**
(5 grafice, verificate în `app.js`: `type: "bar"` ×3, `type: "doughnut"` ×2).

Soluție aplicată: bundle custom `dashboard/vendor/chart.min.js`
(**165 KiB**, −36 KiB), construit din `scripts/chart-entry.js` cu esbuild
(`scripts/build_chart_bundle.py`, Chart.js 4.4.7 MIT — licența rămâne în
`vendor/CHARTJS-LICENSE.md`). Expune același global `Chart`
(`new Chart`, `.resize()`, `.destroy()`), deci `app.js` nu s-a schimbat
pentru asta. Verificat în browser real: toate 5 canvas-uri au instanță
Chart activă și graficele bar/doughnut se pictează corect (inclusiv
legendă, tooltip, click-to-filter).

Ce rămâne din „unused" (62 KiB estimați de Lighthouse): nucleul Chart.js
(interacțiune, animație, helpers) — este cod care *se execută* la fiecare
interacție cu graficele, dar Lighthouse îl marchează nefolosit pe
încărcarea inițială, pentru că graficele sunt sub fold / în tab-uri
neactivate la momentul măsurătorii. Încărcarea lazy a Chart.js ar amâna
graficele din primul tab (vizibile imediat) și ar strica UX-ul, fără
câștig real — de aceea nu s-a făcut. Aceasta este concluzia „raport
scris": restul de 62 KiB nu poate fi eliminat fără a pierde graficele
sau a le întârzia.

## 4. ARIA — REPARAT

- **Cauza principală**: `aria-expanded` era pus pe `<tr class="pub-main">`
  (rand de tabel, rol `row`) — atribut nepermis pentru rolul `row`
  (audit `aria-allowed-attr`). Înlocuit cu un buton real
  `<button class="pub-expand-btn" aria-expanded aria-controls="pub-detail-<id>">`
  în prima celulă; click-ul pe rând funcționează la fel, iar starea
  expandată se setează acum pe buton. Stil buton adăugat în `styles.css`
  (inclusiv `:focus-visible`).
- `aria-label` pe `<div>` fără rol (`charts-row`, `filterbar`) →
  adăugat `role="group"`, ca eticheta să aibă sens.
- `aria-label` pe `<canvas>` → adăugat `role="img"` (5 grafice).
- Bonus, același scor de accesibilitate: auditul `link-in-text-block`
  (linkuri distinse doar prin culoare) — linkurile inline din subtitlu
  și footer sunt acum subliniate permanent. Acesta a fost ultimul audit
  picat; accesibilitatea a ajuns la 100.

## Verificări rulate (toate OK)

- `python3 -m unittest discover -s tests` → 58 teste OK
- `node tests/test_app_js_smoke.js` → SMOKE OK (pe `app.min.js`)
- `python3 scripts/build_dashboard_data.py --check` → validation OK
- Browser real (file://): 5/5 grafice pictate, rând expandabil funcțional,
  0 `tr[aria-expanded]`, v7 încărcat (23 publicații).
- Lighthouse 13.5.0 desktop: Accesibilitate **94 → 100**,
  Performance 91, contrast/ARIA/minify trecute, unused JS 712 → 62 KiB.

## Fișiere schimbate

`dashboard/styles.css`, `dashboard/index.html`, `dashboard/app.js`,
`dashboard/sw.js`, `dashboard/app.min.js` (nou, generat),
`dashboard/vendor/chart.min.js` (nou, generat),
`dashboard/vendor/chart.umd.min.js` (șters), `docs/` (sync oglindă),
`scripts/minify_app_js.py` + `scripts/build_chart_bundle.py` +
`scripts/chart-entry.js` (noi), `scripts/update_readme.py`,
`.github/workflows/refresh-citations.yml`, `tests/test_app_js_smoke.js`,
`package.json` + `package-lock.json` (devDependencies: chart.js 4.4.7,
esbuild 0.25.10 — doar pentru build, nepublicate), `README.md`,
`lighthouse-accessibility-after-2026-11-09.json`.

Fără push, fără modificarea istoricului git — commit-ul rămâne la
Narcis (GitHub Desktop), ca de obicei.
