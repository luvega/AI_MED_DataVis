from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(os.environ.get("AI_MED_BOOK_SOURCE", "E:/Codex_Projects/AI_MED_DataVis_Book"))
DOCS_ROOT = REPO_ROOT / "docs"
IMAGE_PATTERN = re.compile(r"(!\[[^\]]*\]\()([^)]+)(\))")

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

PARTS = [
    ("第一篇 课程入口、工具链与 AI 协作规范", [1, 2, 3]),
    ("第二篇 数据结构、读取、清洗与探索性分析", [4, 5, 6]),
    ("第三篇 图表表达、统计推断与基础建模", [7, 8, 9, 10]),
    ("第四篇 高维医药数据与 bulk 组学分析", [11, 12, 13]),
    ("第五篇 单细胞、空间组学与综合项目", [14, 15]),
]

TEACHING_FILES = {
    "syllabus/36课时-统一融合修订版.md": "teaching/36-hour-syllabus.md",
    "syllabus/36课时-学生学习地图.md": "teaching/36-hour-learning-map.md",
    "outputs/2026-08-21-NGS00移交包归档与课程融合更新/2026-08-21-18周教师教案.md": "teaching/18-week-teacher-plan.md",
    "outputs/2026-08-21-NGS00移交包归档与课程融合更新/2026-08-21-统一综合项目模板.md": "teaching/unified-project-template.md",
    "outputs/2026-06-06-第一章正文生成/2026-06-06-第1章-课堂任务单.md": "teaching/chapter-1-task-sheet.md",
    "chapters/chapter-6/第6章-使用材料清单.md": "teaching/chapter-6-material-list.md",
    "chapters/chapter-6/第6章-材料护照.md": "teaching/chapter-6-material-passport.md",
}

UNIFIED_SYLLABUS = SOURCE_ROOT / "syllabus" / "36课时-统一融合修订版.md"
FORBIDDEN_LEGACY_TERMS = ("拓展线", "双轨项目", "NGS拓展", "表格项目", "NGS项目")

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


def materialize_external_images(body: Path, target_dir: Path, content: str) -> str:
    chapter_dir = body.parent.resolve()
    source_root = SOURCE_ROOT.resolve()

    def replace(match: re.Match[str]) -> str:
        target = match.group(2).strip()
        if target.startswith(("http://", "https://", "data:", "#")):
            return match.group(0)

        path_part = target.split("#", 1)[0].split("?", 1)[0]
        source_image = (body.parent / unquote(path_part)).resolve()
        if not source_image.is_file():
            return match.group(0)

        try:
            source_image.relative_to(source_root)
        except ValueError as error:
            raise ValueError(f"image target is outside source root: {source_image}") from error

        try:
            source_image.relative_to(chapter_dir)
            return match.group(0)
        except ValueError:
            pass

        target_image = target_dir / "assets" / source_image.name
        if target_image.exists() and target_image.read_bytes() != source_image.read_bytes():
            raise ValueError(f"conflicting chapter asset name: {target_image.name}")
        copy_file(source_image, target_image)
        return f"{match.group(1)}assets/{source_image.name}{match.group(3)}"

    return IMAGE_PATTERN.sub(replace, content)


def remove_generated_dirs() -> None:
    for relative in ["chapters", "teaching", "references", "book-outline"]:
        target = DOCS_ROOT / relative
        if target.exists():
            shutil.rmtree(target)
    for relative in ["index.md", "book-outline.md"]:
        target = DOCS_ROOT / relative
        if target.exists():
            target.unlink()


def chapter_body_path(chapter_number: int) -> Path:
    chapter_dir = SOURCE_ROOT / "chapters" / f"chapter-{chapter_number}"
    preferred = chapter_dir / "正文.md"
    if preferred.exists():
        return preferred
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
        assets = source_dir / "assets"
        if assets.exists():
            shutil.copytree(assets, target_dir / "assets", dirs_exist_ok=True)
        content = materialize_external_images(body, target_dir, read_text(body))
        write_text(target_dir / "index.md", content)


def copy_support_files() -> None:
    for source_relative, target_relative in TEACHING_FILES.items():
        copy_file(SOURCE_ROOT / source_relative, DOCS_ROOT / target_relative)
    for source_relative, target_relative in REFERENCE_FILES.items():
        copy_file(SOURCE_ROOT / source_relative, DOCS_ROOT / target_relative)


def chapter_links() -> str:
    lines: list[str] = []
    for part_title, chapter_numbers in PARTS:
        lines.append(f"## {part_title}")
        lines.append("")
        lines.append("| 章节 | 正文 |")
        lines.append("| --- | --- |")
        for number in chapter_numbers:
            title = CHAPTER_TITLES[number]
            lines.append(
                f"| 第{number}章 {title} | "
                f"[进入正文](chapters/chapter-{number}/index.md) |"
            )
        lines.append("")
    return "\n".join(lines)


