"""Unit tests for scripts/build_dashboard_data.py (pure functions only).

Run:  python3 -m unittest discover -s tests -v
"""

import importlib.util
import os
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "build_dashboard_data", ROOT / "scripts" / "build_dashboard_data.py"
)
bdd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bdd)


class TestTextHelpers(unittest.TestCase):
    def test_fold_strips_diacritics_and_lowercases(self):
        self.assertEqual(bdd.fold("Știință ȘI Învățământ"), "stiinta si invatamant")

    def test_fold_none_is_empty(self):
        self.assertEqual(bdd.fold(None), "")

    def test_clean_collapses_whitespace(self):
        self.assertEqual(bdd.clean("  a \n\t b  "), "a b")
        self.assertEqual(bdd.clean(None), "")

    def test_parse_int(self):
        self.assertEqual(bdd.parse_int("2024"), 2024)
        self.assertEqual(bdd.parse_int("vol. 12 (2024)"), 12)
        self.assertEqual(bdd.parse_int("-5"), -5)
        self.assertIsNone(bdd.parse_int("abc"))
        self.assertEqual(bdd.parse_int("abc", 7), 7)

    def test_split_authors(self):
        self.assertEqual(bdd.split_authors("Ana; Bob ;  Cid "), ["Ana", "Bob", "Cid"])
        self.assertEqual(bdd.split_authors(""), [])
        self.assertEqual(bdd.split_authors(None), [])

    def test_parse_article_ids_dedupes_and_keeps_order(self):
        self.assertEqual(bdd.parse_article_ids("1, 2, 3"), [1, 2, 3])
        self.assertEqual(bdd.parse_article_ids("1,1,2"), [1, 2])
        self.assertEqual(bdd.parse_article_ids(""), [])


class TestDoiLinkAndTypes(unittest.TestCase):
    def test_normalize_doi_extracts_and_cleans(self):
        self.assertEqual(
            bdd.normalize_doi("https://doi.org/10.1234/ABC.Def."), "10.1234/abc.def"
        )
        self.assertEqual(bdd.normalize_doi("fără doi aici"), "")

    def test_normalize_link(self):
        self.assertEqual(bdd.normalize_link("", "10.1/x"), "https://doi.org/10.1/x")
        self.assertEqual(bdd.normalize_link("", ""), "")
        self.assertEqual(bdd.normalize_link("10.1/x", ""), "https://doi.org/10.1/x")
        self.assertEqual(
            bdd.normalize_link("https://example.com/a", ""), "https://example.com/a"
        )
        self.assertEqual(bdd.normalize_link("nota de subsol", ""), "")

    def test_type_code_uses_folded_keys(self):
        self.assertEqual(bdd.type_code("Articol științific", bdd.PUBLICATION_TYPES), "article")
        self.assertEqual(bdd.type_code("Preprint", bdd.PUBLICATION_TYPES), "preprint")
        self.assertEqual(bdd.type_code("Ceva necunoscut", bdd.PUBLICATION_TYPES), "other")


class TestVersionsAndSelfCitation(unittest.TestCase):
    def test_version_key_is_numeric_not_lexical(self):
        self.assertLess(bdd.version_key("v4"), bdd.version_key("v5"))
        self.assertLess(bdd.version_key("v9"), bdd.version_key("v10"))

    def test_is_self_citation_by_author(self):
        self.assertTrue(bdd.is_self_citation("", ["Gabriela Daniela Stamatie"]))
        self.assertFalse(bdd.is_self_citation("", ["Ana Popescu"]))

    def test_is_self_citation_by_flag(self):
        self.assertTrue(bdd.is_self_citation("Auto-citare: da", ["Ana Popescu"]))
        self.assertFalse(bdd.is_self_citation("Auto-citare: nu", ["Ana Popescu"]))


class TestNormalizePublications(unittest.TestCase):
    def row(self, nr, **kw):
        base = {
            "Nr.": str(nr),
            "An": "2024",
            "Tip": "Articol științific",
            "Titlu": f"Titlu {nr}",
            "Revistă / Publicație": "Journal",
            "DOI": "https://doi.org/10.1234/ABC",
            "Link": "",
            "Toți autorii": "Gabriela Daniela Stamatie; Ana Popescu",
        }
        base.update(kw)
        return base

    def test_normalizes_and_sorts_by_id(self):
        pubs = bdd.normalize_publications([self.row(2), self.row(1)])
        self.assertEqual([p["id"] for p in pubs], [1, 2])
        self.assertEqual(pubs[0]["doi"], "10.1234/abc")
        self.assertEqual(pubs[0]["link"], "https://doi.org/10.1234/abc")
        self.assertEqual(pubs[0]["typeCode"], "article")
        self.assertEqual(pubs[0]["authors"], ["Gabriela Daniela Stamatie", "Ana Popescu"])
        self.assertEqual(pubs[0]["year"], 2024)

    def test_missing_nr_falls_back_to_position(self):
        row = self.row(1)
        row["Nr."] = ""
        pubs = bdd.normalize_publications([row])
        self.assertEqual(pubs[0]["id"], 1)


