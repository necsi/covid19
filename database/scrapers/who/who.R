library(bonanza)

url <- "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"

sess <- 
  browse.launch_session(url)

pg <- 
  sess %>% 
  browse.extract_html()

link_names <- 
  pg %>% 
  rvest::html_nodes("strong") %>% 
  rvest::html_text() %>% 
  .[stringr::str_detect(., "Situation report")]

links <- 
  pg %>% 
  rvest::html_nodes("a") %>% 
  rvest::html_attr("href") %>% 
  .[stringr::str_detect(., "situation-reports")] %>% 
  unique()

link_tbl <- 
  tibble(
    link_suffix = links,
    link = 
      dev.glue(
        "https://www.who.int{link_suffix}"
      )
  ) %>% 
  mutate(
    report_num = 
      link %>% 
      stringr::str_extract("sitrep-[0-9]+") %>% 
      stringr::str_remove("sitrep-")
  )

grab_data <- function(tbl) {
  out <- tibble() 
  
  for (i in 1:nrow(tbl)) {
    dev.glue_message("Scraping report {tbl$report_num[i]}.")
    
    countries_territories_raw <- 
      tbl$link[i] %>% 
      pdftools::pdf_text() %>% 
      .[2] %>% 
      wrangle.clean_html()
    
    countries_territories_raw <- 
      tbl$link[i] %>% 
      pdftools::pdf_text() %>% 
      .[3]
    
  }
  
  out
}