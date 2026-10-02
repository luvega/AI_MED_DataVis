# 喷发时长与下一次等待

素材ID：THU-DA-L06-C04-A01。清华课程只用于发现教学问题；图形和计算由本包数据重新生成。

## 来源与许可

R 4.6.0 datasets::faithful，272条连续观测，非独立随机抽取的全球喷泉样本。随R datasets分发，GPL-2 | GPL-3。部分喷发时长有取整。

外部依据：[原始说明或方法来源](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/faithful.html)。访问核验：2026-09-20。数据与脚本不可被解释为对课程中所有历史叙述的背书。

## 数据字典与处理

eruptions：喷发持续分钟；waiting：到下一次喷发的等待分钟。无缺失，不分组拟合，不把视觉双峰当作已确认潜在类别。

输入为data/faithful.csv。保留原输入，不自动删除极端观察。R和Python读取同一CSV；不调用随机过程。

## 运行与结果

在本包目录运行：

```text
python python/analyze.py
Rscript r/analyze.R
```

脚本使用文件所在位置定位数据，亦可从其他目录调用。Python需要numpy、pandas、scipy、matplotlib；R仅使用随R分发的包。Python图形写入figures/result-python.png和.svg；R图形写入figures/result-r.png。关键结果各写入expected/python.csv和expected/r.csv，比较绝对误差不超过1e-8（概率与系数），计数须完全一致。expected供结果核对，不替代学生报告。

## 解释边界

课堂任务应同时报告观察单位、输入行数与人数、变量单位、方法和限制。观察关联不是因果；样本内拟合不是外部预测性能。历史药物记录不支持现代临床建议，教学重建数不支持任何真实社会或医学结论。
