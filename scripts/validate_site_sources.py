from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml
import pymdownx.superfences  # noqa: F401


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = REPO_ROOT / "docs"
MKDOCS_CONFIG = REPO_ROOT / "mkdocs.yml"
CHAPTER_RANGE = range(1, 16)
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def first_h1(path: Path) -> str:
    for line in read_text(path).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    fail(f"missing H1 in {path.relative_to(REPO_ROOT)}")
    return ""


CHAPTER_TITLES = {
    1: "医药数据分析导论",
    2: "AI 生产力工具链与项目环境",
    3: "AI 任务说明书与协作规范",
    4: "Python 与 R 数据结构基础",
    5: "数据读取、数据字典与数据质量",
    6: "数据整形、描述统计与探索性可视化",
    7: "科研图表规范与 SCI 图表表达",
    8: "统计推断与组间比较",
    9: "相关、回归与分类模型",
    10: "模型评估、特征选择与可解释性",
    11: "高维矩阵、PCA、聚类与热图",
    12: "RNA-seq 数据链条与差异表达分析",
    13: "公共数据库、序列数据与医药大数据智能分析",
    14: "单细胞转录组数据处理与可视化",
    15: "单细胞进阶、空间组学与综合项目",
}


def flatten_nav(items: list[object]) -> list[tuple[str, str]]:
    flattened: list[tuple[str, str]] = []
    for item in items:
        if isinstance(item, dict):
            for label, value in item.items():
                if isinstance(value, str):
                    flattened.append((label, value))
                elif isinstance(value, list):
                    flattened.extend(flatten_nav(value))
        elif isinstance(item, str):
            flattened.append((item, item))
    return flattened


def validate_nav(chapter_titles: dict[int, str]) -> None:
    config = yaml.load(read_text(MKDOCS_CONFIG), Loader=yaml.FullLoader)
    nav_items = flatten_nav(config.get("nav", []))
    nav_by_path = {path: label for label, path in nav_items}
    forbidden_nav = [
        (label, path)
        for label, path in nav_items
        if path == "book-outline.md" or path.endswith("/outline.md") or "大纲" in label
    ]
    if forbidden_nav:
        fail(f"outline pages must not be in navigation: {forbidden_nav}")
    for number, title in chapter_titles.items():
        body_path = f"chapters/chapter-{number}/index.md"
        expected_label = f"第{number}章 {title}"
        actual_label = nav_by_path.get(body_path)
        if actual_label != expected_label:
            fail(f"nav mismatch for {body_path}: expected '{expected_label}', got '{actual_label}'")


def validate_chapters(chapter_titles: dict[int, str]) -> None:
    for number, title in chapter_titles.items():
        chapter_dir = DOCS_ROOT / "chapters" / f"chapter-{number}"
        body = chapter_dir / "index.md"
        if not body.exists():
            fail(f"missing chapter body: {body.relative_to(REPO_ROOT)}")
        expected_h1 = f"第{number}章 {title}"
        if first_h1(body) != expected_h1:
            fail(f"body H1 mismatch in {body.relative_to(REPO_ROOT)}")


def validate_image_links() -> None:
    for markdown_path in DOCS_ROOT.rglob("*.md"):
        text = read_text(markdown_path)
        for match in IMAGE_PATTERN.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "data:", "#")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            target_path = (markdown_path.parent / unquote(target)).resolve()
            if not target_path.exists():
                fail(
                    "missing image target "
                    f"'{target}' referenced from {markdown_path.relative_to(REPO_ROOT)}"
                )


def validate_no_raw_reference_dir() -> None:
    forbidden_names = {"参考资料"}
    for path in REPO_ROOT.rglob("*"):
        if any(part in forbidden_names for part in path.parts):
            fail(f"forbidden raw reference path copied into repo: {path.relative_to(REPO_ROOT)}")


def validate_no_outline_pages() -> None:
    forbidden_paths = [
        DOCS_ROOT / "book-outline.md",
        DOCS_ROOT / "book-outline",
        *DOCS_ROOT.glob("chapters/chapter-*/outline.md"),
        *DOCS_ROOT.glob("chapters/chapter-*/outline"),
    ]
    existing = [path.relative_to(REPO_ROOT).as_posix() for path in forbidden_paths if path.exists()]
    if existing:
        fail(f"outline pages must not be published: {existing}")
    index = read_text(DOCS_ROOT / "index.md")
    if "查看大纲" in index or "本章大纲 |" in index:
        fail("homepage still links to chapter outlines")


def validate_required_support_files() -> None:
    required = [
        DOCS_ROOT / "teaching" / "chapter-1-task-sheet.md",
        DOCS_ROOT / "teaching" / "chapter-6-material-list.md",
        DOCS_ROOT / "teaching" / "chapter-6-material-passport.md",
        DOCS_ROOT / "references" / "terminology.md",
        DOCS_ROOT / "references" / "figure-guidelines.md",
        DOCS_ROOT / "references" / "prompt-examples.md",
    ]
    for path in required:
        if not path.exists():
            fail(f"missing support file: {path.relative_to(REPO_ROOT)}")


def main() -> None:
    if not DOCS_ROOT.exists():
        fail("docs directory is missing")
    chapter_titles = CHAPTER_TITLES
    validate_chapters(chapter_titles)
    validate_nav(chapter_titles)
    validate_image_links()
    validate_no_raw_reference_dir()
    validate_no_outline_pages()
    validate_required_support_files()
    print("Site source validation passed.")


if __name__ == "__main__":
    main()
