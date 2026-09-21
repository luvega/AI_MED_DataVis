from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import validate_site_sources


class OutlineValidationTests(unittest.TestCase):
    def test_scans_gb18030_teaching_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_root = repo_root / "docs"
            fixture = docs_root / "chapters/chapter-5/assets/case-THU-DA-L02-C01-A02/data/guesses_gb18030.csv"
            fixture.parent.mkdir(parents=True)
            with (
                patch.object(validate_site_sources, "REPO_ROOT", repo_root),
                patch.object(validate_site_sources, "DOCS_ROOT", docs_root),
            ):
                fixture.write_text("编号,估计\n甲,100\n", encoding="gb18030")
                validate_site_sources.validate_no_restricted_or_sensitive_content()
                fixture.write_text("地址\n192.168.1.23\n", encoding="gb18030")
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        validate_site_sources.validate_no_restricted_or_sensitive_content()

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

    def test_rejects_teacher_only_support_page(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            docs_root = repo_root / "docs"
            teacher_plan = docs_root / "teaching" / "18-week-teacher-plan.md"
            teacher_plan.parent.mkdir(parents=True)
            teacher_plan.write_text(
                "# 教师教案\n",
                encoding="utf-8",
            )

            with (
                patch.object(validate_site_sources, "REPO_ROOT", repo_root),
                patch.object(validate_site_sources, "DOCS_ROOT", docs_root),
            ):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        validate_site_sources.validate_no_teacher_only_support_files()


if __name__ == "__main__":
    unittest.main()
