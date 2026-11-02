# Metodologie și incertitudini — citări v4

Data recuperării: **2026-11-01** (toate interogările din acest document au fost rulate în această zi).
Autor: researcher (echipa reaserch-list).

## 1. Scop

Creșterea acoperirii citărilor și transformarea numărului de citări într-un indicator
verificabil: fiecare lucrare citantă trebuie să aibă o sursă identificabilă, o dată de
verificare și un nivel de încredere explicit. Nu se inventează și nu se interpolează
înregistrări.

## 2. Decizie de versionare

v1 și v3 rămân neatinse. S-a produs o pereche nouă:

- `centralizator/v4/Centralizator_Articole_Gabriela_Daniela_Stamatie_v4.{csv,md,xlsx}`
- `citari/v4/Citari_Articole_Gabriela_Daniela_Stamatie_v4.{csv,md,xlsx}`
- `citari/v4/Acoperire_Publicatii_v4.{csv,md,xlsx}` — stare de acoperire pe publicație
- `citari/v4/Excluded_Candidates_v4.csv` — candidați respinși, cu motiv (audit)
- `citari/v4/raw/` — răspunsurile brute ale API-urilor, verbatim, pentru trasabilitate

## 3. Surse încercate și accesibilitate (2026-11-01)

| Sursă | Acces | Rezultat |
|---|---|---|
| OpenAlex | public, gratuit | funcțional; listă completă de lucrări citante per articol |
| Semantic Scholar Graph API | public, fără cheie | endpoint-ul de citări per DOI funcțional; endpoint-ul de căutare după titlu a returnat **HTTP 429** în mod repetat (limită de rată partajată) |
| Crossref | public | funcțional pentru contor (`is-referenced-by-count`); **lista** de lucrări citante (Cited-by) necesită credențiale de membru/depozitant și nu este disponibilă public |
| DataCite | public | funcțional; pentru #19 raportează `citationCount = 0` |
| Scopus / Web of Science / Google Scholar | cu plată / abonament | **indisponibil** — nu avem credențiale |

Notă despre Crossref: la prima încercare (2026-10-31) API-ul a răspuns cu HTTP 429
(rate limit). La reverificarea din 2026-11-01 a revenit la HTTP 200, iar contoarele
au putut fi colectate integral. Limitarea a fost temporară, nu permanentă.

## 4. Metodă de recuperare

1. Pentru fiecare publicație s-a rezolvat un identificator OpenAlex: după DOI când există,
   altfel după potrivire **exactă** a titlului normalizat (fără potriviri aproximative).
2. Lucrările citante s-au descărcat integral (paginare cu cursor) din OpenAlex
   (`filter=cites:W...`) și din Semantic Scholar (`paper/{id}/citations`, cheie DOI).
3. Pentru fiecare publicație s-a înregistrat contorul public Crossref, ca verificare
   independentă a ordinului de mărime.
4. Răspunsurile brute au fost salvate sub `citari/v4/raw/<sursă>/<id>.json` și nu au
   fost modificate ulterior.

Scripturi reproducibile: `scripts/fetch_citation_sources.py`,
`scripts/check_crossref_counts.py`, `scripts/build_citations_v4.py`.

## 5. Deduplicare

Cheia de identitate a unei lucrări citante:

1. DOI normalizat (lowercase, fără prefix `https://doi.org/`), dacă există;
2. altfel `titlu normalizat | an | numele primului autor`.

Normalizarea titlului elimină diacriticele, punctuația și diferențele de majuscule.
O lucrare care citează mai multe articole ale autoarei rămâne **o singură** înregistrare,
cu toate ID-urile în coloana `Articol (ID)` — aceeași convenție ca în v3.

Rezultat: 107 lucrări unice, 0 duplicate după DOI, 0 rânduri fără niciun identificator.

## 6. Reconciliere cu v3 (99 lucrări / 102 legături)

| Indicator | v3 | v4 |
|---|---|---|
| Lucrări citante unice | 99 | **107** |
| Legături articol–lucrare | 102 | **110** |
| Lucrări auto-citante | 2 | **2** (neschimbat) |
| Legături de auto-citare | 4 | **4** (neschimbat) |
| Publicații cu ≥1 citare | 11 / 19 | **11 / 19** |

Toate cele 99 de lucrări din v3 sunt prezente în v4 (verificat automat pe cheia de
identitate). Diferențele pe publicație provin din actualizarea OpenAlex și din
adaugarea Semantic Scholar:

- #4: +2 legături (40 → 42)
- #11: +4 legături (24 → 28) — Semantic Scholar aduce lucrări absente din OpenAlex
- #13: +2 legături (2 → 4)
- #7: neschimbat (11 → 11) după excluderea candidatului fals pozitiv
- celelalte publicații: neschimbate

Descoperirile din verificarea Crossref (2026-11-01), comparate cu **legăturile** reale
din v3 (nu cu numărul de rânduri, care subestima articolele citate de lucrări multiple):
#11 +1 (25 vs 24), #18 +1 (2 vs 1), #4 −2 (38 vs 40), #7 −2 (9 vs 11).
Diferențele se explică prin faptul
că Crossref numără doar citările cu DOI înregistrat și referințe depuse, în timp ce
OpenAlex/Semantic Scholar includ și alte tipuri de itemi (lucrări de conferință,
preprinturi, capitole). Lista Crossref nu poate fi descărcată fără acces de membru,
deci diferența nu poate fi reconciliată rând cu rând — este documentată ca atare.

## 7. Zero-uri confirmate și zero-uri neverificabile

**Zero confirmat** (verificat în OpenAlex, Semantic Scholar și, unde există DOI, Crossref):
#9, #15, #16, #17, #19.