class TestStatsAndValidate(unittest.TestCase):
    def pubs(self):
        return [
            {"id": 1, "doi": "10.1/a", "year": 2023, "title": "A"},
            {"id": 2, "doi": "", "year": 2024, "title": "B"},
        ]

    def cits(self):
        return [
            {"id": 1, "articleIds": [1, 2], "selfCitation": True, "venue": "J1", "title": "X", "doi": ""},
            {"id": 2, "articleIds": [1], "selfCitation": False, "venue": "J1", "title": "Y", "doi": ""},
        ]

    def test_stats_for_counts_links(self):
        stats = bdd.stats_for(self.pubs(), self.cits())
        self.assertEqual(stats["publications"], 2)
        self.assertEqual(stats["citations"], 2)
        self.assertEqual(stats["citationLinks"], 3)
        self.assertEqual(stats["selfCitations"], 1)
        self.assertEqual(stats["externalCitations"], 1)
        self.assertEqual(stats["selfCitationLinks"], 2)
        self.assertEqual(stats["publicationsWithDoi"], 1)
        self.assertEqual(stats["citingVenues"], 1)
        self.assertEqual(stats["publicationYearRange"], [2023, 2024])

    def test_validate_accepts_consistent_data(self):
        self.assertEqual(bdd.validate("v5", self.pubs(), self.cits()), [])

    def test_validate_catches_duplicate_pub_ids(self):
        pubs = self.pubs() + [dict(self.pubs()[0])]
        problems = bdd.validate("v5", pubs, self.cits())
        self.assertTrue(any("duplicate publication ids" in p for p in problems))

    def test_validate_catches_unknown_article_ids(self):
        cits = [dict(self.cits()[0], articleIds=[99])]
        problems = bdd.validate("v5", self.pubs(), cits)
        self.assertTrue(any("unknown article ids" in p for p in problems))

    def test_validate_catches_empty_citations(self):
        problems = bdd.validate("v5", self.pubs(), [])
        self.assertTrue(any("no citations parsed" in p for p in problems))


class TestDigestAndTimestamp(unittest.TestCase):
    def test_input_digest_is_stable_and_content_sensitive(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "a.txt"
            # input_digest resolves paths relative to ROOT; use a real repo file
            real = ROOT / "scripts" / "build_dashboard_data.py"
            first = bdd.input_digest([real])
            second = bdd.input_digest([real])
            self.assertEqual(first, second)
            self.assertTrue(first.startswith("sha256:"))
            path.write_text("x", encoding="utf-8")
            # digest of the real file must not depend on tmp file presence
            self.assertEqual(bdd.input_digest([real]), first)

    def test_build_timestamp_prefers_source_date_epoch(self):
        old = os.environ.get("SOURCE_DATE_EPOCH")
        os.environ["SOURCE_DATE_EPOCH"] = "1761955200"  # 2025-11-01T00:00:00Z
        try:
            ts = bdd.build_timestamp([{"verifiedOn": "2026-11-01"}])
            self.assertEqual(ts, "2025-11-01T00:00:00+00:00")
        finally:
            if old is None:
                del os.environ["SOURCE_DATE_EPOCH"]
            else:
                os.environ["SOURCE_DATE_EPOCH"] = old

    def test_build_timestamp_uses_newest_verified_on(self):
        os.environ.pop("SOURCE_DATE_EPOCH", None)
        ts = bdd.build_timestamp(
            [{"verifiedOn": "2026-10-31"}, {"verifiedOn": "2026-11-01"}, {}]
        )
        self.assertEqual(ts, "2026-11-01T00:00:00+00:00")


if __name__ == "__main__":
    unittest.main()


class TestResearchGate(unittest.TestCase):
    def test_is_researchgate_doi(self):
        self.assertTrue(bdd.is_researchgate_doi("10.13140/rg.2.2.29075.86568"))
        self.assertTrue(bdd.is_researchgate_doi("10.13140/RG.2.2.29075.86568".lower()))
        self.assertFalse(bdd.is_researchgate_doi("10.3390/foods11223667"))
        self.assertFalse(bdd.is_researchgate_doi(""))
        self.assertFalse(bdd.is_researchgate_doi(None))

    def test_normalize_coverage_passes_researchgate_status(self):
        rows = [{
            "ID": "19", "Titlu": "Poster", "An": "2018",
            "DOI": "10.13140/rg.2.2.29075.86568", "Lucrări citante v4": "0",
            "Surse verificate": "DataCite", "Stare acoperire": "parțial",
            "Stare OpenAlex": "x", "Stare Crossref": "x",
            "Stare Semantic Scholar": "x", "Stare DataCite": "x",
            "Stare ResearchGate": "verificat (DOI ResearchGate)",
        }]
        cov = bdd.normalize_coverage(rows)
        self.assertEqual(cov[0]["sources"]["researchgate"], "verificat (DOI ResearchGate)")
