#!/usr/bin/env python3
"""Fetch Europe PMC citation counts per publication (public API, no key).

Europe PMC indexes biomedical and agricultural literature and reports an
independent cited-by count per DOI. Best-effort: failures are recorded per
publication and never break the refresh.
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


def europepmc_record(doi):
    query = urllib.parse.quote('DOI:"%s"' % doi)
    url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
           "?query=%s&format=json&resultType=core&pageSize=1" % query)
    payload = fcs.fetch(url)
    results = ((payload or {}).get("resultList") or {}).get("result") or []
    if not results:
        return None
    first = results[0]
    return {
        "citedByCount": first.get("citedByCount"),
        "pmcid": first.get("pmcid"),
        "id": first.get("id"),
        "title": first.get("title"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--source-version", default=None)
    ap.add_argument("--target-version", default=None)
    args = ap.parse_args()
    fcs.init_paths(args.source_version, args.target_version)
    only = {x.strip() for x in args.only.split(",") if x.strip()}
    pubs = [p for p in fcs.load_publications() if not only or p["Nr."] in only]
    for pub in pubs:
        pid = pub["Nr."]
        doi = (pub.get("DOI") or "").strip()
        row = {"publicationId": pid, "doi": doi}
        if not doi:
            fcs.write_raw("europepmc", pid, None)
            print(json.dumps(row, ensure_ascii=False), flush=True)
            continue
        try:
            record = europepmc_record(doi)
            fcs.write_raw("europepmc", pid, record)
            row["citedByCount"] = (record or {}).get("citedByCount")
        except Exception as e:
            row["europepmcError"] = "%s: %s" % (type(e).__name__, e)
            try:
                fcs.write_raw("europepmc", pid, None)
            except Exception:
                pass
        print(json.dumps(row, ensure_ascii=False), flush=True)
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
