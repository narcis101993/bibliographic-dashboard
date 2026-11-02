# Dashboard bibliografic — Gabriela Daniela Stamatie

Proiect de documentare bibliografică pentru **Gabriela Daniela Stamatie (Criveanu-Stamatie)** — ORCID [0000-0002-1850-7278](https://orcid.org/0000-0002-1850-7278), Institutul de Bioresurse Alimentare (IBA), București.

Dashboard static bilingv (RO/EN) cu:
- **Publicații** — centralizator cu 19 înregistrări, filtrare, sortare, paginare, export CSV/XLSX
- **Citări** — 107 lucrări citante, 110 legături, 2 auto-citări, matrice multi-legătură
- **Sinteză** — statistici, acoperire, surse, manifest de versiune

## Structura folderului

```
Bibliographic dashboard/
├── dashboard/              Aplicația web (HTML/CSS/JS + Chart.js)
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── vendor/
│   │   └── chart.umd.min.js
│   └── data/
│       ├── dashboard-data.js      Date încorporate (funcționează pe file://)
│       ├── version-manifest.json  Versiuni detectate + surse
│       ├── v1/                    Date normalizate v1
│       ├── v3/                    Date normalizate v3
│       └── v4/                    Date normalizate v4 (curent)
├── centralizator/          Sursa XLSX/CSV/MD (local)
│   ├── v1/
│   ├── v3/
│   └── v4/
├── citari/                 Sursa XLSX/CSV/MD + raw data (local)
│   ├── v1/
│   ├── v3/
│   └── v4/
├── scripts/                Scripturi Python de build
└── README.md               Acest fișier
```

## Rulare locală

```bash
# Deschide direct (date încorporate, funcționează pe file://)
open dashboard/index.html

# Server local (încarcă CSV-urile la runtime, ca pe GitHub Pages)
python3 -m http.server 8000
# apoi: http://localhost:8000/dashboard/
```

## Regenerarea datelor

```bash
python3 scripts/build_dashboard_data.py
```

Scriptul detectează cea mai mare versiune numerică prezentă în `centralizator/vN` și `citari/vN`, normalizează CSV-urile și scrie:
- `dashboard/data/version-manifest.json`
- `dashboard/data/vN/publications.json` și `citations.json`
- `dashboard/data/dashboard-data.js` — bundle încorporat pentru `file://`

## Publicare pe GitHub Pages

### Varianta 1: GitHub Pages (recomandată)

1. Creează un repo public pe GitHub: `https://github.com/narcis101993/bibliographic-dashboard`
2. Clonează local și copiază conținutul folderului `Bibliographic dashboard/` în repo
3. În Settings → Pages:
   - Source: **Deploy from a branch**
   - Branch: **main** / **root** (sau `/docs` dacă pui fișele în `docs/`)
4. GitHub Pages va genera URL-ul: `https://narcis101993.github.io/bibliographic-dashboard/`

**Fișiere necesare pentru deploy:**
```
dashboard/index.html
dashboard/styles.css
dashboard/app.js
dashboard/vendor/chart.umd.min.js
dashboard/data/dashboard-data.js
dashboard/data/version-manifest.json
centralizator/v4/*.xlsx    (pentru download XLSX)
citari/v4/*.xlsx           (pentru download XLSX)
```

### Varianta 2: Cloudflare Pages (fără limită de bandă)

1. Conectează repo-ul GitHub
2. Build command: `echo "no build needed"`
3. Output folder: `dashboard/`
4. Deploy automat la fiecare push

## Versiuni

| Versiune | Centralizator | Citări | Descriere |
|----------|--------------|--------|-----------|
| **v1** | 3 fișiere (fără sufix) | 3 fișiere (fără sufix) | Versiunea inițială: 19 înregistrări, 99 lucrări citante. |
| **v2** | — | — | Nu a fost produsă. |
| **v3** | 3 fișiere `_v3` | 1 fișier `_v3.csv` | Consolidare: centralizatorul integrează datele de citare. |
| **v4** | 3 fișiere `_v4` | 3 fișe + acoperire + metodologie | Citări multi-sursă (OpenAlex + Semantic Scholar): 107 lucrări / 110 legături. Acoperire explicită pe publicație. |

## Cifre-cheie (v4)

- 19 publicații (17 articole științifice, 1 preprint, 1 poster)
- 107 lucrări citante unice, 110 legături de citare
- 2 auto-citări (Foods 2022, Agronomy 2026)
- Top citate: #4 – 42 citări, #11 – 28 citări, #7 – 11 citări
- 14 publicații cu DOI, 5 fără citări confirmate, 3 parțial verificate

## Limitări / lacune de acoperire

- Nr. **5, 8, 14** (fără DOI / identificator) — citările nu pot fi recuperate automat (parțial verificate)
- Nr. **6** — nu este în OpenAlex; 1 citare prin Semantic Scholar
- Nr. **19** — indexat în DataCite, confirmat 0 citări
- Rezultatele de căutare după titlu au produs potriviri greșite în OpenAlex și au fost eliminate
- Pentru acoperire completă: Crossref Cited-by, Scopus/Web of Science, Google Scholar

## Funcționalități

- Tab-uri **Publicații**, **Citări**, **Sinteză**; comutare RO/EN
- Filtre instantanee: căutare, autor/co-autor, an, tip, revistă, doar cu DOI
- Sortare pe coloane, paginare, export CSV, descărcare XLSX
- Stare partajabilă în URL: tab, limbă, filtre, sortare, pagină
- Grafice Chart.js: publicații pe an/tip, citări pe an, top articole citate
- Panou detalii expandabil pentru fiecare publicație
- Acoperire date: badge-uri pentru zero confirmat / parțial verificat

## Licențe

- Chart.js 4.4.7 — MIT License (`dashboard/vendor/CHARTJS-LICENSE.md`)
