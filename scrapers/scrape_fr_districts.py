#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from io import StringIO
import re
from bs4 import BeautifulSoup
import scrape_common as sc
from scrape_fr_common import get_fr_csv

inhabitants = {
    'Broye': 32894,
    'Glane': 24337,
    'Greyerz': 55726,
    'Saane': 106136,
    'See': 36800,
    'Sense': 43990,
    'Vivisbach': 18831,
}

district_ids = {
    'Broye': 1001,
    'Glane': 1002,
    'Greyerz': 1003,
    'Saane': 1004,
    'See': 1005,
    'Sense': 1006,
    'Vivisbach': 1007,
}

district_xls = {
    'Broye': 'Broye',
    'Glane': 'Glâne',
    'Greyerz': 'Gruyère',
    'Saane': 'Sarine',
    'See': 'Lac',
    'Sense': 'Singine',
    'Vivisbach': 'Veveyse',
}

# weekly data
url = 'https://www.fr.ch/de/gesundheit/covid-19/coronavirus-statistik-ueber-die-entwicklung-im-kanton'
d = sc.download(url, silent=True)
d = d.replace('&nbsp;', ' ')

soup = BeautifulSoup(d, 'html.parser')
table = soup.find(string=re.compile(r'Anzahl positive F.lle nach Bezirk')).find_next('table')

weeks = []
years = []
week_regex = re.compile(r'Woche \d+')
trs = table.find_all('tr')
for header in trs[0]:
    week = sc.find(r'Woche (\d+)', header.string)
    if week is not None:
        weeks.append(week)
        years.append('2021')

for tr in trs[1:]:
    tds = tr.find_all('td')

    for i in range(len(weeks)):
        district = tds[0].string
        if district in inhabitants:
            dd = sc.DistrictData(canton='FR', district=district)
            dd.url = url
            dd.week = weeks[i]
            # TODO restore once all weeks are in 2021
            # dd.year = '20' + year
            dd.year = years[i]
            dd.new_cases = tds[i + 1].string
            dd.population = inhabitants[district]
            dd.district_id = district_ids[district]
            print(dd)


# daily data from csv
csv_url, csv_data, main_url = get_fr_csv()
reader = csv.DictReader(StringIO(csv_data), delimiter=';')

for row in reader:
    row_date = row['Date']
    row_date = sc.date_from_text(row_date)
    for district, d_id in district_ids.items():
        for key, val in row.items():
            if sc.find(r'.*(' + district + ').*', key):
                dd = sc.DistrictData(canton='FR', district=district)
                dd.url = url
                dd.date = row_date.isoformat()
                dd.new_cases = val
                dd.population = inhabitants[district]
                dd.district_id = d_id
                print(dd)
