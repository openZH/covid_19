#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup

import scrape_common as sc

url = 'https://www.sz.ch/behoerden/information-medien/medienmitteilungen/coronavirus.html/72-416-412-1379-6948'
content = sc.download(url, silent=True)
soup = BeautifulSoup(content, 'html.parser')
pdf_url = soup.find('a', text=re.compile(r'Coronafälle pro Gemeinde')).get('href')

content = sc.pdfdownload(pdf_url, layout=True, silent=True)
date = sc.find(r'Stand\W+(\d+\.\d+\.20\d{2})', content)
date = sc.date_from_text(date).isoformat()
district_data = re.findall(r'^Bezirk\W+(\w+)\s+(≤?\s?\d+)', content, re.MULTILINE)

# https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/karten.assetdetail.5688189.html
district_ids = {
    'Einsiedeln': 501,
    'Gersau': 502,
    'Höfe': 503,
    'Küssnacht': 504,
    'March': 505,
    'Schwyz': 506,
}

# https://www.sz.ch/kanton/bezirke/schwyz.html/72-210-112-106
population = {
    'Einsiedeln': 16027,
    'Gersau': 2314,
    'Höfe': 29123,
    'Küssnacht': 13270,
    'March': 43528,
    'Schwyz': 55390,
}

assert len(district_data) == len(district_ids), f'expected {len(district_ids)} districts available, but got {len(district_data)}: {district_data}'

for district, total_cases in district_data:
    assert district in district_ids, f'District {district} is unknown'

    dd = sc.DistrictData(canton='SZ', district=district)
    dd.url = pdf_url
    dd.district_id = district_ids[district]
    dd.population = population[district]
    dd.date = date
    # skip total_cases for ≤ entries
    if not sc.find(r'(≤)', total_cases):
        dd.total_cases = total_cases
    print(dd)
