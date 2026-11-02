#!/usr/bin/env python3
"""Fetch citing works for every publication in centralizator/v3 from the
public sources that are reachable without paid access.

Sources:
  * OpenAlex  (works?filter=cites:W...)
  * Semantic Scholar Graph API (paper/{id}/citations)
  * DataCite   (dois/{doi}, citationCount + relationships)

Raw responses are stored verbatim under citari/v4/raw/<source>/<pub-id>.json
so that every record in the merged dataset can be traced back to a retrieval.
Nothing is synthesised: a source that returns nothing is recorded as such.

Crossref's Cited-by *list* endpoint requires depositor credentials; only the
public is-referenced-by-count is available and is fetched separately by
scripts/check_crossref_counts.py.
"""

import argparse
import csv
import json
import re
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENTRALIZATOR = os.path.join(
    ROOT, "centralizator", "v3", "Centralizator_Articole_Gabriela_Daniela_Stamatie_v3.csv"
)
RAW = os.path.join(ROOT, "citari", "v4", "raw")
UA = "Reasercher-List/1.0 (mailto:researcher@example.org)"
RETRIEVAL_DATE = "2026-11-01"


def parse_version_arg(args, flag, default):
    val = getattr(args, flag, None)
    if val:
        return val if val.startswith("v") else "v" + val
    return default

SOURCE_VERSION = "v3"
TARGET_VERSION = "v4"


def init_paths(source_version=None, target_version=None):
    global SOURCE_VERSION, TARGET_VERSION, CENTRALIZATOR, RAW
    SOURCE_VERSION = source_version or SOURCE_VERSION
    TARGET_VERSION = target_version or TARGET_VERSION
    CENTRALIZATOR = os.path.join(
        ROOT, "centralizator", SOURCE_VERSION,
        "Centralizator_Articole_Gabriela_Daniela_Stamatie%s.csv" % SOURCE_VERSION
    )
    RAW = os.path.join(ROOT, "citari", TARGET_VERSION, "raw")


def fetch(url, tries=4, pause=2.0):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 404:
                raise
            time.sleep(pause * (attempt + 1))
        except Exception as e:  # network hiccup
            last = e
            time.sleep(pause * (attempt + 1))
    raise last


def write_raw(source, pub_id, payload):
    d = os.path.join(RAW, source)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "%s.json" % pub_id), "w", encoding="utf-8") as f:
        json.dump(
            {"retrievedOn": RETRIEVAL_DATE, "publicationId": pub_id, "payload": payload},
            f,
            ensure_ascii=False,
            indent=1,
        )


def norm_title(t):
    t = (t or "").lower().replace("\u2013", "-").replace("\u2014", "-")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def load_publications():
    with open(CENTRALIZATOR, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


def openalex_resolve(pub):
    doi = (pub.get("DOI") or "").strip()
    if doi:
        try:
            rec = fetch("https://api.openalex.org/works/doi:%s" % urllib.parse.quote(doi))
            return rec
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
    title = (pub.get("Titlu") or "").strip()
    if not title:
        return None
    q = urllib.parse.quote(title)
    data = fetch(
        "https://api.openalex.org/works?search=%s&per-page=5&select=id,doi,title,publication_year,cited_by_count"
        % q
    )
    for rec in data.get("results", []):
        if norm_title(rec.get("title")) == norm_title(title):
            return rec
    return None


def openalex_citing(work_id):
    out, cursor = [], "*"
    while cursor:
        url = (
            "https://api.openalex.org/works?filter=cites:%s&per-page=200&cursor=%s"
            % (work_id.rsplit("/", 1)[-1], urllib.parse.quote(cursor))
        )
        data = fetch(url)
        out.extend(data.get("results", []))
        cursor = (data.get("meta") or {}).get("next_cursor")
        time.sleep(0.2)
    return out


def s2_paper_id(pub):
    doi = (pub.get("DOI") or "").strip()
    if doi:
        return "DOI:%s" % doi
    title = (pub.get("Titlu") or "").strip()
    if not title:
        return None
    data = fetch(
        "https://api.semanticscholar.org/graph/v1/paper/search?query=%s&fields=title,year,externalIds&limit=5"
        % urllib.parse.quote(title)
    )
    for rec in data.get("data", []):
        if norm_title(rec.get("title")) == norm_title(title):
            return rec.get("paperId")
    return None


def s2_citing(paper_id):
    out, offset, limit = [], 0, 100
    while True:
        url = (
            "https://api.semanticscholar.org/graph/v1/paper/%s/citations"
            "?fields=title,year,venue,externalIds,authors,publicationTypes,publicationDate,journal"
            "&limit=%d&offset=%d" % (urllib.parse.quote(paper_id), limit, offset)
        )
        data = fetch(url)
        batch = data.get("data", [])
        out.extend(batch)
        if len(batch) < limit:
            break
        offset += limit
        time.sleep(1.2)
    return out


def datacite_record(pub):
    doi = (pub.get("DOI") or "").strip()
    if not doi:
        return None
    try:
        return fetch("https://api.datacite.org/dois/%s" % urllib.parse.quote(doi))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma separated publication ids")
    ap.add_argument("--source-version", default=None, help="source version (e.g. v3, v4)")
    ap.add_argument("--target-version", default=None, help="target version (e.g. v4, v5)")
    args = ap.parse_args()
    init_paths(args.source_version, args.target_version)
    only = {x.strip() for x in args.only.split(",") if x.strip()}
    pubs = [p for p in load_publications() if not only or p["Nr."] in only]
    summary = []
    for pub in pubs:
        pid = pub["Nr."]
        row = {"publicationId": pid, "doi": (pub.get("DOI") or "").strip()}
        try:
            rec = openalex_resolve(pub)
            row["openalexId"] = rec.get("id") if rec else None
            if rec:
                write_raw("openalex_work", pid, rec)
                citing = openalex_citing(rec["id"])
                write_raw("openalex_citing", pid, citing)
                row["openalexCiting"] = len(citing)
            else:
                write_raw("openalex_work", pid, None)
                row["openalexCiting"] = 0
        except Exception as e:
            row["openalexError"] = "%s: %s" % (type(e).__name__, e)
        try:
            sid = s2_paper_id(pub)
            row["s2PaperId"] = sid
            if sid:
                citing = s2_citing(sid)
                write_raw("s2_citing", pid, citing)
                row["s2Citing"] = len(citing)
            else:
                write_raw("s2_citing", pid, None)
                row["s2Citing"] = 0
        except Exception as e:
            row["s2Error"] = "%s: %s" % (type(e).__name__, e)
        try:
            dc = datacite_record(pub)
            write_raw("datacite", pid, dc)
            row["dataciteCitationCount"] = (
                ((dc or {}).get("data") or {}).get("attributes", {}).get("citationCount")
            )
        except Exception as e:
            row["dataciteError"] = "%s: %s" % (type(e).__name__, e)
        summary.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        time.sleep(1.0)

    os.makedirs(RAW, exist_ok=True)
    with open(os.path.join(RAW, "retrieval-summary.json"), "w", encoding="utf-8") as f:
        json.dump(
            {"retrievedOn": RETRIEVAL_DATE, "sources": ["OpenAlex", "Semantic Scholar", "DataCite"], "publications": summary},
            f,
            ensure_ascii=False,
            indent=1,
        )
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
