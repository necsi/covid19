library(googlesheets4)
library(dplyr)
library(tidyr)

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

url <- 
  "https://docs.google.com/spreadsheets/d/1jfB4muWkzKTR0daklmf8D5F0Uf_IYAgcx_-Ij9McClQ/edit#gid=0"

raw <- 
  googlesheets4::read_sheet(url)

na_to_zero <- function(x) {
  if (is.na(x)) 0
  else x
}

clean <- 
  raw %>% 
  rename_all(
    snakecase::to_snake_case
  ) %>% 
  mutate(
    date = lubridate::as_date(date_added),
    country = "japan",
    confirmed = 1,
    source = url
  ) %>% 
  replace_na(
    list(
      detected_city = "Unspecified",
      status = "Unspecified"
    )
  ) %>% 
  select(
    date,
    city = detected_city,
    province = detected_prefecture,
    country,
    status,
    source
  )


(out <- 
  clean %>% 
  arrange(
    date
  ) %>% 
  group_by(
    date,
    province,
    country,
    status,
    confirmed,
    source
  ) %>% 
  count() %>% 
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
    ungroup() %>% 
    mutate_all(na_to_zero) %>% 
)
