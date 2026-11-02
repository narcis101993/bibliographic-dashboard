# Dashboard mockup — note tehnice

Status: **mockup static pentru aprobare** (v0.1). Nu conține logică de producție, nu încarcă date reale la runtime și nu are backend.

## Fișiere

```
dashboard/mockup/
├── index.html        structura: header, tabs, filtre, tabele, grafice, panou metadate
├── styles.css        design system minimal, layout responsive, componente
├── mock-version.js   simulare detectare versiune + badge dinamica
└── NOTES.md          acest document
```

Deschidere: `open dashboard/mockup/index.html` (funcționează și prin `file://`, fără build).

## Ce arată mockup-ul

### Layout

- Header cu identitatea autoarei, badge de versiune și data ultimei extrageri.
- Banner de auto-detectare: versiunea curentă, folderele folosite, regula de selecție, buton „Re-detectează”.
- Zonă principală cu trei taburi: **Publicații**, **Citări**, **Sinteză**.
- Bară de filtre deasupra fiecărui tabel (căutare, an, tip, revistă / articol citat, auto-citări).
- Tabele cu antet sticky, coloane numerice aliniate la dreapta, paginare mock.
- Grafice-placeholder: bare pe an, donut pe tipuri, top articole citate, matrice articol × an.
- Panou lateral permanent cu **Date extrase**, **Versiune & auto-detectare**, **Surse**.

### Taburi

| Tab | Conținut | Sursă de date planificată |
|---|---|---|
| Publicații | 19 înregistrări, filtre, tabel, publicații/an, tipuri | foaia `Centralizator` din `centralizator/v3/*_v3.xlsx` |
| Citări | 99 lucrări, filtre, KPI, tabel cu auto-citări evidențiate, citări/an, top citate | foaia `Citări` din `centralizator/v3/*_v3.xlsx` + `citari/v3/*_v3.csv` |
| Sinteză | KPI, matrice articol × an, acoperire, QA | foaia `Sinteză citări` + `Metodologie` |

### Panou metadate

- **Date extrase**: data extragerii, număr publicații, lucrări citante, legături, auto-citări, fișierul sursă.
- **Versiune & auto-detectare**: versiunea afișată, folderele detectate, pașii algoritmului, starea manifestului.
- **Surse**: OpenAlex, Semantic Scholar, Crossref, DataCite, ORCID, cu rol și status.

## Auto-detectarea versiunii (design propus)

Scop: dashboard-ul afișează întotdeauna cea mai nouă versiune comună dintre centralizator și citări, fără configurare manuală.

### Ordine de rezoluție

1. **Manifest** (preferat): `dashboard/version-manifest.json`, generat la finalul pipeline-ului de date.
2. **Scanare foldere**: `centralizator/v*/` și `citari/v*/`; se intersecționează versiunile și se alege maximul semver.
3. **Fallback**: ultima versiune cunoscută + avertisment vizibil în UI (nu se afișează date parțiale fără marcaj).

### Manifest propus

```json
{
  "schemaVersion": 1,
  "generatedAt": "2026-10-31T20:00:00Z",
  "latest": { "centralizator": "v3", "citari": "v3" },
  "datasets": [
    {
      "id": "centralizator",
      "version": "v3",
      "records": 19,
      "updatedAt": "2026-10-31",
      "files": {
        "xlsx": "centralizator/v3/Centralizator_Articole_Gabriela_Daniela_Stamatie_v3.xlsx",
        "csv": "centralizator/v3/Centralizator_Articole_Gabriela_Daniela_Stamatie_v3.csv",
        "md": "centralizator/v3/Centralizator_Articole_Gabriela_Daniela_Stamatie_v3.md"
      }
    },
    {
      "id": "citari",
      "version": "v3",
      "records": 99,
      "updatedAt": "2026-10-31",
      "files": {
        "csv": "citari/v3/Citari_Articole_Gabriela_Daniela_Stamatie_v3.csv"
      }
    }
  ]
}
```

Reguli:

- versiunile sunt comparate numeric (`v10 > v9`, nu lexicografic);
- dacă versiunile diferă între dataset-uri, se alege maximul **comun** și se afișează un badge de avertizare;
- manifestul are prioritate față de scanare; dacă lipsește, scanarea este suficientă;
- în mockup, detectarea este simulată în `mock-version.js` (lista `["v1","v3"]`, fără acces la disc).

## Maparea datelor

### Publicații (19)

Câmpuri afișate: `Nr.`, `An`, `Titlu`, `Revistă`, `Tip`, `DOI`, `Citări` (agregat). Coloanele complete din workbook rămân disponibile în vizualizarea detaliată (nu sunt toate în tabelul principal, pentru lizibilitate).

