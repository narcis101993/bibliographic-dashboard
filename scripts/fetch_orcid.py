#!/usr/bin/env python3
"""Fetch the author's works from the ORCID public API (no key required).

ORCID's public API exposes the works recorded on the researcher's ORCID
profile. We store the raw response once per refresh and match DOIs against
the centralizator during the build. Best-effort: any failure is recorded
and never breaks the refresh.
"""

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "fetch_citation_sources", os.path.join(HERE, "fetch_citation_sources.py")
)
fcs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fcs)

AUTHOR_ORCID = "0000-0002-1850-7278"


def works_dois(payload):
    """Extract the set of normalised DOIs from an ORCID works payload."""
    dois = set()
    if not isinstance(payload, dict):
        return dois
    for group in payload.get("group") or []:
        for summary in group.get("work-summary") or []:
            external = (summary.get("external-ids") or {}).get("external-id") or []
            for item in external:
                if str(item.get("external-id-type", "")).lower() == "doi":
                    value = fcs_DOI(item.get("external-id-value"))
                    if value:
                        dois.add(value)
    return dois


def fcs_DOI(value):
    text = (value or "").strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-version", default=None)
    ap.add_argument("--target-version", default=None)
    args = ap.parse_args()
    fcs.init_paths(args.source_version, args.target_version)
    os.makedirs(os.path.join(fcs.RAW, "orcid"), exist_ok=True)
    try:
        payload = fcs.fetch("https://pub.orcid.org/v3.0/%s/works" % AUTHOR_ORCID)
        fcs.write_raw("orcid", "author", payload)
        print(json.dumps({"orcidWorks": len(works_dois(payload))}, ensure_ascii=False), flush=True)
    except Exception as e:
        print("orcid error: %s: %s" % (type(e).__name__, e), file=sys.stderr)
        try:
            fcs.write_raw("orcid", "author", None)
        except Exception:
            pass


if __name__ == "__main__":
    main()
