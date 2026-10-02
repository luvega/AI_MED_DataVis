# 第六课：从练习目录运行；先读懂，再修改target_time。
values <- c(6000, 18000, 51000)
print(values[1])
print(length(values))
print(mean(values))

table <- read.csv("data/raw/lolamicin_2_8h.csv", fileEncoding = "UTF-8",
                  stringsAsFactors = FALSE, check.names = FALSE)
target_time <- 8
keep <- table$time_h == target_time
selected <- table[keep, ]
print(selected$source_cell)
print(selected$value)
print(mean(selected$value))

# 保留时间、单位与来源字段；不把R行号写成新的实验字段。
dir.create("outputs", showWarnings = FALSE)
write.csv(selected, "outputs/r_selected.csv", row.names = FALSE,
          fileEncoding = "UTF-8")
