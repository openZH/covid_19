#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://www.gef.be.ch/gef/de/index/Corona/Corona/corona_impfung_bern.html'
d = sc.download(url, silent=True)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

table = soup.find('h2', string=re.compile('Durchgef.hrte Impfungen im Kanton Bern')).find_next('table')
tbody = table.find_all('tbody')[0]
trs = tbody.find_all('tr')

for tr in trs:
    tds = tr.find_all('td')
    assert len(tds) == 3, f'expected 3 rows, but got {len(tds)} ({tds})'

    vd = sc.VaccinationData(canton='BE', url=url)
    date = sc.find(r'(\d+\.\d+\.\d{4})', tds[0].text)
    date = sc.date_from_text(date)
    vd.date = date.isoformat()
    vd.total_vaccinations = sc.find(r'(\d+)\s?', tds[1].text)
    vd.vaccinated_people = sc.find(r'(\d+)\s?', tds[2].text)
    if vd:
        print(vd)
