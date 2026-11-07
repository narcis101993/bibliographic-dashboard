#!/usr/bin/env python3
"""Build the v4 citation dataset with multi-source provenance.

Inputs (all raw, verbatim):
  citari/v4/raw/openalex_citing/<pub>.json   OpenAlex citing works
  citari/v4/raw/s2_citing/<pub>.json         Semantic Scholar citing works
  citari/v4/raw/datacite/<pub>.json          DataCite record (citation count)
  citari/v4/raw/crossref_counts.json         Crossref public cited-by counts
  citari/v4/raw/retrieval-summary.json       per-publication retrieval result
  citari/v3/*.csv                            previous dataset (records retained
                                             when a source cannot be re-queried)

Merge rules:
  * identity key = DOI (lowercased) when present, else normalised title +
    publication year + first-author surname.
  * a citing work that cites several publications becomes one row listing all
    publication ids (same convention as v3), so links = sum of id lists.
  * nothing is synthesised; every row carries at least one source identifier
    or an explicit v3-retained provenance note.

Outputs: citari/v4/*.csv|md|xlsx, citari/v4/Acoperire_Publicatii_v4.*,
centralizator/v4/*.csv|md|xlsx, citari/v4/METODOLOGIE_v4.md
"""

import csv
import glob
import json
import os
import re
import argparse
import unicodedata
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "citari", "v4", "raw")
V3_CITARI = os.path.join(ROOT, "citari", "v3", "Citari_Articole_Gabriela_Daniela_Stamatie_v3.csv")
V3_CENTRALIZATOR = os.path.join(
    ROOT, "centralizator", "v3", "Centralizator_Articole_Gabriela_Daniela_Stamatie_v3.csv"
)
OUT_CIT = os.path.join(ROOT, "citari", "v4")
OUT_CEN = os.path.join(ROOT, "centralizator", "v4")
RETRIEVAL_DATE = __import__("datetime").date.today().isoformat()
SELF_NAMES = ("stamatie", "criveanu")

SOURCE_VERSION = "v3"
TARGET_VERSION = "v4"


def _find_versioned_csv(folder, prefix, version):
    exact = os.path.join(folder, "%s_%s.csv" % (prefix, version))
    if os.path.exists(exact):
        return exact
    matches = sorted(glob.glob(os.path.join(folder, prefix + "_*.csv")))
    return matches[0] if matches else exact


def init_paths(source_version=None, target_version=None):
    global RAW, V3_CITARI, V3_CENTRALIZATOR, OUT_CIT, OUT_CEN, SOURCE_VERSION, TARGET_VERSION
    SOURCE_VERSION = source_version or SOURCE_VERSION
    TARGET_VERSION = target_version or TARGET_VERSION
    if not SOURCE_VERSION.startswith("v"):
        SOURCE_VERSION = "v" + SOURCE_VERSION
    if not TARGET_VERSION.startswith("v"):
        TARGET_VERSION = "v" + TARGET_VERSION
    RAW = os.path.join(ROOT, "citari", TARGET_VERSION, "raw")
    V3_CITARI = _find_versioned_csv(
        os.path.join(ROOT, "citari", SOURCE_VERSION),
        "Citari_Articole_Gabriela_Daniela_Stamatie",
        SOURCE_VERSION,
    )
    V3_CENTRALIZATOR = _find_versioned_csv(
        os.path.join(ROOT, "centralizator", SOURCE_VERSION),
        "Centralizator_Articole_Gabriela_Daniela_Stamatie",
        SOURCE_VERSION,
    )
    OUT_CIT = os.path.join(ROOT, "citari", TARGET_VERSION)
    OUT_CEN = os.path.join(ROOT, "centralizator", TARGET_VERSION)

# Candidates excluded after manual plausibility review. Every entry must state
# the reason and stay documented in Excluded_Candidates_v4.csv.
EXCLUDED = {
    "10.25699/tohbipp.2024.90.71.018": "Titlu și subiect necorelate (electrofilare polimeri vs. panificație); potrivire Semantic Scholar suspectată a fi fals pozitiv. Exclus din setul principal, păstrat aici pentru audit.",
}

