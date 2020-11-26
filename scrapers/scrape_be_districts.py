#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
html_url = 'https://www.besondere-lage.sites.be.ch/besondere-lage_sites/de/index/corona/index.html'
d = sc.download(html_url, silent=True)
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')
table = soup.find('table', {'summary': 'COVID-19 Fallzahlen nach Verwaltungskreis'})
thead = table.find_next('thead')
weeks = []
year = None
for th in thead.find_all('th'):
    week = sc.find(r'KW (\d+)', th.text)
    if week:
        weeks.append(week)
    year = sc.find(r'\d+\.\d+\.(\d+)', th.text)
if len(year) == 2:
    year = f'20{year}'

tbody = table.find_next('tbody')
for tr in tbody.find_all('tr'):
    tds = tr.find_all('td')
    assert len(tds) == len(weeks) + 1, f'expected {len(weeks) + 1} items, but got {len(tds)}'
    district = tds[0].text
    assert district in district_ids, f'district "{district}" not found in {district_ids}!'

    for i in range(len(week)):
        dd = sc.DistrictData(district=district, canton='BE')
        dd.url = html_url
        dd.district_id = district_ids[district]
        dd.population = inhabitants[district]
        dd.week = weeks[i]
        dd.year = year
        dd.new_cases = tds[i + 1].text.replace("'", "")
        print(dd)
