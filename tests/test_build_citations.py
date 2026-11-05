"""Unit tests for scripts/build_citations.py (pure functions only).

Run:  python3 -m unittest discover -s tests -v
"""

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "build_citations", ROOT / "scripts" / "build_citations.py"
)
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)


class TestTextHelpers(unittest.TestCase):
    def test_norm_title_folds_and_strips_punctuation(self):
        # raw "&" is a separator; only the "&amp;" entity becomes "and"
        self.assertEqual(bc.norm_title("Știință & Tehnologie: 2024!"), "stiinta tehnologie 2024")
        self.assertEqual(bc.norm_title("Rock &amp; Roll"), "rock and roll")
        self.assertEqual(bc.norm_title(""), "")
        self.assertEqual(bc.norm_title(None), "")

    def test_surname(self):
        self.assertEqual(bc.surname("Stamatie, Gabriela Daniela"), "stamatie")
        self.assertEqual(bc.surname("Ana Popescu"), "popescu")
        self.assertEqual(bc.surname(""), "")

    def test_clean_unescapes_entities(self):
        self.assertEqual(bc.clean("A &amp; B &lt;x&gt;"), "A & B <x>")

    def test_doi_of_strips_prefix_and_lowercases(self):
        self.assertEqual(bc.doi_of("https://doi.org/10.1234/ABC"), "10.1234/abc")
        self.assertEqual(bc.doi_of("http://dx.doi.org/10.1234/ABC"), "10.1234/abc")
        self.assertEqual(bc.doi_of("10.1234/ABC"), "10.1234/abc")
        self.assertEqual(bc.doi_of(""), "")


def work(**kw):
    base = {
        "pub_ids": [1],
        "title": "Some Title",
        "year": 2024,
        "authors": ["Ana Popescu"],
        "venue": "Journal",
        "doi": "",
        "type": "Articol",
        "openalex": None,
        "s2": None,
        "sources": {"OpenAlex"},
    }
    base.update(kw)
    return base


class TestIdentityAndSelf(unittest.TestCase):
    def test_key_of_prefers_doi(self):
        w = work(doi="10.1/abc", title="Altceva", authors=[])
        self.assertEqual(bc.key_of(w), "doi:10.1/abc")

    def test_key_of_falls_back_to_title_year_surname(self):
        w = work(title="Some Title!", year=2024, authors=["Ana Popescu"], doi="")
        self.assertEqual(bc.key_of(w), "tt:some title|2024|popescu")

    def test_is_self_matches_author_names(self):
        self.assertTrue(bc.is_self(work(authors=["Gabriela Daniela Stamatie"])))
        self.assertTrue(bc.is_self(work(authors=["A. Criveanu"])))
        self.assertFalse(bc.is_self(work(authors=["Ana Popescu"])))


class TestSourceAdapters(unittest.TestCase):
    def test_oa_work_maps_openalex_record(self):
        rec = {
            "title": "Deep &amp; Learning",
            "publication_year": 2023,
            "authorships": [{"author": {"display_name": "Ana Popescu"}}],
            "primary_location": {"source": {"display_name": "Nature"}},
            "doi": "https://doi.org/10.9/XYZ",
            "type": "article",
            "id": "https://openalex.org/W1",
        }
        w = bc.oa_work(rec, 7)
        self.assertEqual(w["pub_ids"], [7])
        self.assertEqual(w["title"], "Deep & Learning")
        self.assertEqual(w["year"], 2023)
        self.assertEqual(w["authors"], ["Ana Popescu"])
        self.assertEqual(w["venue"], "Nature")
        self.assertEqual(w["doi"], "10.9/xyz")
        self.assertEqual(w["type"], "Articol")
        self.assertEqual(w["sources"], {"OpenAlex"})

    def test_oa_work_unknown_type_is_alt_tip(self):
        w = bc.oa_work({"type": "dataset", "title": "T"}, 1)
        self.assertEqual(w["type"], "Set de date")
        w2 = bc.oa_work({"type": "ciudat", "title": "T"}, 1)
        self.assertEqual(w2["type"], "Alt tip")

    def test_s2_work_maps_semantic_scholar_record(self):
        item = {
            "citingPaper": {
                "title": "Citing Work",
                "year": 2022,
                "authors": [{"name": "Bob Ionescu"}],
                "journal": {"name": "Science"},
                "externalIds": {"DOI": "10.5/QWE"},
                "publicationTypes": ["JournalArticle"],
                "paperId": "abc123",
            }
        }
        w = bc.s2_work(item, 3)
        self.assertEqual(w["pub_ids"], [3])
        self.assertEqual(w["doi"], "10.5/qwe")
        self.assertEqual(w["type"], "Articol")
        self.assertEqual(w["venue"], "Science")
        self.assertEqual(w["s2"], "abc123")
        self.assertEqual(w["sources"], {"Semantic Scholar"})

    def test_s2_work_without_types(self):
        w = bc.s2_work({"citingPaper": {"title": "T"}}, 1)
        self.assertEqual(w["type"], "Alt tip")
        self.assertEqual(w["authors"], [])

    def test_v3_work_parses_legacy_row(self):
        row = {
            "Articol (ID)": "1, 2",
            "Lucrare citată": "Legacy &amp; Work",
            "An citare": "2020",
            "Autori citatori": "Ana Popescu; Bob Ionescu",
            "Revistă / Eveniment": "Old Journal",
            "DOI citare": "https://doi.org/10.2/LEG",
            "Tip citare": "Articol",
            "Sursă verificare": "Semantic Scholar",
        }
        w = bc.v3_work(row)
        self.assertEqual(w["pub_ids"], ["1", "2"])
        self.assertEqual(w["year"], 2020)
        self.assertEqual(w["authors"], ["Ana Popescu", "Bob Ionescu"])
        self.assertEqual(w["doi"], "10.2/leg")
        self.assertEqual(w["sources"], {"Semantic Scholar"})
        self.assertEqual(w["retained_from"], "v3")


