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

    def test_accepts_exactly_18_weeks_and_36_hours(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            syllabus = Path(temp_dir) / "syllabus.md"
            rows = "\n".join(
                f"| 第{week}周，2学时 | 主题 | 具体教学内容与课堂活动 | AI检查具体数据代码结果 | 重点 | 难点 | 保存产物 |"
                for week in range(1, 19)
            )
            syllabus.write_text(
                "# 《医药数据处理与可视化》36课时统一融合修订版\n\n"
                + rows
                + "\n\n合计：18个教学单元，36学时。\n",
                encoding="utf-8",
            )

            with patch.object(generate_site, "UNIFIED_SYLLABUS", syllabus):
                generate_site.verify_unified_syllabus()

    def test_rejects_incomplete_unified_syllabus(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            syllabus = Path(temp_dir) / "syllabus.md"
            rows = "\n".join(
                f"| 第{week}周，2学时 | 主题 | 具体教学内容与课堂活动 | AI检查具体数据代码结果 | 重点 | 难点 | 保存产物 |"
                for week in range(1, 18)
            )
            syllabus.write_text(
                "# 《医药数据处理与可视化》36课时统一融合修订版\n\n"
                + rows
                + "\n\n合计：18个教学单元，36学时。\n",
                encoding="utf-8",
            )

            with patch.object(generate_site, "UNIFIED_SYLLABUS", syllabus):
                with self.assertRaises(ValueError):
                    generate_site.verify_unified_syllabus()

    def test_homepage_uses_one_ai_airway_course_route(self) -> None:
        homepage = generate_site.build_homepage()
        self.assertIn("airway", homepage)
        self.assertIn("数据主线", homepage)
        self.assertIn("AI主线", homepage)
        self.assertIn("学生学习资源", homepage)
        self.assertIn("18周学生学习地图", homepage)
        self.assertIn("统一综合项目模板", homepage)
        for teacher_only_label in ("课程计划", "教师教案", "材料清单", "材料护照"):
            self.assertNotIn(teacher_only_label, homepage)
        for term in generate_site.FORBIDDEN_LEGACY_TERMS:
            self.assertNotIn(term, homepage)

    def test_only_student_facing_teaching_files_are_generated(self) -> None:
        targets = set(generate_site.TEACHING_FILES.values())
        self.assertEqual(
            targets,
            {
                "teaching/36-hour-learning-map.md",
                "teaching/unified-project-template.md",
                "teaching/chapter-1-task-sheet.md",
            },
        )

    def test_teacher_tip_section_is_removed_from_public_support_content(self) -> None:
        content = "# 学生任务\n\n## 提交要求\n\n提交作业。\n\n## 教师提示\n\n批改说明。\n"
        public_content = generate_site.student_facing_support_content(content)
        self.assertIn("## 提交要求", public_content)
        self.assertNotIn("教师提示", public_content)
        self.assertNotIn("批改说明", public_content)

if __name__ == "__main__":
    unittest.main()