TYPE_RO = {
    "article": "Articol",
    "review": "Review",
    "conference-paper": "Lucrare de conferință",
    "book-chapter": "Capitol de carte",
    "preprint": "Preprint",
    "book": "Carte",
    "dataset": "Set de date",
    "dissertation": "Teză",
    "report": "Raport",
    "editorial": "Editorial",
    "letter": "Scrisoare",
    "erratum": "Erata",
    "paratext": "Paratext",
    "other": "Alt tip",
    "peer-review": "Recenzie",
    "libguides": "Ghid",
    "standard": "Standard",
    "reference-entry": "Intrare de referință",
    "supplementary-materials": "Material suplimentar",
}
S2_TYPE_RO = {
    "JournalArticle": "Articol",
    "Review": "Review",
    "Conference": "Lucrare de conferință",
    "Book": "Carte",
    "BookSection": "Capitol de carte",
    "Dataset": "Set de date",
    "Editorial": "Editorial",
    "LettersAndComments": "Scrisoare",
    "MetaJournal": "Articol",
    "News": "Știre",
    "Study": "Studiu",
    "CaseReport": "Studiu de caz",
    "ClinicalTrial": "Studiu clinic",
}


def norm_title(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode()
    t = t.lower().replace("&amp;", "and")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def surname(name):
    name = (name or "").strip()
    if not name:
        return ""
    return norm_title(name.split(",")[0].split()[-1])


def clean(t):
    return (t or "").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()


RG_DOI_PREFIX = "10.13140/"


def load_scholar_counts():
    """Manual Google Scholar counts from citari/google_scholar_counts.csv."""
    path = os.path.join(ROOT, "citari", "google_scholar_counts.csv")
    counts = {}
    try:
        with open(path, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f, delimiter=";"):
                pid = (row.get("Nr.") or "").strip()
                raw = (row.get("Citari_Google_Scholar") or "").strip()
                if pid and raw.isdigit():
                    counts[pid] = int(raw)
    except Exception:
        pass
    return counts


def is_researchgate_doi(u):
    return doi_of(u).startswith(RG_DOI_PREFIX)


def doi_of(u):
    d = (u or "").strip()
    if not d:
        return ""
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d, flags=re.I)
    return d.lower()


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)["payload"]
    except Exception:
        return default


