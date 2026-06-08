from __future__ import annotations

import os
import re
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(os.environ.get("AI_MED_BOOK_SOURCE", "E:/Codex_Projects/AI_MED_DataVis_Book"))
DOCS_ROOT = REPO_ROOT / "docs"

CHAPTER_TITLES = {
    1: "医药数据分析导论",
    2: "AI 生产力工具链与项目环境",
    3: "AI 任务说明书与协作规范",
    4: "Python 与 R 数据结构基础",
    5: "数据读取、数据字典与数据质量",
    6: "数据整形、描述统计与探索性可视化",
    7: "图表契约与科研图表规范",
    8: "统计推断与组间比较",
    9: "相关、回归与分类模型",
    10: "模型评估、特征选择与可解释性",
    11: "高维矩阵、PCA、聚类与热图",
    12: "RNA-seq 数据链条与差异表达分析",
    13: "公共数据库、序列数据与医药大数据智能分析",
    14: "单细胞转录组数据处理与可视化",
    15: "单细胞进阶、空间组学与综合项目",
}

PARTS = [
    ("第一篇 课程入口、工具链与 AI 协作规范", [1, 2, 3]),
    ("第二篇 数据结构、读取、清洗与探索性分析", [4, 5, 6]),
    ("第三篇 图表表达、统计推断与基础建模", [7, 8, 9, 10]),
    ("第四篇 高维医药数据与 bulk 组学分析", [11, 12, 13]),
    ("第五篇 单细胞、空间组学与综合项目", [14, 15]),
]

TEACHING_FILES = {
    "chapters/chapter-1/第1章-课堂任务单-第一版.md": "teaching/chapter-1-task-sheet.md",
    "chapters/chapter-6/第6章-使用材料清单.md": "teaching/chapter-6-material-list.md",
    "chapters/chapter-6/第6章-材料护照.md": "teaching/chapter-6-material-passport.md",
}

REFERENCE_FILES = {
    "references/术语表.md": "references/terminology.md",
    "references/图表规范.md": "references/figure-guidelines.md",
    "references/提示词样例.md": "references/prompt-examples.md",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def remove_generated_dirs() -> None:
    for relative in ["chapters", "teaching", "references"]:
        target = DOCS_ROOT / relative
        if target.exists():
            shutil.rmtree(target)
    for relative in ["index.md", "book-outline.md"]:
        target = DOCS_ROOT / relative
        if target.exists():
            target.unlink()


def chapter_body_path(chapter_number: int) -> Path:
    chapter_dir = SOURCE_ROOT / "chapters" / f"chapter-{chapter_number}"
    candidates = [
        path
        for path in chapter_dir.glob("*.md")
        if path.name != "本章大纲.md"
        and "材料" not in path.name
        and "课堂任务单" not in path.name
    ]
    if not candidates:
        raise FileNotFoundError(f"missing body markdown for chapter-{chapter_number}")
    return max(candidates, key=lambda path: path.stat().st_size)


def copy_chapters() -> None:
    for chapter_number in CHAPTER_TITLES:
        source_dir = SOURCE_ROOT / "chapters" / f"chapter-{chapter_number}"
        target_dir = DOCS_ROOT / "chapters" / f"chapter-{chapter_number}"
        body = chapter_body_path(chapter_number)
        outline = source_dir / "本章大纲.md"
        if not outline.exists():
            raise FileNotFoundError(outline)
        copy_file(body, target_dir / "index.md")
        copy_file(outline, target_dir / "outline.md")
        assets = source_dir / "assets"
        if assets.exists():
            shutil.copytree(assets, target_dir / "assets", dirs_exist_ok=True)


def copy_support_files() -> None:
    copy_file(SOURCE_ROOT / "大纲.md", DOCS_ROOT / "book-outline.md")
    for source_relative, target_relative in TEACHING_FILES.items():
        copy_file(SOURCE_ROOT / source_relative, DOCS_ROOT / target_relative)
    for source_relative, target_relative in REFERENCE_FILES.items():
        copy_file(SOURCE_ROOT / source_relative, DOCS_ROOT / target_relative)


def chapter_links() -> str:
    lines: list[str] = []
    for part_title, chapter_numbers in PARTS:
        lines.append(f"## {part_title}")
        lines.append("")
        lines.append("| 章节 | 正文 | 本章大纲 |")
        lines.append("| --- | --- | --- |")
        for number in chapter_numbers:
            title = CHAPTER_TITLES[number]
            lines.append(
                f"| 第{number}章 {title} | "
                f"[进入正文](chapters/chapter-{number}/index.md) | "
                f"[查看大纲](chapters/chapter-{number}/outline.md) |"
            )
        lines.append("")
    return "\n".join(lines)


def build_homepage() -> str:
    return f"""# 医药数据处理与可视化

本网站发布《医药数据处理与可视化》在线教材。教材面向药学本科生和研究生，不默认学生具备高级统计、生信或编程背景。

课程主线围绕数据结构、数据清洗、统计解释、图表表达和 AI 协作核验展开。AI 工具用于辅助检查、整理和生成局部代码，不能替代学生判断数据来源、变量含义、统计前提和医学解释边界。

## 核验顺序

| 顺序 | 材料 | 用途 |
| --- | --- | --- |
| 1 | `AGENTS.md` | 确认项目规则、只读目录、输出路径和写作边界 |
| 2 | `大纲.md` | 作为全书篇名、章名和小节结构的唯一来源 |
| 3 | `chapters/chapter-*/本章大纲.md` | 作为各章结构蓝图 |
| 4 | `chapters/chapter-*/*正文*.md` | 作为在线教材正文来源 |
| 5 | `references/术语表.md`、`references/图表规范.md`、`references/提示词样例.md` | 统一术语、图表契约和 AI 协作边界 |

## 教材目录

{chapter_links()}
## 备课与参考规范

| 材料 | 页面 |
| --- | --- |
| 第1章课堂任务单 | [查看](teaching/chapter-1-task-sheet.md) |
| 第6章使用材料清单 | [查看](teaching/chapter-6-material-list.md) |
| 第6章材料护照 | [查看](teaching/chapter-6-material-passport.md) |
| 术语表 | [查看](references/terminology.md) |
| 图表规范 | [查看](references/figure-guidelines.md) |
| 提示词样例 | [查看](references/prompt-examples.md) |

## 证据边界

站点正文保留原教材中的 `需补证据` 和 `需人工确认` 标记。凡涉及生物医学、药学、组学、AI 模型或临床解释的内容，均应区分观察结果、方法来源、允许解释、替代解释和仍需验证内容。
"""


def verify_source_outline() -> None:
    outline = read_text(SOURCE_ROOT / "大纲.md")
    for number, title in CHAPTER_TITLES.items():
        pattern = rf"### 第{number}章 {re.escape(title)}"
        if not re.search(pattern, outline):
            raise ValueError(f"chapter title not found in root outline: 第{number}章 {title}")


def main() -> None:
    if not SOURCE_ROOT.exists():
        raise FileNotFoundError(f"source root not found: {SOURCE_ROOT}")
    verify_source_outline()
    remove_generated_dirs()
    copy_chapters()
    copy_support_files()
    write_text(DOCS_ROOT / "index.md", build_homepage())
    print(f"Generated MkDocs content from {SOURCE_ROOT} into {DOCS_ROOT}")


if __name__ == "__main__":
    main()
