# Bibliographic dashboard — retenție repo la v8 (pregătire, 2026-11-09)

**Stare: PREGĂTIRE, nu execuție finală.** N-am șters nimic, n-am rescris istoric git, n-am făcut push.
Motivul: (1) v8 nu există încă — refresh-ul lunar e programat pe 2026-12-01
(cron `0 0 1 * *` în `.github/workflows/refresh-citations.yml`); (2) ștergerea din repo
cere confirmarea explicită a lui Narcis.

## 1. Verificare v8 (2026-11-09)
- Ultimul commit: `ac59e96 chore: auto-refresh citation data 2026-11-07 — new version v7`
- Versiunea curentă: **v7** (foldere `citari/v1, v3, v4, v5, v6, v7` — nu există `v2` ca folder,
  nici `v8`; `centralizator/` are tot v1, v3–v7 și conduce detecția versiunii în workflow).
- De re-verificat după 2026-12-01 / reminder organizer 2026-12-02.

## 2. Mărime înainte (măsurat cu `du`, 2026-11-09)
- Working tree total: **38 MB** (include `node_modules/` 15 MB, ne-urmărit de git)
- `citari/`: **16 MB**, din care:
  - v1 116 KB, v3 48 KB (fără foldere `raw/`)
  - v4 3,8 MB (raw 3,5 MB), v5 3,7 MB (raw 3,5 MB), v6 4,2 MB (raw 4,0 MB), v7 4,4 MB (raw 4,2 MB)
  - **v1–v6 împreună ≈ 11,9 MB**, din care ~11,0 MB sunt `raw/` (JSON-uri brute per sursă)
- `centralizator/v1–v6`: ~292 KB total (mic; de inclus în arhiva finală pentru completitudine)
- `.git/`: 2,6 MB (pack 1,93 MiB) — conține deja blob-urile v1–v6 din istoric

## 3. Arhivă de probă (NON-destructivă, NU în repo)
- Fișier: `/Users/narciscriveanu/.hermes/profiles/dev/cache/scratch/citari-v1-v6-DRAFT-2026-11-09.zip`
- Mărime: **2,0 MB** (11,9 MB → 2,0 MB; JSON-urile se comprimă bine), `zip -T` = OK
- Atenție: e în folderul de scratch (pruned după 24h) — e doar DRAFT de măsurare.
  Arhiva finală trebuie mutată într-un loc permanent pe laptop (ex. folderul proiectului
  părinte sau un folder `Arhiva/` creat de Narcis), NU în repo.

## 4. Ce se întâmplă după confirmare + v8 (plan, de executat atunci)
1. Zip final: `citari/v1, v3–v6` + `centralizator/v1, v3–v6` → arhivă locală permanentă,
   verificată cu `zip -T` + sumă SHA-256 notată.
2. Eliminare din working tree printr-un **commit nou** (`git rm`), NU prin rescriere istoric.
   Efect așteptat: `citari/` 16 MB → ~2,2 MB (v7+v8 fără raw-uri vechi) — dar clone-urile
   noi păstrează istoricul vechi (~1,9 MiB pack), pentru că nu rescriem istoricul (cerința 4).
3. Măsurare `du` înainte/după și raport final; push DOAR prin GitHub Desktop cu aprobarea lui Narcis.

## 5. Oprirea creșterii viitoare (de decis, NU implementat acum)
Cauza creșterii: fiecare refresh copiază integral `raw/` pentru noua versiune (~3,5–4,2 MB).
Opțiuni de propus lui Narcis înainte de 2026-12-01:
- **A (recomandat):** `raw/` rămâne doar pentru versiunea curentă; la refresh, raw-ul versiunii
  anterioare pleacă în arhiva locală și iese din git (commit nou). Datele curente rămân în repo,
  istoricul trasabil rămâne în arhiva zip locală.
- **B:** `raw/` e ignorat de git (`.gitignore` + workflow nu-l mai face `git add`), păstrat doar local.
  Atenție: GitHub Actions rulează pe runner temporar — raw-ul ar dispărea dacă nu e salvat ca artifact.
- **C:** Git LFS — păstrează tot în cloud, dar adaugă cost/complexitate; respins ca default.

## 6. Blocaje / decizii necesare de la Narcis
1. Confirmare pentru pasul 4.2 (eliminarea v1–v6 din repo printr-un commit nou, după zip final verificat).
2. Alegerea opțiunii A/B/C pentru creșterea viitoare + locul permanent al arhivei locale.
3. Așteptarea v8 (2026-12-01) înainte de execuția finală.