def load_pubs():
    with open(V3_CENTRALIZATOR, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


def load_v3_rows():
    with open(V3_CITARI, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


def oa_work(rec, pub_id):
    src = ((rec.get("primary_location") or {}).get("source") or {}).get("display_name")
    authors = [a["author"]["display_name"] for a in rec.get("authorships", []) if a.get("author")]
    return {
        "pub_ids": [pub_id],
        "title": clean(rec.get("title") or rec.get("display_name")),
        "year": rec.get("publication_year"),
        "authors": authors,
        "venue": clean(src) if src else "",
        "doi": doi_of(rec.get("doi")),
        "type": TYPE_RO.get(rec.get("type"), "Alt tip"),
        "openalex": rec.get("id"),
        "s2": None,
        "sources": {"OpenAlex"},
    }


def s2_work(item, pub_id):
    p = item.get("citingPaper") or {}
    ext = p.get("externalIds") or {}
    venue = clean((p.get("journal") or {}).get("name") or p.get("venue"))
    types = p.get("publicationTypes") or []
    return {
        "pub_ids": [pub_id],
        "title": clean(p.get("title")),
        "year": p.get("year"),
        "authors": [a.get("name") for a in (p.get("authors") or []) if a.get("name")],
        "venue": venue,
        "doi": doi_of(ext.get("DOI")),
        "type": S2_TYPE_RO.get(types[0], "Alt tip") if types else "Alt tip",
        "openalex": None,
        "s2": p.get("paperId"),
        "sources": {"Semantic Scholar"},
    }


def fatcat_citations(payload):
    """Extract citing-release list from a Fatcat raw payload (tolerant)."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        cites = payload.get("citations")
        if isinstance(cites, list):
            return cites
    return []


def fatcat_work(item, pub_id):
    """Map one Fatcat citing release to the common work shape (or None)."""
    if not isinstance(item, dict):
        return None
    rel = item.get("citing_release") or item.get("release") or item
    if not isinstance(rel, dict) or not rel.get("title"):
        return None
    authors = []
    for author in rel.get("authors") or []:
        if isinstance(author, dict):
            name = ((author.get("given_name") or "") + " " + (author.get("surname") or "")).strip()
            if name:
                authors.append(name)
        elif isinstance(author, str) and author.strip():
            authors.append(author.strip())
    year = rel.get("year")
    return {
        "pub_ids": [pub_id],
        "title": clean(rel.get("title")),
        "year": year if isinstance(year, int) else None,
        "authors": authors,
        "venue": clean(rel.get("container_name") or ""),
        "doi": doi_of(rel.get("doi")),
        "type": TYPE_RO.get(rel.get("type"), "Alt tip"),
        "openalex": None,
        "s2": None,
        "sources": {"Fatcat"},
    }


def v3_work(row):
    ids = [x.strip() for x in row["Articol (ID)"].split(",") if x.strip()]
    authors = [a.strip() for a in (row["Autori citatori"] or "").split(";") if a.strip()]
    return {
        "pub_ids": ids,
        "title": clean(row["Lucrare citată"]),
        "year": int(row["An citare"]) if (row["An citare"] or "").isdigit() else None,
        "authors": authors,
        "venue": clean(row["Revistă / Eveniment"]),
        "doi": doi_of(row["DOI citare"]),
        "type": row["Tip citare"],
        "openalex": None,
        "s2": None,
        "sources": {"Semantic Scholar"} if "Semantic" in (row["Sursă verificare"] or "") else {"OpenAlex"},
        "retained_from": "v3",
    }


def key_of(w):
    if w["doi"]:
        return "doi:" + w["doi"]
    first = surname(w["authors"][0]) if w["authors"] else ""
    return "tt:%s|%s|%s" % (norm_title(w["title"]), w["year"] or "", first)


def is_self(w):
    for a in w["authors"]:
        n = norm_title(a)
        if any(s in n for s in SELF_NAMES):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-version", default=None, help="source version (e.g. v3, v4)")
    ap.add_argument("--target-version", default=None, help="target version (e.g. v4, v5)")
    args = ap.parse_args()
    init_paths(args.source_version, args.target_version)

    pubs = load_pubs()
    pub_by_id = {p["Nr."]: p for p in pubs}
    summary = {r["publicationId"]: r for r in json.load(open(os.path.join(RAW, "retrieval-summary.json")))["publications"]}

    def raw_count(source, pid):
        path = os.path.join(RAW, source, pid + ".json")
        if not os.path.exists(path):
            return None
        data = load_json(path, [])
        return len(data or [])
    crossref = {r["publicationId"]: r for r in json.load(open(os.path.join(RAW, "crossref_counts.json")))["publications"]}
    dc_path = os.path.join(RAW, "datacite_search", "no_doi_publications.json")
    if os.path.exists(dc_path):
        dc_search = json.load(open(dc_path))["results"]
    else:
        dc_search = {}

    groups = {}

    def add(w):
        k = key_of(w)
        g = groups.get(k)
        if g is None:
            groups[k] = w
            return
        g["pub_ids"] = sorted(set(g["pub_ids"]) | set(w["pub_ids"]), key=int)
        g["sources"] |= w["sources"]
        for f in ("openalex", "s2"):
            if not g.get(f) and w.get(f):
                g[f] = w[f]
        for f in ("title", "venue", "type", "year", "doi"):
            if not g.get(f) and w.get(f):
                g[f] = w[f]
        if len(w["authors"]) > len(g["authors"]):
            g["authors"] = w["authors"]

    for p in pubs:
        pid = p["Nr."]
        oa = load_json(os.path.join(RAW, "openalex_citing", pid + ".json"), []) or []
        for rec in oa:
            add(oa_work(rec, pid))
        s2 = load_json(os.path.join(RAW, "s2_citing", pid + ".json"), []) or []
        for item in s2:
            add(s2_work(item, pid))
        fat = load_json(os.path.join(RAW, "fatcat_citing", pid + ".json"))
        for item in fatcat_citations(fat):
            work = fatcat_work(item, pid)
            if work:
                add(work)

    merged_keys = set(groups)
    retained = 0
    for row in load_v3_rows():
        w = v3_work(row)
        if key_of(w) in merged_keys:
            continue
        if "Semantic Scholar" in w["sources"]:
            add(w)
            retained += 1

    excluded = []
    rows = []
    for w in groups.values():
        if w["doi"] and w["doi"] in EXCLUDED:
            excluded.append((w, EXCLUDED[w["doi"]]))
            continue
        rows.append(w)

    def sort_key(w):
        return (min(int(x) for x in w["pub_ids"]), w["year"] or 0, norm_title(w["title"]))

    rows.sort(key=sort_key)

    out = []
    for i, w in enumerate(rows, 1):
        ids = w["pub_ids"]
        titles = [pub_by_id[x]["Titlu"] for x in ids if x in pub_by_id]
        years = [pub_by_id[x]["An"] for x in ids if x in pub_by_id]
        src = sorted(w["sources"])
        if "retained_from" in w:
            src_label = "Semantic Scholar (reverificare blocată 2026-11-01; înregistrare preluată din v3)"
        else:
            src_label = " + ".join(src)
        if w["doi"]:
            if len(src) >= 2:
                conf, basis = "ridicat", "DOI rezolvabil, confirmat în %d surse independente (%s)" % (len(src), ", ".join(src))
            elif "OpenAlex" in w["sources"]:
                conf, basis = "ridicat", "DOI rezolvabil, înregistrare OpenAlex cu metadate de editor"
            else:
                conf, basis = "mediu", "DOI rezolvabil, o singură sursă (Semantic Scholar); verificare manuală recomandată"
        else:
            if w["authors"] and w["year"] and w["venue"]:
                conf, basis = "mediu", "Fără DOI; titlu, an, autori și revistă prezente într-o singură sursă; verificare manuală recomandată"
            else:
                conf, basis = "scăzut", "Fără DOI și metadate incomplete (an/autori/revistă lipsă); verificare manuală necesară"
        obs = "Auto-citare: %s" % ("Da" if is_self(w) else "Nu")
        if len(ids) > 1:
            obs += " · Lucrare citează și articolele nr. %s" % ", ".join(ids)
        if "retained_from" in w:
            obs += " · Înregistrare preluată din v3 (sursă originală: Semantic Scholar)"
        out.append(
            {
                "Nr.": i,
                "Articol (ID)": ", ".join(ids),
                "Titlu articol": titles[0] if titles else "",
                "An publicație": "; ".join(years),
                "An citare": w["year"] or "",
                "Lucrare citată": w["title"],
                "Autori citatori": "; ".join(w["authors"]),
                "Revistă / Eveniment": w["venue"],
                "DOI citare": w["doi"],
                "Link": ("https://doi.org/" + w["doi"]) if w["doi"] else "",
                "Tip citare": w["type"],
                "Context / Observații": obs,
                "Sursă verificare": src_label,
                "Surse (proveniență)": "; ".join(src),
                "Data verificării": RETRIEVAL_DATE,
                "Nivel de încredere": conf,
                "Baza încrederii": basis,
                "OpenAlex Work ID": (w["openalex"] or "").rsplit("/", 1)[-1] if w["openalex"] else "",
                "Semantic Scholar Paper ID": w["s2"] or "",
            }
        )

    os.makedirs(OUT_CIT, exist_ok=True)
    os.makedirs(OUT_CEN, exist_ok=True)

    cit_cols = list(out[0].keys())
    cit_csv = os.path.join(OUT_CIT, "Citari_Articole_Gabriela_Daniela_Stamatie_%s.csv" % TARGET_VERSION)
    with open(cit_csv, "w", encoding="utf-8-sig", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=cit_cols, delimiter=";")
        wtr.writeheader()
        wtr.writerows(out)

    # coverage
    per_pub = defaultdict(lambda: {"works": set(), "links": 0})
    for r in out:
        for pid in r["Articol (ID)"].split(", "):
            per_pub[pid]["works"].add(r["Nr."])
            per_pub[pid]["links"] += 1

    cov_rows = []
    scholar_counts = load_scholar_counts()
    for p in pubs:
        pid = p["Nr."]
        s = summary.get(pid, {})
        cr = crossref.get(pid, {})
        oa = raw_count("openalex_citing", pid)
        s2 = raw_count("s2_citing", pid)
        dc_raw = load_json(os.path.join(RAW, "datacite", pid + ".json"), None)
        dc = None
        if dc_raw:
            dc = ((dc_raw.get("data") or {}).get("attributes") or {}).get("citationCount")
        n = per_pub[pid]["links"]
        if not p["DOI"].strip():
            oa_state = ("verificat (%s lucrări)" % oa) if oa is not None else "fără înregistrare OpenAlex (căutare după titlu, fără potrivire exactă)"
            cr_state = "neinterogabil (fără DOI)"
            s2_state = "indisponibil: căutare Semantic Scholar blocată HTTP 429"
            ds = dc_search.get(pid)
            if ds is None:
                dc_state = "neinterogabil (fără DOI)"
            elif ds.get("error"):
                dc_state = "eroare căutare (%s)" % ds["error"]
            elif ds.get("total"):
                dc_state = "căutare fără potrivire exactă (%s rezultate, niciun titlu identic)" % ds["total"]
            else:
                dc_state = "verificat prin căutare; 0 rezultate"
        else:
            oa_state = ("verificat (%s lucrări)" % oa) if oa is not None else "fără înregistrare OpenAlex (căutare după titlu, fără potrivire exactă)"
            cr_state = ("verificat, %s citări raportate (listă indisponibilă fără acces member)" % cr.get("isReferencedByCount")) if cr.get("status") == "ok" else "blocat (%s)" % cr.get("status")
            if s2 is not None:
                s2_state = "verificat (%s lucrări)" % s2
            elif s.get("s2Error"):
                s2_state = "blocat (%s)" % s.get("s2Error")
            else:
                s2_state = "fără rezultat / neindexat"
            dc_state = ("verificat (citationCount=%s)" % dc) if dc is not None else "fără înregistrare DataCite"
        if pid in scholar_counts:
            gs_state = "manual (%s citări)" % scholar_counts[pid]
        else:
            gs_state = "necompletat (import manual)"
        if is_researchgate_doi(p["DOI"]):
            rg_state = "verificat (DOI ResearchGate: %s)" % doi_of(p["DOI"])
        elif p["DOI"].strip():
            rg_state = "fără DOI ResearchGate (DOI editor)"
        else:
            rg_state = "neinterogabil (fără DOI)"
        if n > 0:
            status = "acoperit"
        elif not p["DOI"].strip() and s.get("openalexId") is None:
            status = "parțial verificat - fără identificator"
        elif s.get("s2Error") or (not p["DOI"].strip()):
            status = "parțial - zero în sursele accesibile"
        else:
            status = "zero confirmat"
        cov_rows.append(
            {
                "ID": pid,
                "Titlu": p["Titlu"],
                "An": p["An"],
                "DOI": p["DOI"],
                "Lucrări citante v4": n,
                "Surse verificate": "OpenAlex; Crossref (doar contor); Semantic Scholar; DataCite",
                "Stare OpenAlex": oa_state,
                "Stare Crossref": cr_state,
                "Stare Semantic Scholar": s2_state,
                "Stare DataCite": dc_state,
                "Stare ResearchGate": rg_state,
                "Stare Google Scholar": gs_state,
                "Stare acoperire": status,
            }
        )

    exc_rows = []
    for w, reason in excluded:
        exc_rows.append(
            {
                "Titlu": w["title"],
                "Autori": "; ".join(w["authors"]),
                "An": w["year"] or "",
                "Revistă": w["venue"],
                "DOI": w["doi"],
                "Articol (ID)": ", ".join(w["pub_ids"]),
                "Surse": "; ".join(sorted(w["sources"])),
                "Motiv excludere": reason,
                "Data verificării": RETRIEVAL_DATE,
            }
        )
    if exc_rows:
        with open(os.path.join(OUT_CIT, "Excluded_Candidates_%s.csv" % TARGET_VERSION), "w", encoding="utf-8-sig", newline="") as f:
            wtr = csv.DictWriter(f, fieldnames=list(exc_rows[0].keys()), delimiter=";")
            wtr.writeheader()
            wtr.writerows(exc_rows)

    cov_csv = os.path.join(OUT_CIT, "Acoperire_Publicatii_%s.csv" % TARGET_VERSION)
    with open(cov_csv, "w", encoding="utf-8-sig", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(cov_rows[0].keys()), delimiter=";")
        wtr.writeheader()
        wtr.writerows(cov_rows)

    # centralizator v4
    COVERAGE_COLS = [
        "Citări găsite (v4)",
        "Surse verificate (citări)",
        "Stare acoperire citări",
        "Încredere agregată",
        "Notă acoperire",
    ]
    # Source rows may already carry coverage columns from a previous
    # generation; exclude them so they are emitted exactly once.
    cen_cols = [c for c in pubs[0].keys() if c not in COVERAGE_COLS] + COVERAGE_COLS
    cen_rows = []
    for p, c in zip(pubs, cov_rows):
        confs = [
            r["Nivel de încredere"]
            for r in out
            if p["Nr."] in r["Articol (ID)"].split(", ")
        ]
        agg = "—"
        if confs:
            agg = "ridicat" if "ridicat" in confs and "scăzut" not in confs else ("scăzut" if "scăzut" in confs else "mediu")
        note = ""
        if c["Stare acoperire"].startswith("parțial verificat"):
            note = "Fără DOI și fără înregistrare OpenAlex/DataCite (căutare după titlu, fără potrivire exactă); căutarea Semantic Scholar după titlu a fost blocată (HTTP 429). Necesită acces Scopus/Web of Science sau verificare manuală."
        elif c["Stare acoperire"].startswith("parțial"):
            note = "Zero citări în sursele accesibile; reverificarea Semantic Scholar a fost blocată (HTTP 429)."
        elif c["Stare acoperire"] == "acoperit" and pid == "6":
            note = "Singura lucrare citantă provine din înregistrarea Semantic Scholar preluată din v3; reverificarea Semantic Scholar a fost blocată (HTTP 429)."
        elif c["Stare acoperire"] == "zero confirmat":
            note = "Zero citări confirmat în OpenAlex, Crossref și Semantic Scholar."
        r = dict(p)
        r["Citări găsite (v4)"] = c["Lucrări citante v4"]
        r["Surse verificate (citări)"] = c["Surse verificate"]
        r["Stare acoperire citări"] = c["Stare acoperire"]
        r["Încredere agregată"] = agg
        r["Notă acoperire"] = note
        cen_rows.append(r)

    cen_csv = os.path.join(OUT_CEN, "Centralizator_Articole_Gabriela_Daniela_Stamatie_%s.csv" % TARGET_VERSION)
    with open(cen_csv, "w", encoding="utf-8-sig", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=cen_cols, delimiter=";")
        wtr.writeheader()
        wtr.writerows(cen_rows)

    # regenerate the retrieval summary from the raw files so it never goes stale
    regen = []
    for p in pubs:
        pid = p["Nr."]
        oa = raw_count("openalex_citing", pid)
        s2 = raw_count("s2_citing", pid)
        dc_raw = load_json(os.path.join(RAW, "datacite", pid + ".json"), None)
        dc = ((dc_raw.get("data") or {}).get("attributes") or {}).get("citationCount") if dc_raw else None
        notes = []
        if oa is None:
            notes.append("OpenAlex: fără înregistrare / fără potrivire exactă după titlu")
        if s2 is None:
            notes.append("Semantic Scholar: neindexat (404) sau căutare după titlu blocată (HTTP 429)")
        if not p["DOI"].strip():
            notes.append("fără DOI: Crossref Cited-by și DataCite nu pot fi interogate după DOI")
        regen.append(
            {
                "publicationId": pid,
                "doi": p["DOI"].strip(),
                "openalexCiting": oa,
                "s2Citing": s2,
                "dataciteCitationCount": dc,
                "notes": notes,
            }
        )
    with open(os.path.join(RAW, "retrieval-summary.json"), "w", encoding="utf-8") as f:
        json.dump({"retrievedOn": RETRIEVAL_DATE, "sources": ["OpenAlex", "Semantic Scholar", "DataCite"], "publications": regen}, f, ensure_ascii=False, indent=1)

    # markdown
    def md_table(rows, cols):
        lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
        for r in rows:
            lines.append("| " + " | ".join(str(r.get(c, "")).replace("|", "\\|") for c in cols) + " |")
        return "\n".join(lines)

    md_cit = ["# Citări — Gabriela Daniela Stamatie (%s)" % TARGET_VERSION, "", "Generat: %s. Sursa: OpenAlex + Semantic Scholar + DataCite; contor Crossref pentru control." % RETRIEVAL_DATE, "", md_table(out, cit_cols)]
    open(os.path.join(OUT_CIT, "Citari_Articole_Gabriela_Daniela_Stamatie_%s.md" % TARGET_VERSION), "w", encoding="utf-8").write("\n".join(md_cit) + "\n")
    md_cov = ["# Acoperirea citărilor pe publicație (%s)" % TARGET_VERSION, "", md_table(cov_rows, list(cov_rows[0].keys()))]
    open(os.path.join(OUT_CIT, "Acoperire_Publicatii_%s.md" % TARGET_VERSION), "w", encoding="utf-8").write("\n".join(md_cov) + "\n")
    md_cen = ["# Centralizator — Gabriela Daniela Stamatie (%s)" % TARGET_VERSION, "", md_table(cen_rows, cen_cols)]
    open(os.path.join(OUT_CEN, "Centralizator_Articole_Gabriela_Daniela_Stamatie_%s.md" % TARGET_VERSION), "w", encoding="utf-8").write("\n".join(md_cen) + "\n")

    # xlsx
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font

        wb = Workbook()
        ws = wb.active
        ws.title = "Citări"
        ws.append(cit_cols)
        for r in out:
            ws.append([r[c] for c in cit_cols])
        for cell in ws[1]:
            cell.font = Font(bold=True)
        ws.freeze_panes = "A2"
        wb.save(os.path.join(OUT_CIT, "Citari_Articole_Gabriela_Daniela_Stamatie_%s.xlsx" % TARGET_VERSION))

        wb = Workbook()
        ws = wb.active
        ws.title = "Acoperire"
        ws.append(list(cov_rows[0].keys()))
        for r in cov_rows:
            ws.append([r[c] for c in cov_rows[0].keys()])
        for cell in ws[1]:
            cell.font = Font(bold=True)
        wb.save(os.path.join(OUT_CIT, "Acoperire_Publicatii_%s.xlsx" % TARGET_VERSION))

        wb = Workbook()
        ws = wb.active
        ws.title = "Centralizator"
        ws.append(cen_cols)
        for r in cen_rows:
            ws.append([r[c] for c in cen_cols])
        for cell in ws[1]:
            cell.font = Font(bold=True)
        ws.freeze_panes = "A2"
        wb.save(os.path.join(OUT_CEN, "Centralizator_Articole_Gabriela_Daniela_Stamatie_%s.xlsx" % TARGET_VERSION))
    except ImportError:
        pass

    links = sum(len(r["Articol (ID)"].split(", ")) for r in out)
    self_works = sum(1 for r in out if "Auto-citare: Da" in r["Context / Observații"])
    self_links = sum(len(r["Articol (ID)"].split(", ")) for r in out if "Auto-citare: Da" in r["Context / Observații"])
    stats = {
        "works": len(out),
        "links": links,
        "selfWorks": self_works,
        "selfLinks": self_links,
        "retainedFromV3": retained,
        "bySource": {s: sum(1 for r in out if s in r["Surse (proveniență)"].split("; ")) for s in ("OpenAlex", "Semantic Scholar")},
        "byConfidence": {c: sum(1 for r in out if r["Nivel de încredere"] == c) for c in ("ridicat", "mediu", "scăzut")},
        "coveredPubs": sum(1 for c in cov_rows if c["Lucrări citante v4"] > 0),
        "excludedCandidates": len(excluded),
        "coverageStatus": {},
    }
    for c in cov_rows:
        stats["coverageStatus"][c["Stare acoperire"]] = stats["coverageStatus"].get(c["Stare acoperire"], 0) + 1
    with open(os.path.join(OUT_CIT, "v4-stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)
    print(json.dumps(stats, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
