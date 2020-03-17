library(gestalt)

elmers <- glue::glue %>>>% as.character

write_or_append <- function(tbl, path) {
  if (!fs::file_exists(path)) {
    readr::write_csv(tbl, path)
  } else {
    readr::write_csv(tbl, path, append = TRUE)
  }
}