#!/usr/bin/env python3

import re
import datetime
from bs4 import BeautifulSoup
import scrape_common as sc

d = sc.download('https://www.ow.ch/de/kanton/publired/publikationen/?action=info&pubid=20318',
                encoding='windows-1252')
soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find(href=re.compile("\.XLSX$")).get('href')
assert xls_url, "URL is empty"

for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if cells[0].string and cells[0].string.startswith('Datum'):
        file_date = cells[1].string

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
is_first = True
for row in rows:
    if isinstance(row['A'], datetime.datetime):
        dd = sc.DayData(canton='OW', url=xls_url)
        dd.datetime = row['A']
        data_found = False
        if isinstance(row['B'], int):
            dd.cases = row['B']
            data_found = True
        if isinstance(row['D'], int):
            dd.hospitalized = row['D']
            data_found = True
        if isinstance(row['E'], int):
            dd.deaths = row['E']
            data_found = True
        if data_found:
            if not is_first:
                print('-' * 10)
            else:
                is_first = False
            print(dd)

