source("database/scrapers/utils.R")

# TODO: should Recovered include Discharged?

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

url <-
  "https://docs.google.com/spreadsheets/d/1jfB4muWkzKTR0daklmf8D5F0Uf_IYAgcx_-Ij9McClQ/edit#gid=0"

raw <-
  googlesheets4::read_sheet(url)

one <-
  raw %>%
  rename_all(
    snakecase::to_snake_case
  ) %>%
  mutate_if(
    is.character,
    stringr::str_to_lower
  ) %>%
  mutate_if(
    is.character,
    stringr::str_squish
  ) %>%
  mutate_if(
    is.character,
    na_if,
    "unspecified"
  ) %>%
  mutate(
    date = lubridate::as_date(date_added),
    country = "japan",
    confirmed = 1
  ) %>%
  select(
    date,
    city = detected_city,
    province = detected_prefecture,
    country,
    status,
    confirmed
  ) %>%
  arrange(
    date
  ) %>%
  drop_na(date)

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
  mutate(
    country = "japan"
  ) %>% 
  # Add confirmed of 0 to rows where we added dates because there were no cases
  replace_na(
    list(confirmed = 0)
  ) %>% 
  arrange(date) 

two %>%
  sample_n(20) %>% # TODO: take out
  # Append to CSV
  attach_lat_long() 

lls <- 
  readr::read_csv(LL_PATH)

three <-
  two %>%
  left_join(
    lls,
    by = c("city", "province", "country")
  )

four <-
  three %>%
  mutate(
    source = url
  ) %>%
  group_by(
    date,
    city,
    province,
    country,
    lat,
    long,
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

out <-
  four %>%
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
