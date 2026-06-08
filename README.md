# 医药数据处理与可视化在线教材

本仓库发布《医药数据处理与可视化》在线教材站点。内容源来自本地课程教材工作区：

`E:\Codex_Projects\AI_MED_DataVis_Book`

## 本地构建

```powershell
python -m pip install -r requirements.txt
$env:PYTHONUTF8='1'
python scripts/generate_site.py
python scripts/validate_site_sources.py
python -m mkdocs build --strict
python -m mkdocs serve -a 127.0.0.1:8000
```

## 发布

推送 `main` 后，`.github/workflows/pages.yml` 会构建 MkDocs 站点并部署到 GitHub Pages。

公开地址：

https://luvega.github.io/AI_MED_DataVis/
