#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://corona.so.ch/bevoelkerung/daten/fallzahlen-nach-gemeinden/'
d = sc.download(url, silent=True)

date = sc.find(r'Stand (\d+\.\d+\.20\d{2})', d)
date = sc.date_from_text(date)

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


def strip_so_number(value):
    return int(value.replace('\'', ''))


soup = BeautifulSoup(d, 'html.parser')
for district, d_id in district_ids.items():
    table = soup.find(text=district).find_next('table')
    trs = table.find_all('tr')
    tds = trs[-1].find_all('td')
    assert tds[0].text == 'Total', f'Expected "Total" row, got {tds[0].text}'
    dd = sc.DistrictData(canton='SO', district=district)
    dd.url = url
    dd.date = date.isoformat()
    dd.population = strip_so_number(tds[1].text)
    dd.district_id = d_id
    dd.total_cases = strip_so_number(tds[2].text)
    dd.new_cases = int(tds[3].text)
    print(dd)
