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


def parse_outline_titles() -> dict[int, str]:
    outline_path = DOCS_ROOT / "book-outline.md"
    if not outline_path.exists():
        fail("docs/book-outline.md is missing")
    titles: dict[int, str] = {}
    for line in read_text(outline_path).splitlines():
        match = re.match(r"### 第(\d+)章\s+(.+)$", line.strip())
        if match:
            number = int(match.group(1))
            if number in CHAPTER_RANGE:
                titles[number] = match.group(2).strip()
    missing = [number for number in CHAPTER_RANGE if number not in titles]
    if missing:
        fail(f"missing chapter titles in book outline: {missing}")
    return titles


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
        outline = chapter_dir / "outline.md"
        if not body.exists():
            fail(f"missing chapter body: {body.relative_to(REPO_ROOT)}")
        if not outline.exists():
            fail(f"missing chapter outline: {outline.relative_to(REPO_ROOT)}")
        expected_h1 = f"第{number}章 {title}"
        if first_h1(body) != expected_h1:
            fail(f"body H1 mismatch in {body.relative_to(REPO_ROOT)}")
        if first_h1(outline) != expected_h1:
            fail(f"outline H1 mismatch in {outline.relative_to(REPO_ROOT)}")


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
    chapter_titles = parse_outline_titles()
    validate_chapters(chapter_titles)
    validate_nav(chapter_titles)
    validate_image_links()
    validate_no_raw_reference_dir()
    validate_required_support_files()
    print("Site source validation passed.")


if __name__ == "__main__":
    main()
