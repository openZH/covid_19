# scrape data from BAG-Table with cantonal Corona-case numbers

require(dplyr)
require(rvest)

#URL of the BAG page containing the case numbers
# pg <- read_html('https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html')
pg <- read_html('https://www.bag.admin.ch/bag/en/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html')

#Date
datum <- pg %>%
  html_node(xpath='/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div[5]/article/p[1]/b') %>% 
  html_text() 
  
#Table containing the case numbers
corona_kt <- pg %>% 
    html_node(xpath='/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div[7]/div/div/div/table') %>% 
    html_table()

colnames(corona_kt) <- c("canton","tested_pos","confirmed")
  
# Add date to table 
data <- corona_kt %>% 
        mutate(date=datum) %>% 
        tidyr::separate(date,c("date","time"),sep=",") %>% 
        mutate(date=as.Date(date, format="%d.%m.%Y"),time=gsub(":","",time)) %>% 
        #add Total -> not included on english BAG-page (check if redundant!)
        add_row(canton = "CH", tested_pos = sum(.$tested_pos), confirmed = sum(.$confirmed),date=unique(.$date),time=unique(.$time))

#load timeseries
timeseries <- read.csv("COVID19_Cases_Cantons_CH_total.csv", sep=",") %>%
              mutate(date=as.Date(date)) %>% 
              filter(date!="2020-03-14")

#if date not already available add data
if(!unique(data$date) %in% unique(timeseries$date)){

all <- timeseries %>% 
        bind_rows(data) %>% 
        arrange(canton)

# store as csv
write.csv(all, "COVID19_Cases_Cantons_CH_total.csv",row.names = F)

}







