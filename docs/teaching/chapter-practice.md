# 全书学生练习包

下载对应章节的ZIP，解压后先读 `README.md`。输入保存在 `data/`，运行结果写入 `outputs/`。每个包的 `manifest.json` 列出版本、运行入口、编码与文件校验值。

已发布 10 / 15 章；正文与练习包按批同步更新。

| 章节 | 练习包 | 版本 | 大小 |
| --- | --- | --- | --- |
| [第1章 医药数据分析导论](../chapters/chapter-1/index.md) | [下载ZIP](../downloads/chapter-01-practice.zip) | 2026-10-02 | 6 KB |
| [第2章 AI 生产力工具链与项目环境](../chapters/chapter-2/index.md) | [下载ZIP](../downloads/chapter-02-practice.zip) | 2026-10-02 | 6 KB |
| [第3章 AI 任务说明书与协作规范](../chapters/chapter-3/index.md) | [下载ZIP](../downloads/chapter-03-practice.zip) | 2026-10-02 | 18 KB |
| [第4章 Python 与 R 数据结构基础](../chapters/chapter-4/index.md) | [下载ZIP](../downloads/chapter-04-practice.zip) | 2026-10-02 | 8 KB |
| [第5章 数据读取、数据字典与数据质量](../chapters/chapter-5/index.md) | [下载ZIP](../downloads/chapter-05-practice.zip) | 2026-10-02 | 26 KB |
| [第6章 数据整形、描述统计与探索性可视化](../chapters/chapter-6/index.md) | [下载ZIP](../downloads/chapter-06-practice.zip) | 2026-10-02 | 20 KB |
| [第7章 科研图表规范与 SCI 图表表达](../chapters/chapter-7/index.md) | [下载ZIP](../downloads/chapter-07-practice.zip) | 2026-10-02 | 112 KB |
| [第8章 统计推断与组间比较](../chapters/chapter-8/index.md) | [下载ZIP](../downloads/chapter-08-practice.zip) | 2026-10-02 | 16 KB |
| [第9章 相关、回归与分类模型](../chapters/chapter-9/index.md) | [下载ZIP](../downloads/chapter-09-practice.zip) | 2026-10-02 | 11 KB |
| [第10章 模型评估、特征选择与可解释性](../chapters/chapter-10/index.md) | [下载ZIP](../downloads/chapter-10-practice.zip) | 2026-10-02 | 25 KB |
| [第11章 高维矩阵、PCA、聚类与热图](../chapters/chapter-11/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第12章 RNA-seq 数据链条与差异表达分析](../chapters/chapter-12/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第13章 公共数据库、序列数据与医药大数据智能分析](../chapters/chapter-13/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第14章 单细胞转录组数据处理与可视化](../chapters/chapter-14/index.md) | 本批尚未发布 | 待发布 | 待发布 |
| [第15章 单细胞进阶、空间组学与综合项目](../chapters/chapter-15/index.md) | 本批尚未发布 | 待发布 | 待发布 |

前期练习以Python为主，R用于已有对照与适合的领域分析。RNA-seq、单细胞和进阶章节在README中区分实际运行入口、轻量练习与大型数据拓展。基础练习使用本地文件。

<a id="chapter-1"></a>

## 第1章开始说明

# 第1章练习包

先读两张小表，手工数记录、参与者和缺失，再填写question_card.md。birth_mode_counts.csv对应1.1的434份问卷汇总，guesses.csv对应1.2-1.3的五行糖豆构造表。

本章以读表和确定问题为主。教师演示或课后想核对时，可在解压根目录运行 `python scripts/01_records.py`；脚本只使用Python标准库，将核对表写入outputs。独立任务在exercises.md，先独立作答再对照输出。

包内没有出生时刻逐人原始表，若任务需要按小时作图，应先说明缺少何种输入。

<a id="chapter-2"></a>

## 第2章开始说明

# 第2章练习包

本包检查Python入口、工作目录、实际依赖和释放表路径，帮助你把一次运行与文件位置对应起来。基础入口只使用标准库，R入口只用基础R。

在解压根目录依次运行。

```text
python scripts/01_environment.py
python scripts/02_release_path.py
Rscript scripts/03_environment.R
```

01报告当前Python和三个后续练习包状态，未安装的包如实标记。02读本包12行构造释放表并写出报告。03记录R版本与最小计算，不要求安装领域包。每个脚本可独立运行，结果写outputs。