- #19 (ResearchGate, `10.13140/RG.2.2.29075.86568`): **are** înregistrare OpenAlex
  (`W6885144657`), dar cu 0 lucrări citante; DataCite raportează `citationCount = 0`;
  Crossref răspunde 404 (DOI nu este înregistrat la Crossref). Constatarea din v3
  („fără înregistrare OpenAlex”) nu mai este valabilă la 2026-11-01.

**Parțial verificat — fără identificator**: #5, #8, #14 (Scientific Bulletin. Series F.).

- nu au DOI, deci Crossref Cited-by nu poate fi interogat, iar DataCite nu poate fi
  interogat după DOI; căutarea DataCite după titlu a fost totuși rulată:
  #8 și #14 → 0 rezultate; #5 → 8 rezultate, niciun titlu identic (potriviri
  necorelate, respinse);
- căutarea OpenAlex după titlu nu a returnat potrivire exactă (candidații apropiați
  au titluri diferite și au fost respinși, nu asimilați);
- căutarea Semantic Scholar după titlu a fost blocată de HTTP 429 fără cheie API
  (reîncercată de trei ori, inclusiv după pauze de 30–45 s).

Aceste trei publicații sunt raportate explicit ca **parțial verificate**, nu ca „fără citări”.
Singura cale care ar putea schimba acoperirea lor este accesul instituțional la
**Scopus / Web of Science** (sau verificarea manuală în arhiva revistei), pe care nu îl avem.

**Caz special #6**: singura lucrare citantă provine din înregistrarea Semantic Scholar
preluată din v3; reverificarea live a fost blocată (HTTP 429). Este marcată ca atare în
coloana `Sursă verificare`, iar încrederea este `mediu`.

## 8. Niveluri de încredere

| Nivel | Regulă |
|---|---|
| `ridicat` | DOI rezolvabil **și** fie confirmat în ≥2 surse independente, fie înregistrare OpenAlex cu metadate de editor |
| `mediu` | o singură sursă: DOI rezolvabil doar în Semantic Scholar, sau fără DOI dar cu titlu, an, autori și revistă complete; verificare manuală recomandată |
| `scăzut` | fără DOI și cu metadate incomplete (an/autori/revistă lipsă); verificare manuală necesară |

Distribuție v4: 98 `ridicat`, 8 `mediu`, 1 `scăzut`.

## 9. Candidați respinși

O singură potrivire Semantic Scholar a fost exclusă din setul principal și păstrată în
`Excluded_Candidates_v4.csv`: `10.25699/tohbipp.2024.90.71.018` (electrofilarea
materialelor compozite polimerice) — subiect total necorelat cu panificația, suspectată
a fi fals pozitiv. Excluderea este documentată, nu ascunsă; nu s-a șters nicio
înregistrare care exista în v3.

## 10. Contractul coloanelor

`citari/v4` păstrează cele 13 coloane din v3 și adaugă 6:

| Coloană nouă | Semnificație |
|---|---|
| `Surse (proveniență)` | sursele care au găsit lucrarea (`OpenAlex`; `Semantic Scholar`) |
| `Data verificării` | data recuperării (`2026-11-01`) |
| `Nivel de încredere` | `ridicat` / `mediu` / `scăzut` |
| `Baza încrederii` | motivul textual al nivelului |
| `OpenAlex Work ID` | identificator OpenAlex al lucrării citante |
| `Semantic Scholar Paper ID` | identificator Semantic Scholar al lucrării citante |

`centralizator/v4` păstrează cele 16 coloane din v3 și adaugă 5:
`Citări găsite (v4)`, `Surse verificate (citări)`, `Stare acoperire citări`,
`Încredere agregată`, `Notă acoperire`.

## 11. Limitări și pași următori de verificare

1. Lista Crossref Cited-by nu este publică; contorul Crossref este doar un control de ordin
   de mărime, nu o dovadă a identității fiecărei lucrări.
2. Semantic Scholar fără cheie API limitează puternic căutarea după titlu (HTTP 429).
   O cheie API ar debloca verificarea #5, #8, #14 și a #6.
3. Diferențele față de contorul Crossref (#2 6 vs 5, #3 2 vs 1, #4 42 vs 38, #7 11 vs 9,
   #11 28 vs 25, #13 4 vs 2, #18 1 vs 2) nu pot fi explicate rând cu rând fără lista Cited-by.
4. Încrederea `mediu`/`scăzut` marchează exact locurile unde este nevoie de verificare
   manuală (8 + 1 înregistrări).
5. Pentru #5, #8, #14: acces Scopus/Web of Science sau arhiva Scientific Bulletin este
   singura cale rezonabilă de a transforma „neverificabil” în „zero confirmat” sau în
   citări reale.

## 12. Stadiul sarcinii

- **Etapa 1 (finalizată)**: recuperare DOI-bearing, merge/dedupe, proveniență și încredere,
  acoperire pe publicație, pereche v4, această notă, reconciliere cu 99/102.
- **Etapa 2 (finalizată pentru sursele accesibile)**: probe DataCite și Semantic Scholar
  pentru #5, #8, #14, #19. DataCite: #19 are înregistrare cu `citationCount = 0` și fără
  relații de citare; #8 și #14 → 0 rezultate; #5 → 8 rezultate fără potrivire exactă.
  Semantic Scholar: #19 → 404 (nu este indexat); căutarea după titlu pentru #5, #8, #14
  rămâne blocată de HTTP 429 fără cheie API. Rezultatul este consemnat ca „verificat,
  fără rezultat” sau „blocat”, niciodată ca citare inventată. Deblocarea necesită o
  cheie API Semantic Scholar sau acces Scopus/Web of Science.
