# 第2章学生环境包

本目录提供 2026-09-07 课程环境基线。把整个目录复制到独立课程工作空间的根目录，再按本页顺序创建环境、安装课程额外包并运行验收脚本。不要把环境安装到教材编写仓库，也不要自行升级锁定版本。

## 文件用途

- `environment.yml`：第4-13章通用 Python 环境，包含表格处理、统计、建模、绘图和基础化学信息练习所需的 conda 包。
- `scripts/install_python_course_extras.py`：从官方 PyPI 安装 `ISLP` 与 `pysradb` 的课程固定版本。课程使用 `ISLP` 的内置数据和聚类辅助功能，因此不安装其未在本书使用的深度学习依赖。
- `DESCRIPTION` 与 `renv.lock`：第4-12章通用 R/Bioconductor 环境，包含数据整理、绘图、统计建模及 `airway`/DESeq2 案例所需包。
- `scripts/check_python_environment.py`：报告 Python 实际解释器、版本、工作目录和基础包，并生成 `outputs/python-smoke-test.txt`。
- `scripts/check_r_environment.R`：报告 R 主目录、版本、包库、基础包和会话信息，并生成 `outputs/r-smoke-test.txt`。
- `环境分层说明.md`：说明通用环境与第11、14、15章专用环境的边界。

## Python 环境

在本目录运行：

```powershell
conda env create --file environment.yml
conda activate medical-data-course
python scripts/install_python_course_extras.py
python scripts/check_python_environment.py
```

验收时还要运行下面的命令，核对当前终端调用的实际解释器：

```powershell
python -c "import sys; print(sys.executable); print(sys.version)"
```

## R 环境

先确认 `Rscript --version` 可运行，再在本目录执行：

```powershell
Rscript -e "if (!requireNamespace('renv', quietly = TRUE)) install.packages('renv', repos = 'https://cloud.r-project.org')"
Rscript -e "renv::restore()"
Rscript scripts/check_r_environment.R
```

`renv::restore()` 依据锁文件建立项目包库，不要求学生在全局包库中逐个安装或升级课程包。

## 适用边界

两份验收脚本都不会安装、更新或删除软件和包，也不会读取或修改 `data/raw/`。缺少基础包时，脚本返回非零状态并写出 `missing`，用于把该项记为“待配置”。额外包安装脚本会访问网络并写入当前已激活的 Python 环境，运行前应确认环境名和解释器路径。

本环境已在当前 Windows 主机的独立目录完成从文件创建与功能验证，但尚未在另一台全新电脑上验证。它记录的是课程发布基线，不代表长期推荐版本，也不能保证不同操作系统得到逐位相同的数值。第11章旧版聚类交叉表、第14章 Seurat 和第15章空间/免疫组库案例使用各自的专用环境，不应强行并入本通用环境。
