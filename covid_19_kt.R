# scrape data from BAG-Table with cantonal Corona-case numbers

require(dplyr)
require(rvest)

options(stringsAsFactors = FALSE)

#URL of the BAG page containing the case numbers
pg <- read_html('https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html')

#Date
datum <- pg %>%
  html_node(xpath='/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div[5]/article/p[2]/b') %>% 
  html_text() %>% 
  
  
#Table containing the case numbers
corona_kt <- pg %>% 
    html_node(xpath='/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div[7]/div/div/div/table') %>% 
    html_table()
  
# Add date to table
data <- corona_kt %>% mutate(datum=datum)

# store as csv
write.csv(data, "covid19_kt.csv")