class TestInitPaths(unittest.TestCase):
    def tearDown(self):
        bc.init_paths("v3", "v4")  # restore module defaults

    def test_adds_missing_v_prefix(self):
        bc.init_paths("3", "4")
        self.assertTrue(bc.V3_CITARI.endswith("citari/v3/Citari_Articole_Gabriela_Daniela_Stamatie_v3.csv"))
        self.assertTrue(bc.OUT_CEN.endswith("centralizator/v4"))

    def test_keeps_existing_prefix(self):
        bc.init_paths("v4", "v5")
        self.assertTrue(bc.V3_CITARI.endswith("citari/v4/Citari_Articole_Gabriela_Daniela_Stamatie_v4.csv"))
        self.assertTrue(bc.OUT_CIT.endswith("citari/v5"))
        self.assertTrue(bc.RAW.endswith("citari/v5/raw"))


if __name__ == "__main__":
    unittest.main()


class TestResearchGateDoi(unittest.TestCase):
    def test_is_researchgate_doi(self):
        self.assertTrue(bc.is_researchgate_doi("10.13140/rg.2.2.29075.86568"))
        self.assertTrue(bc.is_researchgate_doi("https://doi.org/10.13140/RG.2.2.29075.86568"))
        self.assertTrue(bc.is_researchgate_doi("http://dx.doi.org/10.13140/rg.2.2.29075.86568"))
        self.assertFalse(bc.is_researchgate_doi("10.3390/foods11223667"))
        self.assertFalse(bc.is_researchgate_doi(""))


class TestScholarCountsLoader(unittest.TestCase):
    def test_real_template_parses(self):
        counts = bc.load_scholar_counts()
        self.assertIsInstance(counts, dict)
        # template ships empty, so no counts yet
        self.assertEqual(counts, {})


class TestFatcatAdapter(unittest.TestCase):
    def payload(self):
        return {
            "release": {"id": "rel1", "title": "Citing Work", "year": 2023, "doi": "10.1/abc"},
            "citations": [
                {"citing_release": {
                    "title": "Another Citing Work",
                    "year": 2024,
                    "doi": "https://doi.org/10.2/XYZ",
                    "container_name": "Nature",
                    "type": "article-journal",
                    "authors": [{"given_name": "Ana", "surname": "Popescu"}, {"given_name": "Bob", "surname": "Ionescu"}],
                }},
                {"garbage": True},
                "not-a-dict",
            ],
        }

    def test_extracts_citations_list(self):
        self.assertEqual(len(bc.fatcat_citations(self.payload())), 3)
        self.assertEqual(bc.fatcat_citations(None), [])
        self.assertEqual(bc.fatcat_citations({"citations": None}), [])

    def test_maps_release_to_work_shape(self):
        work = bc.fatcat_work(self.payload()["citations"][0], 7)
        self.assertEqual(work["pub_ids"], [7])
        self.assertEqual(work["title"], "Another Citing Work")
        self.assertEqual(work["authors"], ["Ana Popescu", "Bob Ionescu"])
        self.assertEqual(work["venue"], "Nature")
        self.assertEqual(work["doi"], "10.2/xyz")
        self.assertEqual(work["sources"], {"Fatcat"})

    def test_rejects_malformed_items(self):
        self.assertIsNone(bc.fatcat_work({"garbage": True}, 1))
        self.assertIsNone(bc.fatcat_work("not-a-dict", 1))
        self.assertIsNone(bc.fatcat_work(None, 1))


class TestFindVersionedCsv(unittest.TestCase):
    def test_prefers_exact_version_name(self):
        self.assertTrue(bc._find_versioned_csv(
            str(ROOT / "citari" / "v4"),
            "Citari_Articole_Gabriela_Daniela_Stamatie",
            "v4",
        ).endswith("Citari_Articole_Gabriela_Daniela_Stamatie_v4.csv"))

    def test_falls_back_to_glob_when_suffix_mismatches(self):
        # centralizator/v5 holds a _v4-named file (build hardcodes the suffix)
        found = bc._find_versioned_csv(
            str(ROOT / "centralizator" / "v5"),
            "Centralizator_Articole_Gabriela_Daniela_Stamatie",
            "v5",
        )
        self.assertTrue(found.endswith("Centralizator_Articole_Gabriela_Daniela_Stamatie_v4.csv"))

    def test_missing_folder_returns_exact_path(self):
        self.assertTrue(bc._find_versioned_csv(
            str(ROOT / "centralizator" / "v99"),
            "Centralizator_Articole_Gabriela_Daniela_Stamatie",
            "v99",
        ).endswith("Centralizator_Articole_Gabriela_Daniela_Stamatie_v99.csv"))
