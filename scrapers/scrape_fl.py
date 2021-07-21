#!/usr/bin/env python3

import scrape_common as sc
import sys
import re
from bs4 import BeautifulSoup


# get the daily bulletin
base_url = 'https://www.regierung.li'
d = sc.download(base_url, silent=True)
soup = BeautifulSoup(d, 'html.parser')

is_first = True
bulletin = soup.find('h1', text=re.compile(r'COVID-19: Situationsbericht.*'))
if bulletin:
    bulletin = bulletin.find_next('a')
if bulletin:
    url = f"{base_url}{bulletin.get('href')}"
    bulletin_d = sc.download(url, silent=True)
    bulletin_soup = BeautifulSoup(bulletin_d, 'html.parser')

    dd = sc.DayData(canton='FL', url=url)

    title = bulletin_soup.find('h1', text=re.compile(r'.*Situationsbericht.*'))
    dd.datetime = sc.find(r'Situationsbericht vom (.*? 20\d{2})', title.text)

    content = title.find_next('div').text
    content = re.sub(r'(\d+)’(\d+)', r'\1\2', content)

    dd.cases = sc.find(r"insgesamt\s+([0-9]+)\s+laborbestätigte\s+Fälle", content)
    dd.deaths = sc.find(r'(Damit\s+traten\s+)?(?:bisher|bislang)\s+(traten\s+)?(?P<death>\d+)\s+(Todesfall|Todesfälle)', content, flags=re.I, group='death')

    if re.search(r'Alle\s+weiteren\s+Erkrankten\s+sind\s+in\s+der\s+Zwischenzeit\s+genesen', content):
        dd.recovered = int(dd.cases) - int(dd.deaths)

    m = re.search(r'(\S+)\s+Erkrankte\s+sind\s+derzeit\s+hospitalisiert', content)
    if m:
        dd.hospitalized = sc.int_or_word(m[1].lower())

    m = re.search(r'Gegenwärtig\s+befinden\s+sich\s+(\w+)\s+enge\s+Kontaktpersonen\s+in\s+Quarantäne.', content)
    if m:
        dd.quarantined = sc.int_or_word(m[1])

    if dd:
        if not is_first:
            print('-' * 10)
        print(dd)
        is_first = False


# get the data from XLS file containing full history
history_url='https://www.llv.li/files/ag/aktuelle-fallzahlen.xlsx'
xls = sc.xlsdownload(history_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
for row in rows:
    dd_full_list = sc.DayData(canton='FL', url=history_url)
    if isinstance(row['Datenstand'], datetime.datetime):
        dd_full_list.datetime = row['Datenstand']
    else:
        dd_full_list.datetime = str(row['Datenstand']).replace(':', '.')
        
    dd_full_list.cases = str(row['Anzahl pos. Fälle']).replace("'","")
    dd_full_list.recovered = row['genesen']
    dd_full_list.hospitalized = row['hospitalisiert']
    dd_full_list.deaths = row['Todesfälle']
    if dd_full_list:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd_full_list)
