"""Static guard: dashboard/app.js must only call $(...) with bare element ids.

The $ helper is document.getElementById, so selector-style arguments like
$("#pubBody") return null and crash rendering (bug from commit abe1831).
Also checks that every $(id) referenced exists in index.html.

Run:  python3 -m unittest discover -s tests -v
"""

import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_JS = (ROOT / "dashboard" / "app.js").read_text(encoding="utf-8")
INDEX_HTML = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")


class TestDollarHelperUsage(unittest.TestCase):
    def test_no_selector_style_arguments(self):
        bad = re.findall(r'\$\("#[^"]*"\)', APP_JS)
        self.assertEqual(bad, [], f"selector-style $(...) calls return null: {bad}")

    def test_all_referenced_ids_exist_in_html(self):
        html_ids = set(re.findall(r'id="([^"]+)"', INDEX_HTML))
        used = set(re.findall(r'\$\("([A-Za-z][\w-]*)"\)', APP_JS))
        used |= set(re.findall(r'getElementById\("([\w-]+)"\)', APP_JS))
        missing = sorted(u for u in used if u not in html_ids)
        self.assertEqual(missing, [], f"ids used in JS but missing in HTML: {missing}")


if __name__ == "__main__":
    unittest.main()
