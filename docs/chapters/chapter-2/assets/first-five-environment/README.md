# 前5章最小环境

用于第2章环境验收和第4-5章配套任务，不替代后续章节专题环境。旧starter-project保留，但不要求在前5章恢复其全部组学依赖。

Python需要pandas；第5章配套图使用matplotlib，Excel练习使用openpyxl。environment.yml给出隔离环境的配置候选；本轮在现有Python3.13环境运行脚本验证，**没有重新创建conda环境或在新电脑验收该配置**。R基础任务不需扩展包；Excel核对另需readxl。

在复制到学生工作空间的本目录运行：

```powershell
python check_python.py
Rscript check_r.R
```

记录真实输出和退出状态。两个脚本只报告状态，不安装软件、不读取原始数据、不自动创建Git仓库。R的readxl为FALSE时，只表示Excel扩展待配置，不阻止CSV核心练习。

选择使用conda时，可以由教师在测试环境评估本目录environment.yml，再让学生创建独立环境；不要覆盖现有同名环境或课程原始配置。任何新增安装均先确认目标环境、来源和网络权限。
