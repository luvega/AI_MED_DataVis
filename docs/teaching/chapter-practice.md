# 全书学生练习包

下载对应章节的ZIP，解压后先读 `README.md`。输入保存在 `data/`，运行结果写入 `outputs/`。每个包的 `manifest.json` 列出版本、运行入口、编码与文件校验值。

已发布 4 / 15 章；正文与练习包按批同步更新。

| 章节 | 练习包 | 版本 | 大小 |
| --- | --- | --- | --- |
| [第1章 医药数据分析导论](../chapters/chapter-1/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第2章 AI 生产力工具链与项目环境](../chapters/chapter-2/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第3章 AI 任务说明书与协作规范](../chapters/chapter-3/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第4章 Python 与 R 数据结构基础](../chapters/chapter-4/index.md) | [下载ZIP](../downloads/chapter-04-practice.zip) | 2026-10-02 | 8 KB |
| [第5章 数据读取、数据字典与数据质量](../chapters/chapter-5/index.md) | [下载ZIP](../downloads/chapter-05-practice.zip) | 2026-10-02 | 26 KB |
| [第6章 数据整形、描述统计与探索性可视化](../chapters/chapter-6/index.md) | [下载ZIP](../downloads/chapter-06-practice.zip) | 2026-10-02 | 20 KB |
| [第7章 科研图表规范与 SCI 图表表达](../chapters/chapter-7/index.md) | [下载ZIP](../downloads/chapter-07-practice.zip) | 2026-10-02 | 112 KB |
| [第8章 统计推断与组间比较](../chapters/chapter-8/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第9章 相关、回归与分类模型](../chapters/chapter-9/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第10章 模型评估、特征选择与可解释性](../chapters/chapter-10/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第11章 高维矩阵、PCA、聚类与热图](../chapters/chapter-11/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第12章 RNA-seq 数据链条与差异表达分析](../chapters/chapter-12/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第13章 公共数据库、序列数据与医药大数据智能分析](../chapters/chapter-13/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第14章 单细胞转录组数据处理与可视化](../chapters/chapter-14/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第15章 单细胞进阶、空间组学与综合项目](../chapters/chapter-15/index.md) | 本批尚未发布 | 待发布 | 待发布 |

前期练习以Python为主，R用于已有对照与适合的领域分析。RNA-seq、单细胞和进阶章节在README中区分实际运行入口、轻量练习与大型数据拓展。基础练习使用本地文件。

<a id="chapter-4"></a>

## 第4章开始说明

# 第4章练习包

本包帮助你从三条CFU记录开始，亲手输入、预测、运行和保存短程序，再检查糖豆表中的对象、缺失、索引和函数。Python先学，R用于已熟悉问题的对照。

解压后在本目录打开终端。基础环境为Python和pandas；R脚本使用基础R。安装依赖使用 `python -m pip install -r requirements.txt`。

```text
python scripts/01_mean_cfu.py
python scripts/02_objects.py
python scripts/03_conditions_functions.py
Rscript scripts/04_objects.R
```

01对应4.1与4.5，先阅读后把关键五行自己输入解释器。02对应4.2-4.3，运行前手工圈出阈值950保留的记录。03对应4.4，指出函数输入和返回值。04用同一糖豆表和CFU表对照位置、名称和条件。

演示脚本可独立运行，不要求复用前一次会话里的对象。所有结果写入outputs。完成exercises.md中的条件变化题，在records.md填写本人记录。reference仅含演示核对信息，独立任务由你完成。

<a id="chapter-5"></a>

## 第5章开始说明

# 第5章读取与质量练习

在解压后的本包根目录打开终端，先确认能看到data、scripts和outputs。安装requirements.txt所列依赖后依次运行

```powershell
python scripts/01_read_files.py
python scripts/02_inventory_quality.py
python scripts/03_guesses_quality.py
Rscript scripts/03_guesses_quality.R
```

01对应5.1、5.2，核对6×8实验表、工作表和编码副本。02对应5.3、5.6，库存构造表25行，库存任务保留23行；重复候选只标记，单价缺失保留。03对应糖豆主案例，原14条记录、确认副本处理后13条、可数值化9条。R脚本仅需基础R，与Python核对记录号、数量及数值。完整来源、字典及独立任务见本包同名文件。运行结果均写入outputs。

<a id="chapter-6"></a>

## 第6章开始说明

# 第6章整形与汇总练习

从本包根目录运行

```powershell
python scripts/01_reshape_summary.py
python scripts/02_inventory_summary.py
Rscript scripts/03_summary.R
```

01以36条实验测量形成12行宽表，回到36行长表，再按三个键恢复源单元格并生成12组汇总。02使用与第5章相同的23条库存分析记录，统计与作图共享输入。03用基础R核对同一实验分组的n、均值、中位数、SD和SEM。每次运行结果写入outputs。依赖见requirements.txt。图中英文Form编号可回到inventory_by_form.csv对照真实构造标签。

04迁移练习读取本章4×4指标宽表与4×2分组表，恢复4×5表后转为12×4长表；读取8行销售摘录和7行分类表，完成多对一连接、日期解析和汇总。运行 `python scripts/04_transfer.py`。这些输入与正文内嵌示例逐值对应。

<a id="chapter-7"></a>

## 第7章开始说明

# 第7章练习包

本包从同一分析表绘图、导出并回查。NHANES演示分布与不同子图的有效记录数；Lolamicin演示全部原始点、均值和两种误差线。所有输入都已包含在本包内。

在解压后的本目录打开终端，Python环境安装requirements.txt中的三个包，R练习只需基础R。

```text
python scripts/01_nhanes_plot.py
python scripts/02_lolamicin_plot.py
Rscript scripts/03_lolamicin_plot.R
```

01对应7.1-7.3，写出未加权分布图、分母核对表及作图数据。02对应7.4-7.5，输出36条原始点图、12组汇总和2小时的SD/SEM比较图。03从同一36行CSV重新汇总，提供R对照。各入口可独立运行，均写入outputs。

打开PNG查看预览，再打开SVG或PDF检查轴、图例和裁切。填写design_card.md、records.md，完成exercises.md中的局部修改。下载包中的示例核对点用于演示检查，独立练习由你先预测再完成。
