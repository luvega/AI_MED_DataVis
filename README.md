# 医药数据处理与可视化在线教材

本仓库发布《医药数据处理与可视化》在线教材站点。内容源来自本地课程教材工作区：

站点内容由配套教材工作区生成并同步，不在公开仓库中记录本机路径或受限材料位置。

站点保持15章原有URL，发布学生正文、学习地图、项目模板、课堂任务单、参考规范和经解压运行核验的章级练习包。猜糖豆与Lolamicin连接前期表格操作，airway集中用于第12章RNA-seq。练习包登记版本、文件清单与校验值；未登记ZIP和教师资料不进入网站。

逐批发布时使用 `python scripts/generate_site.py --chapters 4,5,6,7`，只更新已核验章节，保留其余章节的已发布版本。完整生成仍使用原命令。下载索引在 `docs/teaching/chapter-practice.md`，固定下载地址为 `downloads/chapter-NN-practice.zip`。

## 本地构建

```powershell
python -m pip install -r requirements.txt
$env:PYTHONUTF8='1'
python scripts/generate_site.py
python scripts/validate_site_sources.py
python -m mkdocs build --strict
python -m mkdocs serve -a 127.0.0.1:8000
```

生成和校验会拒绝受限压缩包、日志、私有地址、本机用户路径、令牌样式文本及旧的并行课程路线用语。公开部署前仍须人工确认凭据已经轮换，并完成拟公开图片的授权审阅。

## 发布

推送 `main` 后，`.github/workflows/pages.yml` 会构建 MkDocs 站点并部署到 GitHub Pages。

公开地址：

https://luvega.github.io/AI_MED_DataVis/
