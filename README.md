# Dashboard bibliografic — Gabriela Daniela Stamatie

Proiect de documentare bibliografică pentru **Gabriela Daniela Stamatie (Criveanu-Stamatie)** — ORCID [0000-0002-1850-7278](https://orcid.org/0000-0002-1850-7278), Institutul de Bioresurse Alimentare (IBA), București.

Dashboard static bilingv (RO/EN) cu:
- **Publicații** — centralizator cu 23 înregistrări, filtrare, sortare, paginare, export CSV/XLSX
- **Citări** — 112 lucrări citante, 115 legături, 2 auto-citări, matrice multi-legătură
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
│       ├── v4/                    Date normalizate v4
│       ├── v5/                    Date normalizate v5
│       ├── v6/                    Date normalizate v6
├── centralizator/          Sursa XLSX/CSV/MD (local)
│   ├── v1/
│   ├── v3/
│   ├── v4/
│   ├── v5/
│   ├── v6/
├── citari/                 Sursa XLSX/CSV/MD + raw data (local)
│   ├── v1/
│   ├── v3/
│   ├── v4/
│   ├── v5/
│   ├── v6/
├── scripts/                Scripturi Python de build
└── README.md               Acest fișier
```

## Versiuni

| Versiune | Centralizator | Citări | Descriere |
|----------|--------------|--------|-----------|
| **v1** | 3 fișiere (fără sufix) | 3 fișiere (fără sufix) | Versiunea inițială: 19 înregistrări, 99 lucrări citante. |
| **v3** | 3 fișiere | 3 fișe + acoperire + metodologie | Consolidare: centralizatorul integrează datele de citare. 19 înregistrări, 99 lucrări citante. |
| **v4** | 3 fișiere | 3 fișe + acoperire + metodologie | 19 înregistrări, 107 lucrări citante. |
| **v5** | 3 fișiere | 3 fișe + acoperire + metodologie | 23 înregistrări, 107 lucrări citante. |
| **v6** | 3 fișiere | 3 fișe + acoperire + metodologie | Refresh automat (GitHub Actions): date actualizate din surse. 112 lucrări citante. |

## Cifre-cheie (v6)

- 23 publicații (17 articole științifice, 1 preprint, 1 poster)
- 112 lucrări citante unice, 115 legături de citare
- 2 auto-citări (Foods 2022, Agronomy 2026)
- Top citate: #1 – 44 citări, #2 – 29 citări, #3 – 11 citări
- 14 publicații cu DOI, 1 fără citări confirmate, 11 parțial verificate

## Funcționalități

- Tab-uri **Publicații**, **Citări**, **Sinteză**; comutare RO/EN
- Filtre instantanee: căutare, autor/co-autor, an, tip, revistă, doar cu DOI
- Sortare pe coloane, paginare, export CSV, descărcare XLSX
- Stare partajabilă în URL: tab, limbă, filtre, sortare, pagină
- Grafice Chart.js: publicații pe an/tip, citări pe an, top articole citate
- Panou detalii expandabil pentru fiecare publicație
- Acoperire date: badge-uri pentru zero confirmat / parțial verificat
- **Actualizare automată** a datelor prin GitHub Actions (lunar)
- Buton **Reîncarcă** în UI pentru reîncărcarea paginii (bypass cache)

## Actualizare automată a datelor

Datele brute (raw) sunt păstrate în git pentru trasabilitate; repo-ul crește cu ~3,5 MB per versiune. Reevaluăm politica de păstrare la v8 (arhivă zip sau Git LFS).

Datele se actualizează automat lunar prin [GitHub Actions](https://github.com/narcis101993/bibliographic-dashboard/actions):

1. **Fetch** — extragere date noi din surse (OpenAlex, Semantic Scholar, DataCite, Crossref, ResearchGate — detectare DOI 10.13140/; Google Scholar: import manual din `citari/google_scholar_counts.csv`, Scholar nu are API public)
2. **Build** — procesare și normalizare în `citari/vN/` și `centralizator/vN/` (versiune nouă automată)
3. **Sync** — regenerare `dashboard/data/` și sincronizare în `docs/` pentru GitHub Pages
4. **Commit** — commit automat în branch-ul `main`

Pentru actualizare manuală, accesează:
- [Run workflow](https://github.com/narcis101993/bibliographic-dashboard/actions/workflows/refresh-citations.yml)

Butonul **Reîncarcă** din dashboard reîncarcă pagina (fără cache) pentru a afișa ultimele date disponibile.

## Licențe

- Chart.js 4.4.7 — MIT License (`dashboard/vendor/CHARTJS-LICENSE.md`)
