#!/usr/bin/env python3

import re
import datetime
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://www.ge.ch/se-faire-vacciner-contre-covid-19/vaccination-chiffres'
d = sc.download(url, silent=True)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

table = soup.find('strong', string=re.compile('VACCINATIONS CONTRE LA COVID-19 PAR SEMAINE')).find_next('table')
trs = table.find_all('tr')
for tr in trs[1:]:
    tds = tr.find_all('td')
    assert len(tds) == 3, f'Expected 3 columns, but got: {tds}'
    date = sc.find(r'(\d+\.\d+[\.-]\d{4})', tds[0].text)
    if not date and sc.find(r'(D.cembre 2020)', tds[0].text):
        # let's use the last day of the year (-6 days, see below)
        date = '2020-12-25'
    # week 2 is '11.01-2021'...
    date = date.replace('-2021', '.2021')
    date = sc.date_from_text(date)
    # this is the start date of the week, let's use the last day
    date = date + datetime.timedelta(days=6)

    vd = sc.VaccinationData(canton='GE', url=url)
    vd.date = date.isoformat()
    vd.total_vaccinations = sc.find(r'^(\d+)\s?', tds[2].text)
    if vd:
        print(vd)
