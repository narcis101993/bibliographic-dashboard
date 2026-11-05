"""Unit tests for scripts/import_scholar_bibtex.py (pure functions only).

Run:  python3 -m unittest discover -s tests -v
"""

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "import_scholar_bibtex", ROOT / "scripts" / "import_scholar_bibtex.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


SAMPLE = """@article{belc2021type,
  title={Type and amount of legume protein concentrate influencing the technological, nutritional, and sensorial properties of wheat bread},
  author={Belc, Nastasia and Duta, Denisa Eglantina and Stamatie, Gabriela Daniela},
  journal={Applied Sciences},
  volume={11},
  year={2021}
}

@article{stamatie2021nutritional,
  title={Nutritional and functional properties of some protein sources},
  author={Stamatie, Gabriela Daniela and Duț{\\u{a}}, Denisa Eglantina and others},
  journal={AgroLife Scientific Journal},
  year={2021}
}

@article{new2024work,
  title={A brand new study not yet in the central index},
  author={Stamatie, Gabriela Daniela},
  year={2024}
}
"""


class TestParseBibtex(unittest.TestCase):
    def test_parses_entries_with_brace_safe_values(self):
        entries = mod.parse_bibtex(SAMPLE)
        self.assertEqual(len(entries), 3)
        first = entries[0]
        self.assertEqual(first["key"], "belc2021type")
        self.assertEqual(first["year"], 2021)
        self.assertEqual(first["journal"], "Applied Sciences")
        self.assertEqual(len(first["authors"]), 3)

    def test_decodes_latex_diacritics_and_drops_others(self):
        entries = mod.parse_bibtex(SAMPLE)
        second = entries[1]
        self.assertIn("Duță", second["authors"][1])
        self.assertNotIn("others", [a.lower() for a in second["authors"]])

    def test_fold_title_normalizes(self):
        self.assertEqual(
            mod.fold_title("Type and Amount of Legume Protein Concentrate!"),
            "type and amount of legume protein concentrate",
        )


class TestMatchWorks(unittest.TestCase):
    def test_matches_by_normalized_title_and_isolates_new(self):
        entries = mod.parse_bibtex(SAMPLE)
        pubs = [
            {"Nr.": "4", "Titlu": "Type and Amount of Legume Protein Concentrate Influencing the Technological, Nutritional, and Sensorial Properties of Wheat Bread"},
            {"Nr.": "2", "Titlu": "Nutritional and functional properties of some protein sources"},
        ]
        matched, new = mod.match_works(entries, pubs)
        self.assertEqual(len(matched), 2)
        self.assertEqual({m["pubId"] for m in matched}, {"4", "2"})
        self.assertEqual(len(new), 1)
        self.assertEqual(new[0]["key"], "new2024work")
        self.assertEqual(new[0]["year"], 2024)


if __name__ == "__main__":
    unittest.main()
