#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

url = "https://corona.so.ch/index.php?id=27979"
d = sc.download(url, silent=True)

rows = []
soup = BeautifulSoup(d, 'html.parser')
data_table = soup.find('h2', text=re.compile("Situation Kanton Solothurn")).find_next("table")
if data_table:
    headers = [cell.string for cell in data_table.find('tr').find_all('th')]
    for row in data_table.find_all('tr'):
        data = sc.DayData(canton='SO', url=url)
        col_num = 0
        tmp_date = None
        tmp_time = None
        for cell in row.find_all(['td']):
            if headers[col_num] == 'Datum':
                tmp_date = cell.string
            elif headers[col_num] == 'Zeit':
                tmp_time = cell.string
            elif headers[col_num] == 'Bestätigte Fälle (kumuliert)':
                data.cases = cell.string.strip()
            elif headers[col_num] == 'Todesfälle (kumuliert)':
                data.deaths = cell.string.strip()
            elif headers[col_num] == 'Im Kanton Hospitalisierte Personen':
                data.hospitalized = cell.string.strip()
            col_num += 1
        if data and tmp_date is not None and \
                not tmp_date.startswith('bis ') and not (tmp_date is None and tmp_time is None):
            data.datetime = f"{tmp_date} {tmp_time}".strip()
            rows.append(data)
else:
    # if the table is not there (it vanished on 2020-05-20) fallback to main page
    url = "https://corona.so.ch/"
    d = sc.download(url, silent=True)
    soup = BeautifulSoup(d, 'html.parser')
    title = soup.find('strong', text=re.compile("Situation Kanton Solothurn"))
    data_list = title.find_parent("div").find_all('li')
    date_str = sc.find('Stand\s*(.+)\s*Uhr', title.string)
    data = sc.DayData(canton='SO', url=url)
    for item in data_list:
        content = "".join([str(s) for s in item.contents])
        if not item:
            continue
        if 'Anzahl positiv getesteter Erkrankungsfälle' in content:
            data.cases = sc.find('.*:.*?(\d+)\s*.*', content).strip()
            continue
        if 'Verstorbene Personen' in content:
            data.deaths = sc.find('.*:.*?(\d+)\s*.*', content).strip()
            continue
        if 'hospitalisierte Personen' in content and not 'weniger als' in content:
            data.hospitalized = sc.find('.*:.*?(\d+)\s*.*', content).strip()
            continue
    rows.append(data)


is_first = True
# skip first row
for row in rows:
    if not is_first:
        print('-' * 10)
    is_first = False
    print(row)

