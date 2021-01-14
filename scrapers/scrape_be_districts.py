#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


# https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/karten.assetdetail.5688189.html
district_ids = {
    'Jura bernois': 241,
    'Biel/Bienne': 242,
    'Seeland': 243,
    'Oberaargau': 244,
    'Emmental': 245,
    'Bern-Mittelland': 246,
    'Thun': 247,
    'Obersimmental-Saanen': 248,
    'Frutigen-Niedersimmental': 249,
    'Interlaken-Oberhasli': 250,
}

# https://www.jgk.be.ch/jgk/de/index/gemeinden/gemeinden/gemeindedaten.assetref/dam/documents/JGK/AGR/de/Gemeinden/Gemeindedaten/agr_gemeinden_gemeindedaten_karte_verwaltungskreise_verwaltungsregionen_de.pdf
inhabitants = {
    'Jura bernois': 53721,
    'Biel/Bienne': 101313,
    'Seeland': 74467,
    'Oberaargau': 81759,
    'Emmental': 97218,
    'Bern-Mittelland': 414658,
    'Thun': 107491,
    'Obersimmental-Saanen': 16588,
    'Frutigen-Niedersimmental': 40375,
    'Interlaken-Oberhasli': 47387,
}


# start getting and parsing the data
html_url = 'https://www.besondere-lage.sites.be.ch/de/start/news/fallzahlen.html'
d = sc.download(html_url, silent=True)
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')
caption = soup.find('caption', string=re.compile('Fallzahlen nach Verwaltungskreisen'))
table = caption.find_parent('table')
trs = table.find_all('tr')
weeks = []
year = None
years = []
for th in trs[0].find_all('th'):
    week = sc.find(r'Kalenderwoche (\d+)', th.text)
    if week:
        weeks.append(week)
    year = sc.find(r'\d+\.\d+\.(\d+)', th.text)
    if year:
        if len(year) == 2:
            year = f'20{year}'
        years.append(year)

assert len(weeks) == len(years), f'expected weeks ({weeks}) to have the same size as the years ({years})'

tbody = table.find_next('tbody')
for tr in trs[1:]:
    tds = tr.find_all('td')
    assert len(tds) == len(weeks), f'expected {len(weeks) + 1} items, but got {len(tds)}'
    ths = tr.find_all('th')
    district = ths[0].text
    if district == 'Unbekannt':
        continue
    assert district in district_ids, f'district "{district}" not found in {district_ids}!'

    for i in range(len(week)):
        dd = sc.DistrictData(district=district, canton='BE')
        dd.url = html_url
        dd.district_id = district_ids[district]
        dd.population = inhabitants[district]
        dd.week = weeks[i]
        dd.year = years[i]
        dd.new_cases = tds[i].text.replace("'", "")
        print(dd)
