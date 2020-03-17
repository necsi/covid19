source("database/scrapers/keys.R")
library(dplyr)
library(gestalt)
library(ggmap)
library(googlesheets4)
library(here)
library(magrittr)
library(tidyr)

# Specify function names from packages that should take precedence in name conflicts
conflicted::conflict_prefer("dplyr", "filter")
conflicted::conflict_prefer("dplyr", "lag")

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

# Store a dataframe of city, province, country and the associated lat long
attach_lat_long <- function(tbl, path = here("database/scrapers/lat_longs.csv")) {
  # Set up Google Maps key
  register_google(gmaps_key)
  
  tbl %<>% 
    select(
      city, province, country
    ) %>% 
    mutate_all(
      stringr::str_to_lower
    ) %>%
    mutate_all(
      stringr::str_squish
    ) %>% 
    mutate_if(
      is.character,
      na_if,
      "unspecified"
    ) %>% 
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
        list(geocode(location))
    ) %>% 
    unnest(ll) %>% 
    rename(
      long = lon
    ) %>% 
    na_if("")
    
  write_or_append(lat_longs, path)
}
