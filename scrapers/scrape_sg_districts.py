#!/usr/bin/env python3

import re
import datetime
from bs4 import BeautifulSoup
import scrape_common as sc

inhabitants = {
    'St.Gallen': 127198,
    'Rohrschach': 44110,
    'Rheintal': 74580,
    'Werdenberg': 40239,
    'Sarganserland': 41736,
    'See Gaster': 76913,
    'Toggenburg': 47272,
    'Wil': 77018,
}

url = 'https://www.sg.ch/tools/informationen-coronavirus.html'
d = sc.download(url, silent=True)
soup = BeautifulSoup(d, 'html.parser')

table = soup.find(string=re.compile(r'Fallzahlen Regionen des Kantons St.Gallen')).find_next('table')
header = table.find_next('th').text
date = sc.find(r'gemeldete F.lle Stand (\d+\.\d+\.20\d{2})', header)
date = sc.date_from_text(date)

for row in table.find_all('tr'):
    columns = row.find_all('td')
    if len(columns) > 0:
        district = sc.find(r'Wahlkreis (.*)$', columns[0].text)
        if district is not None:
            dd = sc.DistrictData(canton='SG', district=district)
            dd.url = url
            dd.date = date.isoformat()
            dd.new_cases = columns[1].text
            if district in inhabitants:
                dd.population = inhabitants[district]
            print(dd)
