source("database/scrapers/keys.R")
library(dplyr)
library(gestalt)
library(ggmap)
library(googlesheets4)
library(here)
library(magrittr)
library(tidyr)

LL_PATH <- here("database/scrapers/lat_longs.csv")

# Specify function names from packages that should take precedence in name conflicts
filter <- dplyr::filter
lag <- dplyr::lag

register_google(gmaps_key)

elmers <- glue::glue %>>>% as.character

na_to_zero <- function(x) {
  if (is.na(x)) 0
  else x
}

write_or_append <- function(tbl, path) {
  if (!fs::file_exists(path)) {
    readr::write_csv(tbl, path)
  } else {
    readr::write_csv(tbl, path, append = TRUE)
  }
}

try_geocode <- purrr::possibly(geocode, 
                               otherwise = 
                                 tibble(long = NA_real_,
                                        lat = NA_real_)
                               )

# Store a dataframe of city, province, country and the associated lat long
attach_lat_long <- function(tbl, path = LL_PATH) {
  # Set up Google Maps key
  register_google(gmaps_key)
  
  tbl %<>% 
    distinct(
      city, province, country
    )
  
  if (fs::file_exists(path)) {
    existing_lls <- readr::read_csv(path)
    
    tbl %<>% 
      anti_join(
        existing_lls,
        by = c("city", "province", "country")
      )
  }
  
  lat_longs <- 
    tbl %>% 
    replace_na(
      list(
        city = "",
        province = "",
        country = ""
      )
    ) %>% 
    mutate(
      location = elmers("{city} {province} {country}") %>% 
        stringr::str_squish()
    ) %>% 
    rowwise() %>% 
    mutate(
      ll = 
        list(try_geocode(location))
    ) %>% 
    unnest(ll) %>% 
    rename(
      long = lon
    ) %>% 
    na_if("")
    
  write_or_append(lat_longs, path)
  
  lat_longs
}
