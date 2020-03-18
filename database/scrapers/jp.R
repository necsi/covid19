source(here::here("database/scrapers/utils.R"))

todays_date <- lubridate::today()

OUT_PATH <- here(elmers("database/scrapers/dat/jp/{todays_date}.csv"))

cols <-
  c(
    "date",
    "city",
    "province",
    "country",
    "location",
    "confirmed",
    "recovered",
    "unspecified",
    "hospitalized",
    "discharged",
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
    country = "japan"
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
  arrange(date,
          province, 
          city) 

two %>%
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
    source = url,
    status = 
      case_when(
        is.na(status) ~ "unspecified",
        TRUE ~ status
      ),
    location = elmers("{lat},{long}")
  ) %>%
  group_by(
    date,
    city,
    province,
    country,
    location,
    status,
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
      hospitalized = 0,
      discharged = 0,
      dead = 0
    )
  ) %>% 
  rowwise() %>% 
  mutate(
    confirmed = 
      sum(
        recovered, unspecified, hospitalized, discharged, dead, 
        na.rm = TRUE)
  ) %>% 
  ungroup()

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

readr::write_csv(out, OUT_PATH)
