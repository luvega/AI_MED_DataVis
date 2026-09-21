required_packages <- c("dplyr", "tidyr", "ggplot2")

project_root <- normalizePath(getwd(), winslash = "/", mustWork = FALSE)
output_dir <- file.path(project_root, "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
output_path <- file.path(output_dir, "r-smoke-test.txt")

package_lines <- vapply(
  required_packages,
  function(package) {
    if (!requireNamespace(package, quietly = TRUE)) {
      paste0("package_", package, "=missing")
    } else {
      paste0("package_", package, "=", as.character(packageVersion(package)))
    }
  },
  character(1)
)

lines <- c(
  "status=environment_checked",
  paste0("r_home=", normalizePath(R.home(), winslash = "/", mustWork = FALSE)),
  paste0("r_version=", R.version.string),
  paste0("working_directory=", project_root),
  paste0("library_paths=", paste(.libPaths(), collapse = ";")),
  package_lines,
  paste0("output_file=", normalizePath(output_path, winslash = "/", mustWork = FALSE))
)

writeLines(lines, output_path, useBytes = TRUE)
cat(paste(lines, collapse = "\n"), "\n")
cat("session_info_begin\n")
print(sessionInfo())
cat("session_info_end\n")

if (any(grepl("=missing$", package_lines))) {
  cat("result=needs_configuration\n")
  quit(status = 1)
}

cat("result=pass\n")
