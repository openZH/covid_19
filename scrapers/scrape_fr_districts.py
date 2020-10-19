#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

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
url = 'https://www.fr.ch/de/gesundheit/covid-19/coronavirus-statistik-ueber-die-entwicklungen-im-kanton'
d = sc.download(url, silent=True)
d = d.replace('&nbsp;', ' ')

soup = BeautifulSoup(d, 'html.parser')
table = soup.find(string=re.compile(r'Anzahl positive F.lle nach Bezirk')).find_next('table')
year_re = r'\(\d+\.\d+\.(\d+) bis'
year = soup.find(string=re.compile(year_re))
year = sc.find(year_re, year)

weeks = []
week_regex = re.compile(r'Woche \d+')
head = table.find_all('thead')[0]
headers = table.find_all('th')
for header in headers:
    week = sc.find(r'Woche (\d+)', header.text)
    if week is not None:
        weeks.append(week)

for tr in table.tbody.find_all('tr'):
    tds = tr.find_all('td')

    for i in range(len(weeks)):
        district = tds[0].string
        if district in inhabitants:
            dd = sc.DistrictData(canton='FR', district=district)
            dd.url = url
            dd.week = weeks[i]
            dd.year = '20' + year
            dd.new_cases = tds[i + 1].string
            dd.population = inhabitants[district]
            dd.district_id = district_ids[district]
            print(dd)


# daily data from xls
xls_url = soup.find(href=re.compile("\.xlsx$")).get('href')
assert xls_url, "URL is empty"
if not xls_url.startswith('http'):
    xls_url = f'https://www.fr.ch{xls_url}'

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=8)
for row in rows:
    for district, d_id in district_ids.items():
        assert district_xls[district] in row, f"District '{district}' / {district_xls[district]} not found in row {row}"
        dd = sc.DistrictData(canton='FR', district=district)
        dd.url = url
        dd.date = row['Date'].date().isoformat()
        dd.new_cases = row[district_xls[district]]
        dd.population = inhabitants[district]
        dd.district_id = d_id
        print(dd)
