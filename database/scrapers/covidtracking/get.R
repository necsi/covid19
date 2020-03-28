source(here::here("database/scrapers/utils.R"))

base_url <- "https://covidtracking.com/api/"

request <- function(url) {
  resp <-
    httr::GET(url) %>%
    httr::stop_for_status()

  lst <- httr::content(resp)

  lst %>%
    purrr::modify_depth(2, replace_null) %>%
    purrr::map(tibble::as_tibble) %>%
    bind_rows()
}

get <- function(endpoint) {
  url <- elmers("{base_url}{endpoint}")
  request(url)
}

states_current <- get("states")
states_daily <- get("states/daily")
states_info <- get("states/info")
us_current <- get("us")

path_prefix <- "database/scrapers/dat"

current_datetime <-
  lubridate::now() %>%
  stringr::str_replace_all("[ ]", "_") %>%
  stringr::str_replace_all(":", "-")

readr::write_csv(
  states_current,
  elmers("{path_prefix}/{current_datetime}_states_daily.csv")
)
readr::write_csv(
  states_daily,
  elmers("{path_prefix}/{current_datetime}_states_info.csv")
)
readr::write_csv(
  states_info,
  elmers("{path_prefix}/{current_datetime}_states_info.csv")
)
readr::write_csv(
  us_current,
  elmers("../../{current_datetime}_us_current.csv")
)
