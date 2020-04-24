#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

d = sc.download('https://www.sz.ch/behoerden/information-medien/medienmitteilungen/coronavirus.html/72-416-412-1379-6948', silent=True)
soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find('a', string=re.compile(r'Coronaf.lle\s*im\s*Kanton\s*Schwyz'))['href']
xls = sc.xlsdownload(xls_url, silent=True)

rows = sc.parse_xls(xls)
for i, row in enumerate(rows):
    if not row['Datum']:
        continue
    print('SZ')
    sc.timestamp()
    print('Downloading:', xls_url)
    if row['Zeit']:
        print('Date and time:', row['Datum'].date().isoformat(), row['Zeit'].time().isoformat())
    else:
        print('Date and time:', row['Datum'].date().isoformat())
    print('Confirmed cases:', row['Bestätigte Fälle (kumuliert)'])
    print('Deaths:', row['Todesfälle (kumuliert)'])
    print('Recovered:', row['Genesene (kumuliert)'])
    # do not print record delimiter for last record
    # this is an indicator for the next script to check
    # for expected values.
    if len(rows) - 1 > i:
        print('-' * 10)
