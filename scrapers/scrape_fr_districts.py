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

url = 'https://www.fr.ch/de/gesundheit/covid-19/coronavirus-statistik-ueber-die-entwicklungen-im-kanton'
d = sc.download(url, silent=True)

soup = BeautifulSoup(d, 'html.parser')
table = soup.find(string=re.compile(r'Anzahl der positiven Fälle nach Bezirk')).find_next('table')

weeks = []
week_regex = re.compile(r'Woche \d+')
week = table.find(string=week_regex)
for i in range(3):
    weeks.append(sc.find(r'Woche (\d+)', week))
    week = week.find_next(string=week_regex)


for tr in table.tbody.find_all('tr'):
    tds = tr.find_all('td')

    for i in range(3):
        district = tds[0].string
        dd = sc.DistrictData(canton='FR', district=district)
        dd.url = url
        dd.week = weeks[i]
        dd.new_cases = tds[i + 1].string
        if district in inhabitants:
            dd.population = inhabitants[district]
        print(dd)
