#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

url = "https://corona.so.ch/spezialseiten/die-covid-19-kennzahlen-im-ueberblick/"
d = sc.download(url, silent=True)

soup = BeautifulSoup(d, 'html.parser')
first_column = soup.find(text=re.compile(r'Stand: \d+\.'))
date = sc.find(r'Stand: (\d+\. .* 20\d{2})', first_column)
date = sc.date_from_text(date)

tbody = first_column.find_previous('tbody')

population = {
    'Solothurn': 16933,
    'Bucheggberg': 7954,
    'Dorneck': 20678,
    'Gäu': 21605,
    'Gösgen': 24536,
    'Lebern': 24536,
    'Olten': 55686,
    'Thal': 14785,
    'Thierstein': 14747,
    'Wasseramt': 52134,
}

district_ids = {
    'Solothurn': 1109,
    'Bucheggberg': 1103,
    'Dorneck': 1104,
    'Gäu': 1101,
    'Gösgen': 1105,
    'Lebern': 1107,
    'Olten': 1108,
    'Thal': 1102,
    'Thierstein': 1110,
    'Wasseramt': 1106,
}

print(sc.DistrictData.header())

for row in tbody.find_all('tr'):
    columns = row.find_all('td')
    if len(columns) == 3:
        district = columns[0].text
        if district in district_ids:
            dd = sc.DistrictData(canton='SO', district=district)
            dd.url = url
            dd.date = date.isoformat()
            dd.population = population[district]
            dd.district_id = district_ids[district]
            dd.total_cases = columns[1].text
            dd.new_cases = columns[2].text
            print(dd)
