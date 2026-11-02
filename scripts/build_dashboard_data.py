#!/usr/bin/env python3
"""Build dashboard data from the versioned bibliography CSV files.

Scans centralizator/v*/ and citari/v*/, normalises the 16-column publication
table and both citation table layouts, and writes:

  dashboard/data/<version>/publications.json
  dashboard/data/<version>/citations.json
  dashboard/data/version-manifest.json
  dashboard/data/dashboard-data.js   (offline / file:// fallback bundle)

No third-party dependencies; run with: python3 scripts/build_dashboard_data.py
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = ROOT / "dashboard"
DATA_DIR = DASHBOARD_DIR / "data"

# Date reported in the source workbook ("Data extragerii: 31 octombrie 2026").
DATA_EXTRACTED_AT = "2026-10-31"

PUBLICATION_TYPES = {
    "articol științific": "article",
    "articol stiintific": "article",
    "articol științific (abstract)": "abstract",
    "articol stiintific (abstract)": "abstract",
    "preprint": "preprint",
    "poster nepublicat": "poster",
    "poster": "poster",
}

CITATION_TYPES = {
    "articol": "article",
    "review": "review",
    "lucrare de conferință": "conference",
    "lucrare de conferinta": "conference",
    "conference paper": "conference",
    "capitol de carte": "chapter",
    "book chapter": "chapter",
    "preprint": "preprint",
    "poster": "poster",
    "teză": "thesis",
    "teza": "thesis",
}

AUTHOR_MARKER = "stamatie"
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s;]+", re.IGNORECASE)


def fold(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    return "".join(ch for ch in text if not unicodedata.combining(ch)).lower().strip()


def clean(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def parse_int(value: str, default: Optional[int] = None) -> Optional[int]:
    match = re.search(r"-?\d+", value or "")
    return int(match.group(0)) if match else default


def split_authors(value: str) -> List[str]:
    parts = re.split(r"\s*;\s*", value or "")
    return [clean(part) for part in parts if clean(part)]


def parse_article_ids(value: str) -> List[int]:
    """Parse the 'Articol (ID)' cell, which may list several ids (e.g. '1, 2, 3')."""
    ids: List[int] = []
    for part in re.split(r"[,;/]", value or ""):
        parsed = parse_int(part)
        if parsed is not None and parsed not in ids:
            ids.append(parsed)
    return ids


def normalize_doi(value: str) -> str:
    match = DOI_RE.search(value or "")
    if not match:
        return ""
    return match.group(0).rstrip(".,);]}>").lower()


def normalize_link(value: str, doi: str) -> str:
    value = clean(value)
    if not value:
        return f"https://doi.org/{doi}" if doi else ""
    if value.lower().startswith("10."):
        return f"https://doi.org/{value}"
    if re.match(r"^https?://", value, re.IGNORECASE):
        return value
    return ""


def type_code(label: str, mapping: Dict[str, str]) -> str:
    key = fold(label)
    return mapping.get(key, mapping.get(clean(label), "other"))


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=";,")
        except csv.Error:
            dialect = csv.excel
            dialect.delimiter = ";"
        reader = csv.DictReader(handle, dialect=dialect)
        rows: List[Dict[str, str]] = []
        for raw in reader:
            row = {}
            for key, value in raw.items():
                if key is None:
                    continue
                row[clean(key)] = clean(value)
            if any(row.values()):
                rows.append(row)
        return rows


FAMILY_REQUIRED_COLUMNS = {
    "centralizator": [("Nr.",), ("Titlu",)],
    "citari": [("Lucrare citată", "Titlu lucrare citantă"), ("Articol (ID)", "Articol citat (nr.)")],
}
COVERAGE_REQUIRED_COLUMNS = ("ID", "Stare acoperire")


def csv_header(path: Path) -> List[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(8192)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=";,")
        except csv.Error:
            dialect = csv.excel
            dialect.delimiter = ";"
        reader = csv.reader(handle, dialect=dialect)
        for row in reader:
            return [clean(cell) for cell in row]
    return []


def find_csv(directory: Path, family: str) -> Optional[Path]:
    """Pick the data CSV by header contract, never by filename alone.

    v4 folders contain several CSVs (data, coverage, excluded candidates); a
    filename sort would silently select the wrong one, so selection is driven
    by the columns the pipeline actually needs.
    """
    candidates = [
        path
        for path in sorted(directory.glob("*.csv"))
        if not path.name.startswith("~$")
    ]
    if not candidates:
        return None
    required = FAMILY_REQUIRED_COLUMNS.get(family)
    if required:
        matching = [
            path
            for path in candidates
            if all(any(column in csv_header(path) for column in group) for group in required)
        ]
        if matching:
            candidates = matching
    if len(candidates) > 1:
        prefix = "centralizator" if family == "centralizator" else "citari"
        preferred = [path for path in candidates if path.name.lower().startswith(prefix)]
        if preferred:
            candidates = preferred
        print(
            f"  note: multiple {family} CSVs in {directory.relative_to(ROOT)};"
            f" using {candidates[0].name}"
        )
    return candidates[0]


def find_coverage_csv(directory: Path) -> Optional[Path]:
    for path in sorted(directory.glob("*.csv")):
        if path.name.startswith("~$"):
            continue
        header = csv_header(path)
        if all(column in header for column in COVERAGE_REQUIRED_COLUMNS):
            return path
    return None


def discover_versions() -> Dict[str, Dict[str, Path]]:
    versions: Dict[str, Dict[str, Path]] = {}
    for family in ("centralizator", "citari"):
        base = ROOT / family
        if not base.is_dir():
            continue
        for directory in sorted(base.iterdir()):
            match = re.fullmatch(r"v(\d+)", directory.name, re.IGNORECASE)
            if not directory.is_dir() or not match:
                continue
            csv_path = find_csv(directory, family)
            if not csv_path:
                print(f"  skip: no {family} CSV in {directory.relative_to(ROOT)}")
                continue
            versions.setdefault(directory.name.lower(), {})[family] = csv_path
    return versions


def version_key(version: str) -> tuple:
    match = re.search(r"\d+", version)
    return (int(match.group(0)) if match else -1, version)


def split_list(value: str) -> List[str]:
    return [clean(part) for part in re.split(r"[;,]", value or "") if clean(part)]


def normalize_publications(rows: Iterable[Dict[str, str]]) -> List[Dict[str, Any]]:
    publications: List[Dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        doi = normalize_doi(row.get("DOI", ""))
        link = normalize_link(row.get("Link", ""), doi)
        label = row.get("Tip", "")
        publication = {
            "id": parse_int(row.get("Nr.", ""), index) or index,
            "year": parse_int(row.get("An", "")),
            "typeCode": type_code(label, PUBLICATION_TYPES),
            "typeLabel": label,
            "title": row.get("Titlu", ""),
            "venue": row.get("Revistă / Publicație", ""),
            "volume": row.get("Volum (Issue)", ""),
            "pages": row.get("Pagini / Nr. articol", ""),
            "doi": doi,
            "link": link,
            "authors": split_authors(row.get("Toți autorii", "")),
            "coauthors": split_authors(row.get("Co-autori (fără G. D. Stamatie)", "")),
            "position": row.get("Poziția autoarei", ""),
            "issn": row.get("ISSN", ""),
            "pmid": row.get("PMID / PMCID", ""),
            "source": row.get("Sursa verificării", ""),
            "notes": row.get("Note / incertitudine", ""),
        }
        if "Stare acoperire citări" in row or "Citări găsite (v4)" in row:
            publication.update(
                {
                    "citationsFound": parse_int(row.get("Citări găsite (v4)", "")),
                    "verifiedSources": split_list(row.get("Surse verificate (citări)", "")),
                    "coverageStatus": row.get("Stare acoperire citări", ""),
                    "confidence": row.get("Încredere agregată", ""),
                    "coverageNote": row.get("Notă acoperire", ""),
                }
            )
        publications.append(publication)
    publications.sort(key=lambda item: item["id"])
    return publications


def is_self_citation(value: str, authors: Iterable[str]) -> bool:
    folded_authors = " ; ".join(fold(author) for author in authors)
    if AUTHOR_MARKER in folded_authors:
        return True
    return bool(re.search(r"auto-?citare\s*[:\-]?\s*(da|yes|true)", fold(value)))


def normalize_citations(
    rows: Iterable[Dict[str, str]], publications: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    publication_years = {pub["id"]: pub.get("year") for pub in publications}
    publication_titles = {pub["id"]: pub.get("title", "") for pub in publications}
    citations: List[Dict[str, Any]] = []

    for index, row in enumerate(rows, start=1):
        if "Articol (ID)" in row:
            citation_id = parse_int(row.get("Nr.", ""), index) or index
            article_ids = parse_article_ids(row.get("Articol (ID)", ""))
            article_title = row.get("Titlu articol", "")
            article_year = parse_int(row.get("An publicație", ""))
            authors = split_authors(row.get("Autori citatori", ""))
            venue = row.get("Revistă / Eveniment", "")
            doi = normalize_doi(row.get("DOI citare", ""))
            link = normalize_link(row.get("Link", ""), doi)
            label = row.get("Tip citare", "")
            context = row.get("Context / Observații", "")
            source = row.get("Sursă verificare", "")
            title = row.get("Lucrare citată", "")
        else:
            citation_id = parse_int(row.get("Nr. crt.", ""), index) or index
            article_ids = parse_article_ids(row.get("Articol citat (nr.)", ""))
            article_title = row.get("Articol citat – titlu", "")
            article_year = publication_years.get(article_ids[0] if article_ids else None)
            authors = split_authors(row.get("Autori", ""))
            venue = row.get("Revistă / Conferință", "")
            combined = row.get("DOI / Link", "")
            doi = normalize_doi(combined)
            link = normalize_link(combined, doi)
            label = row.get("Tip", "")
            self_flag = row.get("Auto-citare", "")
            context = " · ".join(
                part for part in (segment_context(self_flag), row.get("Note", "")) if part
            )
            source = row.get("Sursă", "")
            title = row.get("Titlu lucrare citantă", "")

        article_id = article_ids[0] if article_ids else None
        if not article_title and article_id is not None:
            article_title = publication_titles.get(article_id, "")
        if article_year is None and article_id is not None:
            article_year = publication_years.get(article_id)

        citation = {
            "id": citation_id,
            "articleId": article_id,
            "articleIds": article_ids,
            "articleTitle": article_title,
            "articleYear": article_year,
            "year": parse_int(row.get("An citare", "")),
            "title": title,
            "authors": authors,
            "venue": venue,
            "doi": doi,
            "link": link,
            "typeCode": type_code(label, CITATION_TYPES),
            "typeLabel": label,
            "selfCitation": is_self_citation(context, authors),
            "context": row.get("Context / Observații", "") if "Context / Observații" in row else row.get("Note", ""),
            "source": source,
        }
        if "Surse (proveniență)" in row or "Nivel de încredere" in row:
            citation.update(
                {
                    "provenance": split_list(row.get("Surse (proveniență)", "")),
                    "verifiedOn": row.get("Data verificării", ""),
                    "confidence": row.get("Nivel de încredere", ""),
                    "confidenceBasis": row.get("Baza încrederii", ""),
                    "openAlexId": row.get("OpenAlex Work ID", ""),
                    "semanticScholarId": row.get("Semantic Scholar Paper ID", ""),
                }
            )
        citations.append(citation)
    citations.sort(key=lambda item: (item["id"], item["articleId"] or 0))
    return citations


def normalize_coverage(rows: Iterable[Dict[str, str]]) -> List[Dict[str, Any]]:
    coverage: List[Dict[str, Any]] = []
    for row in rows:
        coverage.append(
            {
                "id": parse_int(row.get("ID", "")),
                "title": row.get("Titlu", ""),
                "year": parse_int(row.get("An", "")),
                "doi": normalize_doi(row.get("DOI", "")),
                "citations": parse_int(row.get("Lucrări citante v4", "")),
                "verifiedSources": split_list(row.get("Surse verificate", "")),
                "status": row.get("Stare acoperire", ""),
                "sources": {
                    "openalex": row.get("Stare OpenAlex", ""),
                    "crossref": row.get("Stare Crossref", ""),
                    "semanticScholar": row.get("Stare Semantic Scholar", ""),
                    "datacite": row.get("Stare DataCite", ""),
                },
            }
        )
    coverage.sort(key=lambda item: item["id"] or 0)
    return coverage


def segment_context(flag: str) -> str:
    flag = clean(flag)
    if not flag:
        return ""
    if fold(flag) in {"da", "yes", "true", "1"}:
        return "Auto-citare: Da"
    if fold(flag) in {"nu", "no", "false", "0"}:
        return ""
    return f"Auto-citare: {flag}"


def stats_for(publications: List[Dict[str, Any]], citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    self_citations = [citation for citation in citations if citation["selfCitation"]]
    self_count = len(self_citations)
    with_doi = sum(1 for publication in publications if publication["doi"])
    years = sorted(
        {publication["year"] for publication in publications if publication.get("year") is not None}
    )
    citation_links = sum(len(citation.get("articleIds") or []) for citation in citations)
    self_links = sum(len(citation.get("articleIds") or []) for citation in self_citations)
    return {
        "publications": len(publications),
        "citations": len(citations),
        "citationLinks": citation_links,
        "selfCitations": self_count,
        "externalCitations": len(citations) - self_count,
        "selfCitationLinks": self_links,
        "externalCitationLinks": citation_links - self_links,
        "publicationsWithDoi": with_doi,
        "citingVenues": len({citation["venue"] for citation in citations if citation["venue"]}),
        "publicationYearRange": [years[0], years[-1]] if years else None,
    }


def validate(
    version: str,
    publications: List[Dict[str, Any]],
    citations: List[Dict[str, Any]],
    coverage: Optional[List[Dict[str, Any]]] = None,
) -> List[str]:
    """Hard validation gates. Any problem aborts the build.

    A wrong CSV in the folder used to produce plausible-looking but meaningless
    numbers (v4 coverage sheet parsed as citations), so this checks identity,
    reconciliation and coverage consistency instead of only id uniqueness.
    """
    problems: List[str] = []
    pub_ids = {publication["id"] for publication in publications}
    if len(pub_ids) != len(publications):
        problems.append(f"{version}: duplicate publication ids")
    cit_ids = {citation["id"] for citation in citations}
    if len(cit_ids) != len(citations):
        problems.append(f"{version}: duplicate citation ids")
    missing = {
        article_id
        for citation in citations
        for article_id in (citation.get("articleIds") or [])
        if article_id not in pub_ids
    }
    if missing:
        problems.append(f"{version}: citations reference unknown article ids {sorted(missing)}")
    no_title = sum(1 for publication in publications if not publication["title"])
    if no_title:
        problems.append(f"{version}: {no_title} publications without title")
    if not citations:
        problems.append(f"{version}: no citations parsed")
    anonymous = [c["id"] for c in citations if not c["title"] and not c["doi"]]
    if anonymous:
        problems.append(f"{version}: {len(anonymous)} citations without title or DOI")
    duplicate_dois = [
        doi for doi, count in Counter(c["doi"] for c in citations if c["doi"]).items() if count > 1
    ]
    if duplicate_dois:
        problems.append(f"{version}: duplicate citation DOIs {duplicate_dois}")

    counts = Counter()
    for citation in citations:
        for article_id in citation.get("articleIds") or []:
            counts[article_id] += 1
    if any("citationsFound" in publication for publication in publications):
        for publication in publications:
            declared = publication.get("citationsFound")
            actual = counts.get(publication["id"], 0)
            if declared is not None and declared != actual:
                problems.append(
                    f"{version}: publication {publication['id']} declares"
                    f" {declared} citations but {actual} rows were parsed"
                )

    if coverage is not None:
        coverage_ids = [row["id"] for row in coverage]
        if len(set(coverage_ids)) != len(coverage_ids):
            problems.append(f"{version}: duplicate coverage ids")
        missing_coverage = sorted(pub_ids - set(coverage_ids))
        extra_coverage = sorted(set(coverage_ids) - pub_ids)
        if missing_coverage:
            problems.append(f"{version}: no coverage row for publications {missing_coverage}")
        if extra_coverage:
            problems.append(f"{version}: coverage rows for unknown publications {extra_coverage}")
        blank_status = [row["id"] for row in coverage if not row["status"]]
        if blank_status:
            problems.append(f"{version}: blank coverage status for publications {blank_status}")
        for row in coverage:
            declared = row.get("citations")
            actual = counts.get(row["id"], 0)
            if declared is not None and declared != actual:
                problems.append(
                    f"{version}: coverage for publication {row['id']} declares"
                    f" {declared} citations but {actual} rows were parsed"
                )
    return problems


def citation_key(citation: Dict[str, Any]) -> str:
    if citation.get("doi"):
        return "doi:" + citation["doi"]
    return "title:" + fold(citation.get("title", "")) + "|" + str(citation.get("year") or "")


def citation_brief(citation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "key": citation_key(citation),
        "title": citation.get("title", ""),
        "year": citation.get("year"),
        "doi": citation.get("doi", ""),
        "articleIds": citation.get("articleIds") or [],
        "sources": citation.get("provenance") or ([citation["source"]] if citation.get("source") else []),
    }


def build_changelog(versions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Auditable diff between consecutive version pairs (works and links)."""
    changelog: List[Dict[str, Any]] = []
    for previous, current in zip(versions, versions[1:]):
        previous_works = {citation_key(c): c for c in previous["citations"]}
        current_works = {citation_key(c): c for c in current["citations"]}
        added = [citation_brief(current_works[key]) for key in sorted(set(current_works) - set(previous_works))]
        removed = [citation_brief(previous_works[key]) for key in sorted(set(previous_works) - set(current_works))]

        def per_publication(entry: Dict[str, Any]) -> Dict[int, int]:
            counts: Counter = Counter()
            for citation in entry["citations"]:
                for article_id in citation.get("articleIds") or []:
                    counts[article_id] += 1
            return dict(counts)

        before = per_publication(previous)
        after = per_publication(current)
        publication_changes = [
            {
                "id": article_id,
                "from": before.get(article_id, 0),
                "to": after.get(article_id, 0),
                "delta": after.get(article_id, 0) - before.get(article_id, 0),
            }
            for article_id in sorted(set(before) | set(after))
            if before.get(article_id, 0) != after.get(article_id, 0)
        ]
        changelog.append(
            {
                "from": previous["version"],
                "to": current["version"],
                "totals": {
                    "works": {"from": len(previous["citations"]), "to": len(current["citations"])},
                    "links": {
                        "from": previous["stats"]["citationLinks"],
                        "to": current["stats"]["citationLinks"],
                    },
                },
                "publications": publication_changes,
                "added": added,
                "removed": removed,
            }
        )
    return changelog


