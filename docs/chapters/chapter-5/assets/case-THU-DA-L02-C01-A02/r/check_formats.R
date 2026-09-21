options(warn=2)
if (.Platform$OS.type=="windows" && !l10n_info()[["UTF-8"]]) {
  invisible(Sys.setlocale("LC_CTYPE","English_United States.utf8"))
}
script <- sub("^--file=", "", grep("^--file=",commandArgs(),value=TRUE)[1])
base <- dirname(dirname(normalizePath(script)))
if (!requireNamespace("readxl",quietly=TRUE)) stop("readxl missing; Excel exercise not verified")
a <- read.csv(file.path(base,"data/guesses_raw.csv"),colClasses="character",na.strings=NULL,fileEncoding="UTF-8",check.names=FALSE)
b <- read.csv(file.path(base,"data/guesses_gb18030.csv"),colClasses="character",na.strings=NULL,fileEncoding="GB18030",check.names=FALSE)
c <- as.data.frame(readxl::read_excel(file.path(base,"data/guesses.xlsx"),sheet="guesses",col_types="text"))
c[is.na(c)] <- ""
stopifnot(identical(a,b),identical(a,c),nrow(a)==14,ncol(a)==5)
cat("PASS: UTF-8 / GB18030 / Excel, identical 14 x 5 text cells\n")
