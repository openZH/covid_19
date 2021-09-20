#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc
import scrape_so_common as soc


base_url = 'https://corona.so.ch'
pdf_url = soc.get_latest_weekly_pdf_url()
content = sc.pdfdownload(pdf_url, layout=True, silent=True, page=1)
content = re.sub(r'(\d+)\'(\d+)', r'\1\2', content)

"""
Hospitalisationen im Kanton  Anzahl Personen in Isolation  davon Kontakte in Quarantäne  Anzahl zusätzlicher Personen in Quarantäne nach Rückkehr aus Risikoland  Re- Wert***
6 (6)                        120 (71)                      280 (189)                     388 (280)                                                                1.46 (1.1)
"""

rows = []

date = sc.find(r'S\s?tand: (\d+\.\d+\.20\d{2})', content)
number_of_tests = sc.find(r'Gem\s?eldete\s+Tes\s?ts\s+\(Total\)\*+?\s+(\d+)\s', content, flags=re.DOTALL)
res = re.search(r'Hospitalisationen im Kanton.*\d+ \(\d+\)\s+(\d+) \(\d+\)\s+(\d+) \(\d+\)\s+(\d+) \(\d+\)\s+', content, re.DOTALL)
if res is not None:
    data = sc.DayData(canton='SO', url=pdf_url)
    data.datetime = date
    data.tested = number_of_tests
    data.isolated = soc.strip_value(res[1])
    data.quarantined = soc.strip_value(res[2])
    data.quarantine_riskareatravel = soc.strip_value(res[3])
    rows.append(data)


# scrape the main page as well
url = "https://corona.so.ch/bevoelkerung/daten/"
d = sc.download(url, silent=True)
soup = BeautifulSoup(d, 'html.parser')
title = soup.find('h3', text=re.compile("Stand"))
data = sc.DayData(canton='SO', url=url)
data.datetime = sc.find(r'Stand\s*(\d+\.\d+\.\d{4})\s*', title.string)
table = title.find_next('table')
for table_row in table.find_all('tr'):
    title = table_row.find_all('th')
    items = table_row.find_all('td')
    if len(items) == 0:
        continue
    name = title[0].text
    value = items[0].text.replace("'", "")
    if sc.find(r'(Laborbestätigte Infektionen).*?:', name):
        data.cases = value
        continue
    if name == 'Verstorbene Personen (kumuliert seit 06.03.2020):':
        data.deaths = value
        continue
    if name == 'Im Kanton hospitalisierte Covid-19-positive Patientinnen und Patienten:':
        data.hospitalized = value
        continue
    if name.strip() == 'Davon befinden sich auf Intensivstationen:':
        data.icu = value
        continue
if data:
    rows.append(data)


is_first = True
# skip first row
for row in rows:
    if not is_first:
        print('-' * 10)
    is_first = False
    print(row)