def input_digest(paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted({path.resolve() for path in paths}, key=lambda item: item.as_posix()):
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def build_timestamp(citations: List[Dict[str, Any]]) -> str:
    """Reproducible timestamp: SOURCE_DATE_EPOCH, else the newest data date."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.fromtimestamp(int(epoch), timezone.utc).replace(microsecond=0).isoformat()
    dates = sorted({c["verifiedOn"] for c in citations if c.get("verifiedOn")})
    if dates:
        return dates[-1] + "T00:00:00+00:00"
    return DATA_EXTRACTED_AT + "T00:00:00+00:00"


def build_manifest(
    versions: List[Dict[str, Any]],
    digest: str = "",
    generated_at: str = "",
    source_retrieved_at: Optional[str] = None,
) -> Dict[str, Any]:
    latest = max(versions, key=lambda item: version_key(item["version"]))
    source_counter = Counter(
        citation["source"] for citation in latest["citations"] if citation["source"]
    )
    publications = latest["publications"]
    verified_dates = sorted(
        {citation["verifiedOn"] for citation in latest["citations"] if citation.get("verifiedOn")}
    )
    last_verified = verified_dates[-1] if verified_dates else None

    def citation_sources(citation: Dict[str, Any]) -> List[str]:
        provenance = citation.get("provenance") or []
        if provenance:
            return provenance
        return [citation["source"]] if citation.get("source") else []

    def citation_link_count(name: str) -> int:
        return sum(
            len(citation.get("articleIds") or [])
            for citation in latest["citations"]
            if any(name.lower() in fold(source) for source in citation_sources(citation))
        )

    crossref_publications = sum(
        1 for publication in publications if "crossref" in fold(publication.get("source", ""))
    )
    datacite_publications = sum(
        1 for publication in publications if "datacite" in fold(publication.get("source", ""))
    )
    orcid_publications = sum(
        1 for publication in publications if "orcid" in fold(publication.get("source", ""))
    )

    sources = [
        {
            "id": "openalex",
            "name": "OpenAlex",
            "url": "https://openalex.org",
            "count": citation_link_count("openalex"),
            "countKind": "citationLinks",
        },
        {
            "id": "semantic-scholar",
            "name": "Semantic Scholar",
            "url": "https://www.semanticscholar.org",
            "count": citation_link_count("semantic scholar"),
            "countKind": "citationLinks",
        },
        {
            "id": "crossref",
            "name": "Crossref",
            "url": "https://www.crossref.org",
            "count": crossref_publications,
            "countKind": "publicationsVerified",
        },
        {
            "id": "datacite",
            "name": "DataCite",
            "url": "https://datacite.org",
            "count": datacite_publications,
            "countKind": "publicationsVerified",
        },
        {
            "id": "orcid",
            "name": "ORCID",
            "url": "https://orcid.org",
            "count": orcid_publications or None,
            "countKind": "publicationsVerified",
        },
    ]

    return {
        "schemaVersion": 2,
        "project": "Gabriela Daniela Stamatie — bibliografie și citări",
        "generatedAt": generated_at
        or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "generatedAtRule": "SOURCE_DATE_EPOCH if set, else newest citation verification date",
        "inputDigest": digest,
        "pipeline": {
            "script": "scripts/build_dashboard_data.py",
            "schemaVersion": 2,
            "command": "python3 scripts/build_dashboard_data.py",
        },
        "dataExtractedAt": DATA_EXTRACTED_AT,
        "latest": {
            "common": latest["version"],
            "centralizator": latest["version"],
            "citari": latest["version"],
        },
        "resolution": {
            "order": ["manifest", "folder-scan", "embedded-fallback"],
            "rule": "Highest numeric vN present in both centralizator/vN and citari/vN",
        },
        "versions": [
            {
                "version": item["version"],
                "centralizator": {
                    "csv": item["sources"]["centralizator"],
                    "records": len(item["publications"]),
                },
                "citari": {
                    "csv": item["sources"]["citari"],
                    "records": len(item["citations"]),
                },
                "stats": item["stats"],
                "coverageStats": item.get("coverageStats"),
                "data": {
                    "publications": f"data/{item['version']}/publications.json",
                    "citations": f"data/{item['version']}/citations.json",
                    "coverage": (
                        f"data/{item['version']}/coverage.json"
                        if item.get("coverage")
                        else None
                    ),
                },
            }
            for item in versions
        ],
        "sources": sources,
        "stats": latest["stats"],
        "changelog": "data/changelog.json",
        "lastVerified": last_verified,
        "sourceRetrievedAt": source_retrieved_at or None,
        "freshness": {
            "value": last_verified or (generated_at or DATA_EXTRACTED_AT)[:10],
            "label": "newest citation verification date",
            "rule": "newest 'Data verificării' across citation rows; generatedAt otherwise",
        },
    }


def relative(path: Path) -> str:
    return "../" + path.relative_to(ROOT).as_posix()


def retrieval_date(citations_path: Path) -> Optional[str]:
    summary = citations_path.parent / "raw" / "retrieval-summary.json"
    if not summary.exists():
        return None
    try:
        payload = json.loads(summary.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    value = payload.get("retrievedOn")
    return str(value) if value else None


def validate_columns(version: str, family: str, path: Path) -> List[str]:
    header = csv_header(path)
    problems = []
    for group in FAMILY_REQUIRED_COLUMNS.get(family, []):
        if not any(column in header for column in group):
            problems.append(f"{version}: {family} CSV lacks required column {group[0]!r}")
    return problems


def collect(complete: Dict[str, Dict[str, Path]]) -> tuple:
    prepared: List[Dict[str, Any]] = []
    problems: List[str] = []
    input_paths: List[Path] = []

    for version in sorted(complete, key=version_key):
        paths = complete[version]
        print(f"\n{version}")
        print(f"  publications: {paths['centralizator'].relative_to(ROOT)}")
        print(f"  citations:    {paths['citari'].relative_to(ROOT)}")
        problems.extend(validate_columns(version, "centralizator", paths["centralizator"]))
        problems.extend(validate_columns(version, "citari", paths["citari"]))
        publications = normalize_publications(read_csv(paths["centralizator"]))
        citations = normalize_citations(read_csv(paths["citari"]), publications)
        coverage_path = find_coverage_csv(paths["citari"].parent)
        coverage: Optional[List[Dict[str, Any]]] = None
        if coverage_path:
            print(f"  coverage:     {coverage_path.relative_to(ROOT)}")
            header = csv_header(coverage_path)
            missing = [column for column in COVERAGE_REQUIRED_COLUMNS if column not in header]
            if missing:
                problems.append(f"{version}: coverage CSV lacks columns {missing}")
            coverage = normalize_coverage(read_csv(coverage_path))
        input_paths.extend([paths["centralizator"], paths["citari"]])
        if coverage_path:
            input_paths.append(coverage_path)
        stats = stats_for(publications, citations)
        print(
            "  parsed:"
            f" {stats['publications']} publications,"
            f" {stats['citations']} citations,"
            f" {stats['citationLinks']} links,"
            f" {stats['selfCitations']} self-citations"
        )
        problems.extend(validate(version, publications, citations, coverage))

        coverage_stats: Optional[Dict[str, Any]] = None
        if coverage is not None:
            status_counts = Counter(row["status"] for row in coverage)
            coverage_stats = {
                "publications": len(coverage),
                "covered": status_counts.get("acoperit", 0),
                "zeroConfirmed": status_counts.get("zero confirmat", 0),
                "partiallyVerified": sum(
                    count for status, count in status_counts.items() if status.startswith("parțial")
                ),
                "byStatus": dict(sorted(status_counts.items())),
            }

        prepared.append(
            {
                "version": version,
                "publications": publications,
                "citations": citations,
                "coverage": coverage,
                "coverageStats": coverage_stats,
                "stats": stats,
                "retrievedAt": retrieval_date(paths["citari"]),
                "sources": {
                    "centralizator": relative(paths["centralizator"]),
                    "citari": relative(paths["citari"]),
                    "coverage": relative(coverage_path) if coverage_path else None,
                },
            }
        )

    return prepared, problems, input_paths


def validate_manifest(manifest: Dict[str, Any], prepared: List[Dict[str, Any]]) -> List[str]:
    problems: List[str] = []
    latest = prepared[-1]
    if manifest["stats"] != latest["stats"]:
        problems.append("manifest stats do not match the generated data")
    for item in prepared:
        entry = next(entry for entry in manifest["versions"] if entry["version"] == item["version"])
        stats = item["stats"]
        if entry["centralizator"]["records"] != len(item["publications"]):
            problems.append(f"{item['version']}: manifest publication records mismatch")
        if entry["citari"]["records"] != len(item["citations"]):
            problems.append(f"{item['version']}: manifest citation records mismatch")
        links = sum(len(citation.get("articleIds") or []) for citation in item["citations"])
        if stats["citationLinks"] != links:
            problems.append(f"{item['version']}: citation links do not reconcile")
        self_links = sum(
            len(citation.get("articleIds") or [])
            for citation in item["citations"]
            if citation["selfCitation"]
        )
        if stats["selfCitations"] != sum(1 for c in item["citations"] if c["selfCitation"]):
            problems.append(f"{item['version']}: self-citation work count does not reconcile")
        if stats["selfCitationLinks"] != self_links:
            problems.append(f"{item['version']}: self-citation link count does not reconcile")
    return problems


def previous_dataset(version: str) -> tuple:
    publications = DATA_DIR / version / "publications.json"
    citations = DATA_DIR / version / "citations.json"
    if not (publications.exists() and citations.exists()):
        return None, None
    return (
        json.loads(publications.read_text(encoding="utf-8")),
        json.loads(citations.read_text(encoding="utf-8")),
    )


def dataset_diff(previous: Optional[List[Dict[str, Any]]], current: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Diff between the previous stored run and the freshly normalized data."""
    if previous is None:
        return {"comparedAgainst": None, "added": [], "removed": [], "changed": []}
    before = {citation_key(citation): citation for citation in previous}
    after = {citation_key(citation): citation for citation in current}
    added = [citation_brief(after[key]) for key in sorted(set(after) - set(before))]
    removed = [citation_brief(before[key]) for key in sorted(set(before) - set(after))]
    changed = []
    for key in sorted(set(before) & set(after)):
        fields = {}
        for field in ("articleIds", "provenance", "confidence"):
            old_value = before[key].get(field)
            new_value = after[key].get(field)
            if (old_value or None) != (new_value or None):
                fields[field] = {"from": old_value, "to": new_value}
        if fields:
            changed.append(
                {"key": key, "title": after[key].get("title", ""), "changes": fields}
            )
    return {"comparedAgainst": None, "added": added, "removed": removed, "changed": changed}


def changelog_markdown(document: Dict[str, Any]) -> str:
    lines = [
        "# Citation changelog",
        "",
        f"Generated: {document['generatedAt']}",
        f"Input digest: `{document['inputDigest']}`",
        f"Work identity: {document['rule']}",
        "",
        "## Between dataset versions",
        "",
    ]
    for entry in document["versions"]:
        totals = entry["totals"]
        lines.append(
            f"- **{entry['from']} → {entry['to']}**: works"
            f" {totals['works']['from']} → {totals['works']['to']}, links"
            f" {totals['links']['from']} → {totals['links']['to']},"
            f" {len(entry['added'])} added, {len(entry['removed'])} removed"
        )
        for change in entry["publications"]:
            lines.append(
                f"  - publication {change['id']}: {change['from']} → {change['to']}"
                f" ({change['delta']:+d})"
            )
    run = document["run"]
    lines.extend(["", "## Since the previous build", ""])
    if run["comparedAgainst"]:
        lines.append(
            f"Compared with `{run['comparedAgainst']}`: {len(run['added'])} added,"
            f" {len(run['removed'])} removed, {len(run['changed'])} changed."
        )
    else:
        lines.append("No previous generated data for this version — baseline run.")
    for brief in run["added"]:
        lines.append(f"- added: {brief['title']} ({brief['year'] or 'n.d.'})")
    for brief in run["removed"]:
        lines.append(f"- removed: {brief['title']} ({brief['year'] or 'n.d.'})")
    for change in run["changed"]:
        lines.append(f"- changed: {change['title']} — {', '.join(change['changes'])}")
    lines.append("")
    return "\n".join(lines)


def report_problems(problems: List[str]) -> None:
    print("\nvalidation failed:", file=sys.stderr)
    for problem in problems:
        print(f"  - {problem}", file=sys.stderr)
    print("\nnothing was written; fix the inputs and re-run.", file=sys.stderr)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the dashboard data bundle from versioned CSV inputs.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate only; write nothing and exit non-zero on problems",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="compare the rebuilt data with the previous run; write nothing",
    )
    args = parser.parse_args(argv)
    if args.check and args.diff:
        parser.error("--check and --diff are mutually exclusive")

    if not (ROOT / "centralizator").is_dir() or not (ROOT / "citari").is_dir():
        print("error: run from a project containing centralizator/ and citari/", file=sys.stderr)
        return 1

    print(f"project: {ROOT}")
    discovered = discover_versions()
    if not discovered:
        print("error: no versioned CSV pairs found", file=sys.stderr)
        return 1

    complete = {
        version: paths
        for version, paths in discovered.items()
        if {"centralizator", "citari"} <= set(paths)
    }
    if not complete:
        print("error: no version has both centralizator and citari CSVs", file=sys.stderr)
        return 1

    prepared, problems, input_paths = collect(complete)
    if problems:
        report_problems(problems)
        return 1

    digest = input_digest(input_paths)
    generated_at = build_timestamp(prepared[-1]["citations"])
    manifest = build_manifest(
        prepared,
        digest=digest,
        generated_at=generated_at,
        source_retrieved_at=prepared[-1]["retrievedAt"],
    )
    problems.extend(validate_manifest(manifest, prepared))
    if problems:
        report_problems(problems)
        return 1

    latest_version = prepared[-1]["version"]
    _, previous_citations = previous_dataset(latest_version)
    run = dataset_diff(previous_citations, prepared[-1]["citations"])
    if previous_citations is not None:
        run["comparedAgainst"] = f"dashboard/data/{latest_version}"

    if args.check:
        manifest_path = DATA_DIR / "version-manifest.json"
        if not manifest_path.exists():
            print(
                f"\nvalidation failed: {manifest_path.relative_to(ROOT)} is missing;"
                " run the build",
                file=sys.stderr,
            )
            return 1
        stored = json.loads(manifest_path.read_text(encoding="utf-8"))
        if stored.get("inputDigest") != digest:
            print(
                f"\nvalidation failed: {manifest_path.relative_to(ROOT)} was built from"
                " different inputs; run the build",
                file=sys.stderr,
            )
            return 1
        print("\nvalidation: OK (generated data matches the current inputs)")
        return 0

    if args.diff:
        print("\ndiff against the previous run:")
        if run["comparedAgainst"] is None:
            print("  no previous generated data for this version — baseline run")
        else:
            print(f"  compared with {run['comparedAgainst']}")
            print(
                f"  {len(run['added'])} added, {len(run['removed'])} removed,"
                f" {len(run['changed'])} changed"
            )
            for brief in run["added"]:
                print(f"  + {brief['title']} ({brief['year'] or 'n.d.'})")
            for brief in run["removed"]:
                print(f"  - {brief['title']} ({brief['year'] or 'n.d.'})")
            for change in run["changed"]:
                print(f"  ~ {change['title']}: {', '.join(change['changes'])}")
        print("\nvalidation: OK")
        return 0

    document = {
        "schemaVersion": 1,
        "generatedAt": manifest["generatedAt"],
        "inputDigest": digest,
        "rule": "Citation works are matched by DOI, then by folded title and year.",
        "versions": build_changelog(prepared),
        "run": run,
    }
    datasets = {
        item["version"]: {
            "publications": item["publications"],
            "citations": item["citations"],
            "coverage": item["coverage"],
        }
        for item in prepared
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for item in prepared:
        version_dir = DATA_DIR / item["version"]
        version_dir.mkdir(parents=True, exist_ok=True)
        (version_dir / "publications.json").write_text(
            json.dumps(item["publications"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (version_dir / "citations.json").write_text(
            json.dumps(item["citations"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        if item["coverage"] is not None:
            (version_dir / "coverage.json").write_text(
                json.dumps(item["coverage"], ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    (DATA_DIR / "version-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "changelog.json").write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "changelog.md").write_text(changelog_markdown(document), encoding="utf-8")

    bundle = {"manifest": manifest, "datasets": datasets, "changelog": document}
    serialized = json.dumps(bundle, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (DATA_DIR / "dashboard-data.js").write_text(
        "/* Generated by scripts/build_dashboard_data.py — do not edit by hand. */\n"
        f"window.DASHBOARD_DATA={serialized};\n",
        encoding="utf-8",
    )

    for entry in document["versions"]:
        totals = entry["totals"]
        print(
            f"\nchangelog {entry['from']} -> {entry['to']}:"
            f" works {totals['works']['from']} -> {totals['works']['to']},"
            f" links {totals['links']['from']} -> {totals['links']['to']},"
            f" +{len(entry['added'])} added, -{len(entry['removed'])} removed"
        )
        for change in entry["publications"]:
            print(
                f"  publication {change['id']}: {change['from']} -> {change['to']}"
                f" ({change['delta']:+d})"
            )

    print(
        f"\nsince previous build: {len(run['added'])} added,"
        f" {len(run['removed'])} removed, {len(run['changed'])} changed"
    )
    print(f"\nlatest: {manifest['latest']['common']} (verified {manifest['freshness']['value']})")
    print(f"wrote:  {DATA_DIR.relative_to(ROOT)}")
    print("validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
