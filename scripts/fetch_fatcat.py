#!/usr/bin/env python3
"""Fetch citing works from Fatcat (scholar.archive.org's public API).

Fatcat is the open, API-accessible counterpart of Google Scholar's index.
Best-effort by design: Fatcat may be slow or unreachable, so every failure
is recorded in the retrieval summary and never breaks the refresh.

Raw responses are stored verbatim under citari/vN/raw/fatcat_citing/<id>.json
with shape {"release": {...}, "citations": [...] | null}; build_citations.py
merges recognised citing releases with the same DOI/title identity keys as
the other sources, so duplicates across sources are not created.
"""

import argparse
import importlib.util
import json
import os
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "fetch_citation_sources", os.path.join(HERE, "fetch_citation_sources.py")
)
fcs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fcs)

API = "https://api.fatcat.wiki/v0"


def fatcat_lookup(doi):
    return fcs.fetch("%s/release/lookup?doi=%s&expand=files,webcaptures" % (API, urllib.parse.quote(doi)))


def fatcat_citations(release_id):
    try:
        return fcs.fetch("%s/release/%s/citations" % (API, urllib.parse.quote(str(release_id))))
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma separated publication ids")
    ap.add_argument("--source-version", default=None)
    ap.add_argument("--target-version", default=None)
    args = ap.parse_args()
    fcs.init_paths(args.source_version, args.target_version)
    only = {x.strip() for x in args.only.split(",") if x.strip()}
    pubs = [p for p in fcs.load_publications() if not only or p["Nr."] in only]
    summary = []
    for pub in pubs:
        pid = pub["Nr."]
        doi = (pub.get("DOI") or "").strip()
        row = {"publicationId": pid, "doi": doi}
        if not doi:
            fcs.write_raw("fatcat_citing", pid, None)
            row["fatcatCiting"] = 0
            summary.append(row)
            continue
        try:
            release = fatcat_lookup(doi)
            citations = None
            if release and release.get("id"):
                citations = fatcat_citations(release["id"])
            fcs.write_raw("fatcat_citing", pid, {"release": release, "citations": citations})
            row["fatcatCiting"] = len(citations) if isinstance(citations, list) else 0
        except Exception as e:
            row["fatcatError"] = "%s: %s" % (type(e).__name__, e)
            try:
                fcs.write_raw("fatcat_citing", pid, None)
            except Exception:
                pass
        summary.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
