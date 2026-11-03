#!/usr/bin/env python3
"""Record the public Crossref is-referenced-by-count for every publication that
has a DOI.

Crossref's Cited-by *list* endpoint needs depositor credentials, so the citing
works themselves cannot be retrieved from Crossref without paid/member access.
The public count is still useful as an independent cross-check of the
OpenAlex/Semantic Scholar totals and is stored verbatim.
"""

import csv
import json
import os
import time
import argparse
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENTRALIZATOR = os.path.join(
    ROOT, "centralizator", "v3", "Centralizator_Articole_Gabriela_Daniela_Stamatie_v3.csv"
)
OUT = os.path.join(ROOT, "citari", "v4", "raw", "crossref_counts.json")
UA = "Reasercher-List/1.0 (mailto:researcher@example.org)"
RETRIEVAL_DATE = "2026-11-01"


def init_paths(source_version=None, target_version=None):
    global CENTRALIZATOR, OUT
    source_version = source_version or "v3"
    target_version = target_version or "v4"
    if not source_version.startswith("v"):
        source_version = "v" + source_version
    if not target_version.startswith("v"):
        target_version = "v" + target_version
    CENTRALIZATOR = os.path.join(
        ROOT, "centralizator", source_version,
        "Centralizator_Articole_Gabriela_Daniela_Stamatie_%s.csv" % source_version
    )
    OUT = os.path.join(ROOT, "citari", target_version, "raw", "crossref_counts.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-version", default=None, help="source version (e.g. v3, v4)")
    ap.add_argument("--target-version", default=None, help="target version (e.g. v4, v5)")
    args = ap.parse_args()
    init_paths(args.source_version, args.target_version)
    with open(CENTRALIZATOR, encoding="utf-8-sig") as f:
        pubs = list(csv.DictReader(f, delimiter=";"))
    out = {"retrievedOn": RETRIEVAL_DATE, "publications": []}
    for pub in pubs:
        doi = (pub.get("DOI") or "").strip()
        row = {"publicationId": pub["Nr."], "doi": doi}
        if not doi:
            row["status"] = "no-doi"
            out["publications"].append(row)
            continue
        url = "https://api.crossref.org/works/%s" % urllib.parse.quote(doi)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                msg = json.load(r)["message"]
            row["status"] = "ok"
            row["isReferencedByCount"] = msg.get("is-referenced-by-count")
            row["crossrefTitle"] = (msg.get("title") or [None])[0]
        except urllib.error.HTTPError as e:
            row["status"] = "http-%d" % e.code
        except Exception as e:
            row["status"] = "error"
            row["error"] = "%s: %s" % (type(e).__name__, e)
        out["publications"].append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        time.sleep(0.7)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
