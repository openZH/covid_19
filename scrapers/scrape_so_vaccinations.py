#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://corona.so.ch/bevoelkerung/daten/impfstatistik/'
d = sc.download(url, silent=True)
soup = BeautifulSoup(d, 'html.parser')

title = soup.find('h3', string=re.compile(r'^Stand \d+\.')).text
date = sc.find(r'Stand (\d+\.\d+\.20\d{2}),', title)
date = sc.date_from_text(date)

element = soup.find('td', string=re.compile('Anzahl Impfungen \(kumuliert\)'))
element = element.find_next('td')

vd = sc.VaccinationData(canton='SO', url=url)
vd.start_date = date.isoformat()
vd.end_date = date.isoformat()
vd.total_vaccinations = element.text.replace("'", "")
if vd:
    print(vd)
