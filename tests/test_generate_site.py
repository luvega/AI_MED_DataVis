from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import generate_site


class CopyChaptersTests(unittest.TestCase):
    def test_copies_external_local_images_into_chapter_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_root = root / "book"
            chapter_dir = source_root / "chapters" / "chapter-10"
            artifact = source_root / "outputs" / "run" / "figure.png"
            docs_root = root / "site" / "docs"

            chapter_dir.mkdir(parents=True)
            artifact.parent.mkdir(parents=True)
            artifact.write_bytes(b"figure-bytes")
            (chapter_dir / "正文.md").write_text(
                "# 第10章 测试\n\n![结果图](../../outputs/run/figure.png)\n",
                encoding="utf-8",
            )

            with (
                patch.object(generate_site, "SOURCE_ROOT", source_root),
                patch.object(generate_site, "DOCS_ROOT", docs_root),
                patch.object(generate_site, "CHAPTER_TITLES", {10: "测试"}),
            ):
                generate_site.copy_chapters()

            generated = docs_root / "chapters" / "chapter-10"
            content = (generated / "index.md").read_text(encoding="utf-8")
            self.assertIn("![结果图](assets/figure.png)", content)
            self.assertEqual(
                (generated / "assets" / "figure.png").read_bytes(),
                b"figure-bytes",
            )

    def test_removes_directory_form_book_outline(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_root = Path(temp_dir) / "docs"
            outline_page = docs_root / "book-outline" / "index.md"
            outline_page.parent.mkdir(parents=True)
            outline_page.write_text("# 不应发布的全书大纲\n", encoding="utf-8")

            with patch.object(generate_site, "DOCS_ROOT", docs_root):
                generate_site.remove_generated_dirs()

            self.assertFalse(outline_page.parent.exists())

    def test_removes_directory_form_chapter_outline(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_root = Path(temp_dir) / "docs"
            outline_page = docs_root / "chapters" / "chapter-1" / "outline" / "index.md"
            outline_page.parent.mkdir(parents=True)
            outline_page.write_text("# 不应发布的章节大纲\n", encoding="utf-8")

            with patch.object(generate_site, "DOCS_ROOT", docs_root):
                generate_site.remove_generated_dirs()

            self.assertFalse(outline_page.parent.exists())

if __name__ == "__main__":
    unittest.main()
