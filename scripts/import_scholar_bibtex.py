#!/usr/bin/env python3
"""Import the author's own Google Scholar BibTeX export.

Google Scholar has no public API and blocks automated access, so the only
supported path is the official profile export (BibTeX). This script parses
citari/google_scholar_export.bib, matches entries against the current
centralizator version by normalised title, and writes
citari/google_scholar_works.json:

  * matched       — Scholar works that already exist in the centralizator
  * newCandidates — Scholar works NOT yet in the centralizator (candidates
                    for future versions; nothing is auto-added)

Nothing in the versioned CSVs is modified. Re-export from Scholar and
replace the .bib file whenever the profile changes; the monthly workflow
re-runs this import automatically.
"""

import csv
import glob
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIB_PATH = os.path.join(ROOT, "citari", "google_scholar_export.bib")
OUT_PATH = os.path.join(ROOT, "citari", "google_scholar_works.json")

_LATEX_MAP = {
    r"{\u{a}}": "ă", r"{\u{A}}": "Ă",
    r"{\u{t}}": "ț", r"{\u{T}}": "Ț",
    r"{\u{s}}": "ș", r"{\u{S}}": "Ș",
    r"{\u{i}}": "i", r"{\u{I}}": "I",
    r"{\u{a}}": "ă", r"{\u{â}}": "â",
    r"\&": "&", r"\%": "%",
}


def decode_latex(text):
    for raw, replacement in _LATEX_MAP.items():
        text = text.replace(raw, replacement)
    text = text.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", text).strip()


def fold_title(text):
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_bibtex(text):
    """Parse @type{key, field={value}, ...} entries (brace-safe)."""
    entries = []
    pos = 0
    n = len(text)
    while True:
        at = text.find("@", pos)
        if at == -1:
            break
        brace = text.find("{", at)
        if brace == -1:
            break
        entry_type = text[at + 1:brace].strip().lower()
        # find matching close brace
        depth = 0
        i = brace
        while i < n:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        body = text[brace + 1:i]
        pos = i + 1
        key, _, rest = body.partition(",")
        fields = {}
        # field = {value} or field = "value"
        pattern = re.compile(r"(\w+)\s*=\s*(\{|\"\"\"|\"|\d+|[\w\.\-]+)", re.S)
        idx = 0
        while idx < len(rest):
            match = pattern.search(rest, idx)
            if not match:
                break
            name = match.group(1).lower()
            start = match.start(2)
            if rest[start] == "{":
                depth = 0
                j = start
                while j < len(rest):
                    if rest[j] == "{":
                        depth += 1
                    elif rest[j] == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                value = rest[start + 1:j]
                idx = j + 1
            elif rest[start] == '"':
                end = rest.find('"', start + 1)
                value = rest[start + 1:end if end != -1 else len(rest)]
                idx = (end + 1) if end != -1 else len(rest)
            else:
                value = match.group(2)
                idx = match.end(2)
            fields[name] = decode_latex(value)
        authors = [a.strip() for a in fields.get("author", "").split(" and ") if a.strip() and a.strip().lower() != "others"]
        year_raw = fields.get("year", "")
        entries.append({
            "key": key.strip(),
            "type": entry_type,
            "title": fields.get("title", ""),
            "authors": authors,
            "journal": fields.get("journal", ""),
            "year": int(year_raw) if year_raw.isdigit() else None,
            "volume": fields.get("volume", ""),
            "doi": fields.get("doi", "").strip(),
        })
    return entries


def load_publications():
    pattern = os.path.join(ROOT, "centralizator", "v*", "Centralizator_*.csv")
    files = sorted(glob.glob(pattern), key=lambda p: int(re.search(r"/v(\d+)/", p).group(1)))
    if not files:
        raise SystemExit("no centralizator CSV found")
    with open(files[-1], encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle, delimiter=";")), os.path.basename(os.path.dirname(files[-1]))


def match_works(entries, pubs):
    by_title = {}
    for pub in pubs:
        by_title.setdefault(fold_title(pub.get("Titlu", "")), pub)
    matched, new = [], []
    for entry in entries:
        pub = by_title.get(fold_title(entry["title"]))
        if pub:
            matched.append({"pubId": pub.get("Nr."), "key": entry["key"], "title": entry["title"], "year": entry["year"]})
        else:
            new.append({"key": entry["key"], "title": entry["title"], "authors": entry["authors"], "year": entry["year"], "journal": entry["journal"]})
    return matched, new


def main():
    if not os.path.exists(BIB_PATH):
        print("no BibTeX export found at %s; writing empty report" % BIB_PATH, file=sys.stderr)
        report = {"entries": 0, "matched": [], "newCandidates": []}
    else:
        with open(BIB_PATH, encoding="utf-8") as handle:
            entries = parse_bibtex(handle.read())
        pubs, version = load_publications()
        matched, new = match_works(entries, pubs)
        report = {
            "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "source": "citari/google_scholar_export.bib",
            "centralizatorVersion": version,
            "entries": len(entries),
            "matched": matched,
            "newCandidates": new,
        }
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=1)
    print("scholar bibtex: %d entries, %d matched, %d new candidates" % (
        report["entries"], len(report["matched"]), len(report["newCandidates"])))


if __name__ == "__main__":
    main()
