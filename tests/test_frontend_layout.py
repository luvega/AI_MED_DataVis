from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = REPO_ROOT / "docs" / "stylesheets" / "extra.css"
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
DOCS_ROOT = REPO_ROOT / "docs"


class FrontendLayoutTests(unittest.TestCase):
    def test_desktop_layout_uses_primary_navigation_and_content_only(self) -> None:
        css = CSS_PATH.read_text(encoding="utf-8")
        desktop = css.split("@media screen and (min-width: 76.25em)", 1)[1]
        self.assertIn(".md-sidebar--secondary", desktop)
        self.assertIn("display: none", desktop)
        self.assertIn(".md-sidebar--primary", desktop)
        self.assertIn(".md-content", desktop)

    def test_reading_layout_is_wide_but_bounded(self) -> None:
        css = CSS_PATH.read_text(encoding="utf-8")
        self.assertIn("max-width: min(94vw, 1500px)", css)
        self.assertIn("max-width: 62rem", css)
        self.assertIn("@media screen and (max-width: 44.984375em)", css)

    def test_theme_uses_one_teal_accent_family(self) -> None:
        config = yaml.load(
            MKDOCS_PATH.read_text(encoding="utf-8"),
            Loader=yaml.FullLoader,
        )
        palettes = config["theme"]["palette"]
        self.assertTrue(all(palette["primary"] == "teal" for palette in palettes))
        self.assertTrue(all(palette["accent"] == "teal" for palette in palettes))

    def test_public_markdown_contains_no_em_dash_characters(self) -> None:
        offenders = []
        for path in DOCS_ROOT.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            if "—" in text or "–" in text:
                offenders.append(path.relative_to(REPO_ROOT).as_posix())
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
