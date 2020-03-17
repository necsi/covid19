source("database/scrapers/keys.R")
library(ggmap)
library(googlesheets4)
library(dplyr)
library(tidyr)

# TODO: should Recovered include Discharged?

# Specify function names from packages that should take precedence in name conflicts
conflicted::conflict_prefer("dplyr", "filter")
conflicted::conflict_prefer("dplyr", "lag")

cols <- 
  c(
    "date",
    "city",
    "province",
    "country",
    "lat",
    "long",
    "confirmed",
    "recovered",
    "dead",
    "daily_diff_confirm",
    "daily_diff_recover",
    "daily_diff_dead",
    "source"
  )

na_to_zero <- function(x) {
  if (is.na(x)) 0
  else x
}

url <- 
  "https://docs.google.com/spreadsheets/d/1jfB4muWkzKTR0daklmf8D5F0Uf_IYAgcx_-Ij9McClQ/edit#gid=0"

raw <- 
  googlesheets4::read_sheet(url)

one <- 
  raw %>% 
  rename_all(
    snakecase::to_snake_case
  ) %>% 
  mutate(
    date = lubridate::as_date(date_added),
    country = "japan",
  ) %>% 
  select(
    date,
    city = detected_city,
    province = detected_prefecture,
    country,
    status
  ) %>% 
  arrange(
    date
  ) %>% 
  drop_na(date)


# Set up Google Maps key
register_google(gmaps_key)

lat_longs <- 
  one %>% 
  distinct(
    city, province, country
  ) %>% 
  replace_na(
    list(
      city = "",
      province = ""
    )
  ) %>% 
  mutate(
    location = elmers("{city} {province} {country}") %>% 
      stringr::str_squish(),
    ll = 
      list(geocode(location))
  ) 

write_or_append(lat_longs)


# Dataframe with one row for every date from the first to last date in the sheet
all_days_df <- 
  tibble(
    date = 
      one$date[1]:one$date[nrow(one)] %>% 
      lubridate::as_date()
  )

two <- 
    one %>% 
    # Get a row for all dates even if they don't appear in sheet
    full_join(
      all_days_df,
      by = "date"
    ) %>% 
    arrange(date) %>% 
    mutate(
      confirmed = 1,
      source = url
    ) %>% 
    replace_na(
      list(
        city = "Unspecified",
        status = "Unspecified",
        province = "Unspecified"
      )
    ) %>% 
  group_by(
    date,
    city,
    province,
    country,
    status,
    confirmed,
    source
  ) %>% 
  count() %>% 
    ungroup() %>% 
  pivot_wider(
    names_from = status,
    values_from = n
  ) %>% 
    rename_all(
      snakecase::to_snake_case
    ) %>% 
    rename(
      dead = deceased
    ) %>% 
  replace_na(
    list(
      recovered = 0,
      unspecified = 0,
      dead = 0
    )
  )

three <- 
  two %>% 
  mutate(
    lag_date = lag(date),
    daily_diff_confirm = 
      confirmed - lag(confirmed),
    daily_diff_recover = 
      recovered - lag(recovered),
    daily_diff_dead =
      dead - lag(dead)
  ) %>% 
  select(cols)
