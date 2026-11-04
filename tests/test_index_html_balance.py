"""Static guard: dashboard/index.html must have balanced structural tags.

A stray </div> once closed .content/main early, pushing the Citări and
Sinteză panels outside <main> where the tab CSS could not reach them.
This strict stack check (no HTML5 implied-close rules) catches that class
of mistake in CI.

Run:  python3 -m unittest discover -s tests -v
"""

import pathlib
import unittest
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOID = {"meta", "link", "input", "br", "img", "hr", "source"}


class BalanceParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: stray </{tag}> (stack empty)")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        names = [t for t, _ in self.stack]
        if tag in names:
            idx = len(names) - 1 - names[::-1].index(tag)
            unclosed = [f"{t}@{l}" for t, l in self.stack[idx + 1:]]
            self.errors.append(
                f"line {self.getpos()[0]}: </{tag}> closes over unclosed {unclosed}"
            )
            del self.stack[idx:]
        else:
            self.errors.append(f"line {self.getpos()[0]}: stray </{tag}>")


class TestHtmlBalance(unittest.TestCase):
    def test_index_html_tags_are_balanced(self):
        html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")
        parser = BalanceParser()
        parser.feed(html)
        self.assertEqual(parser.errors, [], "tag imbalance: " + "; ".join(parser.errors))
        self.assertEqual(parser.stack, [], f"unclosed at EOF: {parser.stack}")

    def test_panels_live_inside_main(self):
        html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")
        main_start = html.index("<main>")
        panels = [
            html.index('panel panel-publicatii'),
            html.index('panel panel-citari'),
            html.index('panel panel-sinteza'),
        ]
        main_end = html.index("</main>")
        for pos in panels:
            self.assertTrue(main_start < pos < main_end, "panel outside <main>")


if __name__ == "__main__":
    unittest.main()
