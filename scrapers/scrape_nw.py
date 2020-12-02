#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://www.nw.ch/gesundheitsamtdienste/6044'
content = sc.download(url, silent=True)
content = content.replace("&nbsp;", " ")
soup = BeautifulSoup(content, 'html.parser')

item = soup.find(text=re.compile('Anzahl F.lle')).find_parent('h3')
assert item, f"Could not find title item in {url}"

dd = sc.DayData(canton='NW', url=url)
dd.datetime = sc.find(r'Stand: (\d+\. .* 20\d{2})', item.text)

rows = item.find_next('table').findChildren('tr')
for row in rows:
    cols = row.findChildren('td')
    item = cols[0].text
    if re.match(r'positiv getestete personen.*', item, re.I):
        dd.cases = cols[1].text
    elif re.match(r'derzeit hospitalisiert', item, re.I):
        dd.hospitalized = cols[1].text
    elif re.match(r'davon auf der intensivstation', item, re.I):
        dd.icu = cols[1].text
    elif re.match(r'verstorbene personen', item, re.I):
        dd.deaths = cols[1].text
    elif re.match(r'personen in isolation', item, re.I):
        dd.isolated = cols[1].text
    elif re.match(r'kontaktpersonen in quarant.ne', item, re.I):
        dd.quarantined = cols[1].text
    elif re.match(r'Reiser.ckkehrer in quarant.ne', item, re.I):
        dd.quarantine_riskareatravel = cols[1].text

is_first = True
if dd:
    print(dd)
    is_first = False


xls_url = 'http://www.nw.ch/coronastatistik'
xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=2)
for row in rows:
    dd = sc.DayData(canton='NW', url=xls_url)
    dd.datetime = row['A'].date().isoformat()
    dd.cases = row['Positiv getestete Personen (kumuliert)']
    dd.icu = row['Davon auf der Intensivstation']

    try:
        dd.hospitalized = row['Aktuell hospitalisierte Personen']
    except KeyError:
        dd.hospitalized = row['Hospitalisierte Personen']

    try:
        dd.deaths = row['Personen verstorben']
    except KeyError:
        dd.deaths = row['Verstorbene Personen']

    # skip empty rows
    if dd.cases is None and dd.icu is None and dd.hospitalized is None and dd.deaths is None:
        continue

    if not is_first:
        print('-' * 10)
    is_first = False
    print(dd)
