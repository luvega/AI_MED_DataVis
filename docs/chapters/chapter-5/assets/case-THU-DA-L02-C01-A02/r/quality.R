# 基础R；输入、规则、保留顺序与Python一致。
options(warn=2)
if (.Platform$OS.type=="windows" && !l10n_info()[["UTF-8"]]) {
  invisible(Sys.setlocale("LC_CTYPE","English_United States.utf8"))
}
script <- sub("^--file=", "", grep("^--file=", commandArgs(), value=TRUE)[1])
base <- dirname(dirname(normalizePath(script, mustWork=TRUE)))
args <- commandArgs(trailingOnly=TRUE)
source <- if (length(args)>=1) args[1] else file.path(base,"data/guesses_raw.csv")
out <- if (length(args)>=2) args[2] else file.path(base,"results/r")
columns <- c("record_id","participant_id","round","estimate","unit")
frame <- read.csv(source, colClasses="character", na.strings=NULL, fileEncoding="UTF-8", check.names=FALSE, blank.lines.skip=FALSE)
if (!identical(names(frame),columns)) stop("Expected exact column names and order")
if (anyNA(frame) || any(frame$record_id=="") || any(frame$participant_id=="") || any(!frame$round %in% c("1","2"))) stop("Missing ID or invalid round; stop for review")
for (rid in unique(frame$record_id)) {
  block <- frame[frame$record_id==rid,,drop=FALSE]
  if (nrow(unique(block))>1) stop(paste("Conflicting record_id:",rid))
}
dup <- duplicated(frame)
issues <- data.frame(source_row=which(dup),record_id=frame$record_id[dup],
                     issue=rep("duplicate_export",sum(dup)),action=rep("drop_duplicate_copy",sum(dup)))
source_rows <- which(!dup)
unique_frame <- frame[!dup,,drop=FALSE]
result <- data.frame(record_id=character(),participant_id=character(),round=integer(),estimate_grains=numeric(),review_high=character())
quarantine <- unique_frame[FALSE,,drop=FALSE]
quarantine$reason <- character()
for (j in seq_len(nrow(unique_frame))) {
  row <- unique_frame[j,,drop=FALSE]
  issue <- ""
  if (row$estimate=="") {
    issue <- "missing_estimate"
  } else if (!grepl("^[+-]?([0-9]+(\\.[0-9]*)?|\\.[0-9]+)$",row$estimate)) {
    issue <- "non_numeric"
  } else if (!row$unit %in% c("粒","千粒")) {
    issue <- "unknown_unit"
  } else {
    value <- as.numeric(row$estimate) * if (row$unit=="千粒") 1000 else 1
    if (value<0) issue <- "negative_estimate"
  }
  if (nzchar(issue)) {
    issues <- rbind(issues,data.frame(source_row=source_rows[j],record_id=row$record_id,issue=issue,action="quarantine"))
    row$reason <- issue
    quarantine <- rbind(quarantine,row)
    next
  }
  high <- value>5000
  if (high) issues <- rbind(issues,data.frame(source_row=source_rows[j],record_id=row$record_id,issue="high_review",action="retain_flag"))
  result <- rbind(result,data.frame(record_id=row$record_id,participant_id=row$participant_id,round=as.integer(row$round),estimate_grains=value,review_high=if (high) "TRUE" else "FALSE"))
}
flow <- data.frame(stage=c("raw","deduplicated","eligible"),
                  records=c(nrow(frame),nrow(unique_frame),nrow(result)),
                  participants=c(length(unique(frame$participant_id)),length(unique(unique_frame$participant_id)),length(unique(result$participant_id))))
dir.create(out,recursive=TRUE,showWarnings=FALSE)
for (name in c("clean","issues","quarantine","flow")) {
  object <- switch(name,clean=result,issues=issues,quarantine=quarantine,flow=flow)
  write.csv(object,file.path(out,paste0(name,".csv")),row.names=FALSE,na="",fileEncoding="UTF-8")
}
draw <- function() {
  mids <- barplot(flow$records,names.arg=flow$stage,col=c("#8a949d","#5c8a99","#276675"),
                  ylim=c(0,16),ylab="Number of records",main="Teaching data: processing stages",border=NA)
  text(mids,flow$records+0.6,labels=flow$records)
}
png(file.path(out,"quality-flow.png"),width=1024,height=576,res=160)
draw()
dev.off()
svg(file.path(out,"quality-flow.svg"),width=6.4,height=3.6)
draw()
dev.off()
print(flow)