def build_homepage() -> str:
    return f"""# 医药数据处理与可视化

《医药数据处理与可视化》是一门面向药学本科生和研究生的入门教材。它不把学生预设为程序员，也不把数据分析写成软件命令清单。本书更关心一个学生能否看懂医药数据从哪里来、每一行和每一列代表什么、图表能支持哪一句判断，以及哪些内容必须留给人工核验。

本书只有一套必修课程路径。前几章帮助学生建立项目环境、AI 协作规范和基本数据结构；中间章节进入读取、清洗、描述统计、科研图表和基础模型；后续章节用同一分析框架处理高维矩阵、RNA-seq、公共数据库、单细胞和空间组学。每一章都把“是什么、为什么、怎么检查”放在一起。

AI 工具在本书中是协作对象，不是结论来源。学生可以让 AI 解释报错、整理任务说明书、生成局部代码和检查图注，但不能让 AI 猜字段含义、替代统计前提判断，或把图中模式写成医学因果。所有关键输出都应能追溯到数据、代码、图表契约、人工核验和仍需确认事项。

贯穿案例使用Bioconductor `airway`：8个人气道平滑肌细胞bulk RNA-seq样本，来自4个细胞系，每个细胞系有地塞米松处理与未处理样本。它连接metadata、计数矩阵、样本质控、标准化、PCA、热图、差异表达和富集审阅。相关、回归和分类继续使用现有医药表格小案例，因为8个样本不适合预测建模。细胞实验结果不能外推为临床疗效或疾病机制。

| 统一主线 | 递进关系 | 读者要形成的能力 |
| --- | --- | --- |
| 数据主线 | 医药表格 → 样本元数据 → 计数矩阵 → 高维结果 → 单细胞和多组学结果 | 识别观察单位、字段、矩阵方向、来源和质量风险 |
| 分析主线 | 读取整理 → 质量检查 → 统计推断 → 可视化 → 差异分析 → 证据综合 | 让方法、图表和解释与问题及设计对齐 |
| AI主线 | 问题拆解 → 代码生成 → 错误诊断 → 结果核验 → 证据审查 → 可复现交付 | 保留任务说明、人工修改、运行结果和证据边界 |

## 教材目录

{chapter_links()}
## 备课与参考规范

| 材料 | 页面 |
| --- | --- |
| 36课时统一课程计划 | [查看](teaching/36-hour-syllabus.md) |
| 18周学生学习地图 | [查看](teaching/36-hour-learning-map.md) |
| 18周教师教案 | [查看](teaching/18-week-teacher-plan.md) |
| 统一综合项目模板 | [查看](teaching/unified-project-template.md) |
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
    legacy_hits = [term for term in FORBIDDEN_LEGACY_TERMS if term in outline]
    if legacy_hits:
        raise ValueError(f"legacy course-route terms found in root outline: {legacy_hits}")


def verify_unified_syllabus() -> None:
    if not UNIFIED_SYLLABUS.exists():
        raise FileNotFoundError(f"unified syllabus not found: {UNIFIED_SYLLABUS}")
    syllabus = read_text(UNIFIED_SYLLABUS)
    if "# 《医药数据处理与可视化》36课时统一融合修订版" not in syllabus:
        raise ValueError("unified syllabus title or course name is incorrect")

    week_rows = re.findall(r"^\| 第(\d+)周，(\d+)学时 \|(.+)$", syllabus, flags=re.MULTILINE)
    weeks = [int(week) for week, _, _ in week_rows]
    hours = [int(hour) for _, hour, _ in week_rows]
    if weeks != list(range(1, 19)):
        raise ValueError(f"unified syllabus must contain weeks 1-18 exactly once: {weeks}")
    if sum(hours) != 36:
        raise ValueError(f"unified syllabus must total 36 hours, got {sum(hours)}")
    if "合计：18个教学单元，36学时。" not in syllabus:
        raise ValueError("unified syllabus total statement is missing")
    for week, _, remainder in week_rows:
        cells = [cell.strip() for cell in remainder.split("|") if cell.strip()]
        if len(cells) != 6:
            raise ValueError(f"week {week} must contain 7 table cells including week/hour")
        if len(cells[2]) < 12:
            raise ValueError(f"week {week} AI task is not concrete enough")
    legacy_hits = [term for term in FORBIDDEN_LEGACY_TERMS if term in syllabus]
    if legacy_hits:
        raise ValueError(f"legacy course-route terms found in unified syllabus: {legacy_hits}")


def main() -> None:
    if not SOURCE_ROOT.exists():
        raise FileNotFoundError(f"source root not found: {SOURCE_ROOT}")
    verify_source_outline()
    verify_unified_syllabus()
    remove_generated_dirs()
    copy_chapters()
    copy_support_files()
    write_text(DOCS_ROOT / "index.md", build_homepage())
    print(f"Generated MkDocs content from {SOURCE_ROOT} into {DOCS_ROOT}")


if __name__ == "__main__":
    main()
