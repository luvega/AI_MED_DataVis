# 医药数据处理与可视化在线教材

本仓库发布《医药数据处理与可视化》在线教材站点。内容源来自本地课程教材工作区：

站点内容由配套教材工作区生成并同步，不在公开仓库中记录本机路径或受限材料位置。

站点保持15章原有URL，并只发布面向学生的学习地图、项目模板、课堂任务单和参考规范。课程以AI应用为方法主线，以airway RNA-seq为贯穿案例；相关、回归和分类使用既有医药表格小案例，但执行同一AI核验和可复现交付规范。

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
