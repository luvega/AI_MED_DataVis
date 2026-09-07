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
    "syllabus/36课时-学生学习地图.md": "teaching/36-hour-learning-map.md",
    "outputs/2026-08-21-NGS00移交包归档与课程融合更新/2026-08-21-统一综合项目模板.md": "teaching/unified-project-template.md",
    "outputs/2026-09-07-第一章自主阅读版更新/2026-09-07-第1章-课堂任务单.md": "teaching/chapter-1-task-sheet.md",
}

UNIFIED_SYLLABUS = SOURCE_ROOT / "syllabus" / "36课时-统一融合修订版.md"
FORBIDDEN_LEGACY_TERMS = ("拓展线", "双轨项目", "NGS拓展", "表格项目", "NGS项目")

REFERENCE_FILES = {
    "references/术语表.md": "references/terminology.md",
    "references/图表规范.md": "references/figure-guidelines.md",
    "references/提示词样例.md": "references/prompt-examples.md",
}

HOMEPAGE_COVER_SOURCE = (
    SOURCE_ROOT
    / "assets"
    / "homepage"
    / "medical-data-visualization-homepage-cover-imagegen.png"
)
HOMEPAGE_COVER_TARGET = (
    DOCS_ROOT / "assets" / "images" / "medical-data-visualization-homepage-cover-imagegen.png"
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def student_facing_support_content(content: str) -> str:
    return re.split(r"^## 教师提示\s*$", content, maxsplit=1, flags=re.MULTILINE)[0].rstrip() + "\n"


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
        source = SOURCE_ROOT / source_relative
        target = DOCS_ROOT / target_relative
        write_text(target, student_facing_support_content(read_text(source)))
    for source_relative, target_relative in REFERENCE_FILES.items():
        copy_file(SOURCE_ROOT / source_relative, DOCS_ROOT / target_relative)


def copy_homepage_cover() -> None:
    if not HOMEPAGE_COVER_SOURCE.is_file():
        raise FileNotFoundError(f"homepage cover not found: {HOMEPAGE_COVER_SOURCE}")
    copy_file(HOMEPAGE_COVER_SOURCE, HOMEPAGE_COVER_TARGET)


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

医药数据分析从明确对象和问题开始。先确认数据从哪里来、每一行表示什么、变量怎样测量，再选择处理、统计和可视化方法。分析的终点也不只是一张图或一个分数，而是一份能从结论回查到输入、处理、输出和解释条件的证据包。

本书面向药学本科生和研究生，不要求预先具备高级统计、生物信息学或编程基础。WorkBuddy 是课程统一使用的前台入口，用于组织工作空间、任务上下文、执行过程和结果核验。Python、R、Git、Miniconda、Node.js 和 Pandoc 根据具体任务调用。

[从第1章开始](chapters/chapter-1/index.md) · [先配置 WorkBuddy 工作空间](chapters/chapter-2/index.md) · [查看18周学习地图](teaching/36-hour-learning-map.md)

<figure class="homepage-cover">
  <img src="assets/images/medical-data-visualization-homepage-cover-imagegen.png" alt="医药数据从问题定义、数据对象和分析图表走向人工核验与证据包的课程封面图" width="1672" height="941" fetchpriority="high">
  <figcaption>从医药问题、数据对象和分析图表，到人工核验与可复现证据包。</figcaption>
</figure>

## 这本书帮助你完成什么

| 面对的问题 | 需要形成的能力 | 可检查的产物 |
| --- | --- | --- |
| 这份数据是什么 | 识别来源、观察单位、字段、矩阵方向、权限和质量风险 | 来源卡、数据字典、质量问题清单 |
| 这个医学问题怎样转成分析任务 | 写清样本、变量、结局、分组、比较和输出 | AI 任务说明书、分析路线 |
| 代码和图表是否可信 | 核对输入、处理步骤、真实输出、统计前提和文件变更 | 脚本、运行记录、图表与结果表 |
| 当前结果能说明什么 | 区分观察、统计推断、模型关联、医学解释和仍需验证内容 | 解释卡、核验清单、证据包 |

## 从问题到证据包

```mermaid
flowchart LR
  A["医学或药学问题"] --> B["数据对象与来源"]
  B --> C["任务说明书"]
  C --> D["处理、统计与可视化"]
  D --> E["真实输出"]
  E --> F["人工核验"]
  F --> G["证据包"]
  G --> H["允许解释与仍需验证"]
```

| 统一主线 | 递进关系 | 读者要形成的能力 |
| --- | --- | --- |
| 数据主线 | 医药表格 → 样本元数据 → 计数矩阵 → 高维结果 → 单细胞和多组学结果 | 识别观察单位、字段、矩阵方向、来源和质量风险 |
| 分析主线 | 读取整理 → 质量检查 → 统计推断 → 可视化 → 差异分析 → 证据综合 | 让方法、图表和解释与问题及设计对齐 |
| AI 主线 | 问题拆解 → 上下文组织 → 代码生成 → 错误诊断 → 结果核验 → 可复现交付 | 保留任务说明、人工修改、真实输出和证据边界 |

## 每章完成一件可检查的事

| 学习部分 | 主要任务 | 阶段产物 |
| --- | --- | --- |
| 第一篇，第1至3章 | 明确分析问题，建立 WorkBuddy 工作空间，写出可执行的 AI 任务说明 | 问题结构表、环境验收包、AI 协作记录 |
| 第二篇，第4至6章 | 识别数据对象，读取和清洗数据，完成整形与描述性分析 | 可运行脚本、数据字典、清洗记录、描述统计表 |
| 第三篇，第7至10章 | 设计科研图表，完成统计比较和基础模型，检查泄漏与解释范围 | 图表、图注、统计说明、模型报告 |
| 第四篇，第11至13章 | 处理高维矩阵，审阅 RNA-seq 数据链，记录公共数据来源 | PCA、聚类与热图结果、差异表达证据包、下载记录 |
| 第五篇，第14至15章 | 审阅单细胞、空间组学和多模态结果，完成综合项目 | 质控与注释记录、解释卡、可复现项目包 |

## WorkBuddy 与底层工具怎样分工

WorkBuddy 负责接收任务、限定工作空间、补充上下文、展示执行过程并核对产物和文件变更。底层工具只在任务需要时进入流程。软件能够启动或显示版本号，不等于分析已经通过验收；代码、真实输出、保存位置和解释边界仍需逐项检查。

AI 可以解释报错、整理任务说明、生成局部代码并提出核验清单。数据含义、分析单位、方法选择、隐私权限、结果解释和最终结论由人负责。涉及敏感数据、外部发送、权限扩大或医学判断时，应先暂停并确认适用规则。

[进入第2章：WorkBuddy 工作空间与结果核验](chapters/chapter-2/index.md)

## 贯穿案例与使用边界

Bioconductor `airway` 是全书的 bulk RNA-seq 贯穿案例。该数据包含8个人气道平滑肌细胞样本，来自4个细胞系，每个细胞系包含地塞米松处理与未处理样本。教材用它连接 metadata、计数矩阵、质量检查、标准化、PCA、热图、差异表达和富集审阅。

| 案例类型 | 在书中的用途 | 不能据此推出 |
| --- | --- | --- |
| `airway` 细胞实验数据 | 连接 bulk RNA-seq 数据对象、设计和结果表 | 临床疗效、患者结局或疾病机制 |
| 医药表格小案例 | 练习相关、回归、分类和统计图表 | 对真实人群的普遍结论 |
| 公共数据库记录 | 练习检索、下载登记、许可和引用 | 数据适合当前问题或结论已被验证 |
| 单细胞、空间和多模态案例 | 识别对象结构、质控、注释和解释边界 | 细胞标签天然正确、轨迹方向或细胞通讯已经证实 |

不同案例服务不同分析问题，不直接合并为同一研究结论。模拟数据、教材摘录、公开数据和本机复现结果均在正文中标明状态。

## 教材目录

{chapter_links()}
## 学生学习资源与参考规范

| 材料 | 页面 |
| --- | --- |
| 18周学生学习地图 | [查看](teaching/36-hour-learning-map.md) |
| 统一综合项目模板 | [查看](teaching/unified-project-template.md) |
| 第1章课堂任务单 | [查看](teaching/chapter-1-task-sheet.md) |
| 术语表 | [查看](references/terminology.md) |
| 图表规范 | [查看](references/figure-guidelines.md) |
| 提示词样例 | [查看](references/prompt-examples.md) |

## 阅读与提交约定

| 内容状态 | 阅读和使用要求 |
| --- | --- |
| 真实或公开数据 | 回查来源、版本、许可、查询日期和适用条件 |
| 模拟数据或教材摘录 | 只用于说明对象和方法，不写成真实医学发现 |
| 统计或模型输出 | 记录数据划分、参数、指标和运行状态，不把关联或预测写成因果 |
| AI 输出 | 与代码、文件和来源逐项核对，保留人工修改和责任人 |
| `需补证据` | 当前材料不足以支持相应判断 |
| `需人工确认` | 涉及权限、隐私、许可、专业判断或正式发布决定 |

完成一章后，读者应能够回答四个问题：使用了什么数据，执行了哪些处理，结果支持什么判断，还有哪些内容不能由当前证据回答。
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
    copy_homepage_cover()
    write_text(DOCS_ROOT / "index.md", build_homepage())
    print(f"Generated MkDocs content from {SOURCE_ROOT} into {DOCS_ROOT}")


if __name__ == "__main__":
    main()