想查看某条语句，可以先输入 `2 + 3`，随后用print保存为短脚本。系统终端与Python交互提示符的区别参见正文。填写records.md与exercises.md。

<a id="chapter-3"></a>

## 第3章开始说明

# 第3章练习包

本包保留Lolamicin抗生素与葡萄糖响应胰岛素两项真实实验的完整读取、汇总和作图；释放构造表用于检验任务说明在更换实验后怎样修订。

在解压根目录运行，Python需要requirements.txt中的包。

```text
python scripts/01_read.py
python scripts/02_lolamicin.py
python scripts/03_insulin.py
python scripts/05_release_context.py
```

前三个入口对应3.1-3.3。还可运行 `python run_all.py` 完成相同主例和对比例。outputs保存本人生成图和汇总表。05读取12行构造释放表，只检查新问题的字段与对象，不拟合模型。

scripts/04_column_error.py是主动设置的列名排错练习，按正文和exercises.md单独运行；它不属于正常验收入口。先看真实列名和字典，再修改并重跑。

数据在data/raw，data_dictionary.md解释实验含义，task_template.md与records.md用于保存本人说明。独立任务先预测和作答，再检查实际输出。

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

<a id="chapter-8"></a>

## 第8章开始说明

# 第8章 统计推断与组间比较练习包

本包对应8.1、8.5。用24行ALT/AST教学表计算均值区间与Welch均值差，随后核对70种茶杯分配、10人睡眠配对及A/B汇总。

解压后进入本目录，在终端按顺序运行下面的演示。Python需要pandas、numpy、scipy、matplotlib、scikit-learn、statsmodels；第11章另需seaborn。R脚本所需包见脚本开头。包内数据均可离线读取；安装软件和依赖需要在上课前完成。

```text
python scripts/01_inference.py
Rscript scripts/02_inference.R
```

脚本按自身位置查找输入，可从其他目录调用。所有新结果写入outputs；data/raw保留原输入。先预测关键结果，再运行核对，最后按exercises.md修改一个条件。文件名出现中文时保留UTF-8；CSV输入编码见bundle.json。独立练习没有附完整答案。

正文中的短代码用于逐步讲解，scripts中的文件给出完整演示。记录数据、参数和实际输出，使用records.md整理自己的运行过程。

<a id="chapter-9"></a>

## 第9章开始说明

# 第9章 相关、回归与分类模型练习包

本包对应9.1、9.5。24行表用于散点、分层相关、线性模型和残差；独立200行构造表用于逻辑回归及三个阈值的分类结果。

解压后进入本目录，在终端按顺序运行下面的演示。Python需要pandas、numpy、scipy、matplotlib、scikit-learn、statsmodels；第11章另需seaborn。R脚本所需包见脚本开头。包内数据均可离线读取；安装软件和依赖需要在上课前完成。

```text
python scripts/01_models.py
Rscript scripts/02_models.R
```

脚本按自身位置查找输入，可从其他目录调用。所有新结果写入outputs；data/raw保留原输入。先预测关键结果，再运行核对，最后按exercises.md修改一个条件。文件名出现中文时保留UTF-8；CSV输入编码见bundle.json。独立练习没有附完整答案。

正文中的短代码用于逐步讲解，scripts中的文件给出完整演示。记录数据、参数和实际输出，使用records.md整理自己的运行过程。

<a id="chapter-10"></a>

## 第10章开始说明

# 第10章 模型评估、特征选择与可解释性练习包

本包对应10.1、10.6。160行构造表、共享训练/测试与五折记录用于评估；320行重复测量表用于定位患者跨集合问题。

解压后进入本目录，在终端按顺序运行下面的演示。Python需要pandas、numpy、scipy、matplotlib、scikit-learn、statsmodels；第11章另需seaborn。R脚本所需包见脚本开头。包内数据均可离线读取；安装软件和依赖需要在上课前完成。

```text
python scripts/01_evaluation.py
Rscript scripts/02_evaluation.R
```

脚本按自身位置查找输入，可从其他目录调用。所有新结果写入outputs；data/raw保留原输入。先预测关键结果，再运行核对，最后按exercises.md修改一个条件。文件名出现中文时保留UTF-8；CSV输入编码见bundle.json。独立练习没有附完整答案。

正文中的短代码用于逐步讲解，scripts中的文件给出完整演示。记录数据、参数和实际输出，使用records.md整理自己的运行过程。
