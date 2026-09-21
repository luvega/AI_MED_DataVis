# 同一CSV与同一筛选规则；基础R，不安装包。
script <- sub("^--file=", "", grep("^--file=", commandArgs(), value=TRUE)[1])
base <- dirname(dirname(normalizePath(script, mustWork=TRUE)))
frame <- read.csv(file.path(base, "data/guesses.csv"), colClasses=c("character","character","integer","numeric"), na.strings="", check.names=FALSE)
missing_columns <- function(frame, required) required[!required %in% names(frame)]
stopifnot(length(missing_columns(frame, c("record_id","participant_id","round","estimate_grains"))) == 0)
keep <- !is.na(frame$estimate_grains) & frame$estimate_grains >= 950
selected <- frame[keep, c("record_id","estimate_grains"), drop=FALSE]
metrics <- data.frame(metric=c("records","participants","missing_estimates","selected_records"),
                      value=c(nrow(frame),length(unique(frame$participant_id)),sum(is.na(frame$estimate_grains)),nrow(selected)))
out <- file.path(base, "results/r")
dir.create(out, recursive=TRUE, showWarnings=FALSE)
write.csv(metrics, file.path(out,"metrics.csv"), row.names=FALSE, na="")
write.csv(selected, file.path(out,"selected.csv"), row.names=FALSE, na="")
print(metrics)
cat("selected IDs:", paste(selected$record_id, collapse=","), "\n")
