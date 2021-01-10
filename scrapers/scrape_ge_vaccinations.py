#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://www.ge.ch/se-faire-vacciner-contre-covid-19/vaccination-chiffres'
d = sc.download(url, silent=True)
soup = BeautifulSoup(d, 'html.parser')

table = soup.find('p', string=re.compile('Nombre de vaccinations')).find_next('table')
trs = table.find_all('tr')
assert len(trs) == 3, f'expected 3 rows, but got {len(trs)} ({trs})'

date_row = trs[0].find_all('td')
vaccination_row = trs[2].find_all('td')
assert len(date_row) == len(vaccination_row), f'expected number of elements in dates and vaccinations to be equal! got {len(date_row)} and {len(vaccination_row)}'

# skip the first two columns, the first one is the "title",
# the second one is December 2020, which cannot really be represented properly.
for i in range(2, len(date_row)):
    vd = sc.VaccinationData(canton='GE', url=url)
    date = sc.date_from_text(date_row[i].text)
    vd.date = date.isoformat()
    vd.total_vaccinations = vaccination_row[i].text
    if vd:
        print(vd)
