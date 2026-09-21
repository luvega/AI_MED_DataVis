# 基础R必需；readxl为Excel练习额外依赖。只检查，不安装。
cat("R home:",R.home(),"\n")
cat("version:",R.version.string,"\n")
cat("working directory:",getwd(),"\n")
cat("basic calculation:",2+3,"\n")
cat("readxl for Excel exercise:",requireNamespace("readxl",quietly=TRUE),"\n")
print(sessionInfo())