### Citări (99 / 102 legături)

Schema 13 coloane din v3: `Nr.`, `Articol (ID)`, `Titlu articol`, `An publicație`, `An citare`, `Lucrare citată`, `Autori citatori`, `Revistă / Eveniment`, `DOI citare`, `Link`, `Tip citare`, `Context / Observații`, `Sursă verificare`.

Reguli de afișare:

- rândurile cu `Auto-citare: Da` primesc fundal galben și pill „Da”;
- `Articol (ID)` poate conține mai multe articole (`1, 2, 3`); agregările pe articol se calculează prin împărțirea legăturii către fiecare ID;
- totalurile afișate: 102 legături, 99 lucrări unice, 97 lucrări externe unice, 2 auto-citări.

### Sinteză

- KPI: publicații, lucrări citante, legături, articole fără date.
- Matrice articol × an: se generează din legăturile de citare (nu din numărul de lucrări unice).
- Acoperire: articolele fără înregistrare OpenAlex (#5, #8, #14, #19) și #6 (doar Semantic Scholar).

## Ce este simulat în mockup

- Filtrele, checkbox-urile, paginarea și butoanele de export sunt **inactive** (demonstrează structura, nu logica).
- Graficele folosesc valori reale aproximative din v3, dar sunt marcate „Placeholder grafic”; implementarea va genera SVG/Canvas din date.
- Linkurile DOI sunt `#` în mockup.
- Detectarea versiunii folosește o listă locală, nu citește folderele.
- Tabelele afișează un eșantion (10 publicații din 19, 8 citări din 99).

## Opțiuni de implementare (pentru decizie)

**Opțiunea A — static + vanilla JS (recomandată pentru început)**
- `index.html` + CSS + JS, fără build; datele se încarcă din manifest și CSV.
- Potrivită pentru un dashboard read-only, ușor de hostat pe GitHub Pages / intranet.
- Necesită parser CSV (~50 linii) și, dacă se dorește citirea directă a XLSX în browser, o librărie (SheetJS) — altfel CSV este sursa runtime, iar XLSX rămâne pentru descărcare.

**Opțiunea B — Vite + React + Chart.js**
- Justificată dacă apar filtre complexe, selecție de coloane, comparații între versiuni sau mai multe dashboard-uri.
- Cost: build step, dependențe, mentenanță.

Recomandare: A pentru aprobare și prima versiune; migrare la B doar dacă cerințele de interactivitate o impun.

## Accesibilitate și responsive

- Taburi cu radio inputs + labels (funcționează fără JS), focus vizibil pe tastatură.
- Tabele semantice cu `thead`/`tbody`, antet sticky.
- Contrast text/fundal peste 4.5:1 pentru textul principal.
- `prefers-reduced-motion` dezactivează animațiile.
- Breakpoints: 1180px (panou lateral mai îngust), 960px (panou sub conținut), 680px (o coloană, filtre stivuite).

## Pași de implementare

1. Aprobare structură și denumiri (acest mockup).
2. Generator manifest + script de versionare la finalul pipeline-ului.
3. Încărcare date runtime: manifest → CSV; normalizare câmpuri și tipuri.
4. Filtre funcționale + sortare + paginare client-side.
5. Grafice reale (SVG sau Chart.js) din agregările deja calculate în v3.
6. Export CSV filtrat și linkuri DOI reale.
7. QA: verificare totaluri față de workbook, test responsive, test `file://` și host static.

## Întrebări deschise pentru aprobare

1. Limba UI: română (ca mockup-ul) sau bilingv RO/EN?
2. Hosting: fișier local / GitHub Pages / intranet? (afectează modul de încărcare a datelor)
3. Sursa runtime: CSV (recomandat) sau citire directă XLSX în browser?
4. Grafice: placeholder SVG simplu sau Chart.js?
5. Este nevoie de comparație între versiuni (v1 vs v3) sau doar „latest”?
6. Se dorește filtrare pe autori/co-autori sau doar pe articol/revistă/an?

## Criterii de acceptare pentru mockup

- Cele trei taburi sunt vizibile și comutabile fără erori.
- Fiecare tab conține filtre, tabel și cel puțin un grafic-placeholder.
- Panoul „Date extrase” și „Surse” este vizibil permanent pe desktop.
- Bannerul arată versiunea detectată și explicația auto-detectării.
- Layout-ul rămâne lizibil la 1440px, 1024px și 390px.
- Notele tehnice acoperă maparea datelor, algoritmul de detectare și pașii următori.
