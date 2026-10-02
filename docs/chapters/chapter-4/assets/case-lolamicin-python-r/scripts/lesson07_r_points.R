# 第七课：复用第六课生成的R结果，修改时间后先重新运行lesson06_compare.R。
selected <- read.csv("outputs/r_selected.csv", fileEncoding = "UTF-8",
                     stringsAsFactors = FALSE, check.names = FALSE)
target_time <- unique(selected$time_h)
stopifnot(length(target_time) == 1, nrow(selected) == 3,
          all(selected$unit == "CFU/mL"), all(is.finite(selected$value)))

png("outputs/r_selected_points.png", width = 1000, height = 700, res = 150)
par(mar = c(4.5, 5, 4, 1))
plot(seq_len(nrow(selected)), selected$value,
     xaxt = "n", pch = 19, col = "#0072B2", cex = 1.2,
     ylim = c(0, max(selected$value) * 1.5),
     xlab = "Source cell", ylab = "CFU/mL",
     main = paste("Lolamicin 4X MIC:", target_time, "h"))
axis(1, at = seq_len(nrow(selected)), labels = selected$source_cell)
abline(h = mean(selected$value), col = "#D55E00", lwd = 2)
legend("topright", legend = c("Source values", "Arithmetic mean"),
       col = c("#0072B2", "#D55E00"), pch = c(19, NA),
       lty = c(NA, 1), bty = "n")
dev.off()
cat("Saved a single-time source-point plot; no error bars.\n")
