from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import validate_site_sources


class OutlineValidationTests(unittest.TestCase):
    def test_rejects_directory_form_book_outline(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_root = repo_root / "docs"
            outline_page = docs_root / "book-outline" / "index.md"
            outline_page.parent.mkdir(parents=True)
            outline_page.write_text("# 不应发布的全书大纲\n", encoding="utf-8")
            (docs_root / "index.md").write_text("# 首页\n", encoding="utf-8")

            with (
                patch.object(validate_site_sources, "REPO_ROOT", repo_root),
                patch.object(validate_site_sources, "DOCS_ROOT", docs_root),
            ):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        validate_site_sources.validate_no_outline_pages()

    def test_rejects_directory_form_chapter_outline(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_root = repo_root / "docs"
            outline_page = docs_root / "chapters" / "chapter-1" / "outline" / "index.md"
            outline_page.parent.mkdir(parents=True)
            outline_page.write_text("# 不应发布的章节大纲\n", encoding="utf-8")
            (docs_root / "index.md").write_text("# 首页\n", encoding="utf-8")

            with (
                patch.object(validate_site_sources, "REPO_ROOT", repo_root),
                patch.object(validate_site_sources, "DOCS_ROOT", docs_root),
            ):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        validate_site_sources.validate_no_outline_pages()

    def test_rejects_private_address_in_public_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_root = repo_root / "docs"
            docs_root.mkdir(parents=True)
            (docs_root / "index.md").write_text(
                "# 首页\n\n内部服务为 192.168.1.23。\n",
                encoding="utf-8",
            )

            with (
                patch.object(validate_site_sources, "REPO_ROOT", repo_root),
                patch.object(validate_site_sources, "DOCS_ROOT", docs_root),
            ):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        validate_site_sources.validate_no_restricted_or_sensitive_content()

    def test_rejects_legacy_parallel_course_term(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_root = repo_root / "docs"
            docs_root.mkdir(parents=True)
            (docs_root / "index.md").write_text(
                "# 首页\n\n旧稿仍写作双轨项目。\n",
                encoding="utf-8",
            )

            with (
                patch.object(validate_site_sources, "REPO_ROOT", repo_root),
                patch.object(validate_site_sources, "DOCS_ROOT", docs_root),
            ):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        validate_site_sources.validate_no_restricted_or_sensitive_content()

    def test_accepts_18_week_36_hour_course_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_root = repo_root / "docs"
            syllabus = docs_root / "teaching" / "36-hour-syllabus.md"
            syllabus.parent.mkdir(parents=True)
            syllabus.write_text(
                "\n".join(
                    f"| 第{week}周，2学时 | 主题 | 内容 | AI任务 | 重点 | 难点 | 产物 |"
                    for week in range(1, 19)
                ),
                encoding="utf-8",
            )

            with (
                patch.object(validate_site_sources, "REPO_ROOT", repo_root),
                patch.object(validate_site_sources, "DOCS_ROOT", docs_root),
            ):
                validate_site_sources.validate_unified_course_plan()


if __name__ == "__main__":
    unittest.main()
