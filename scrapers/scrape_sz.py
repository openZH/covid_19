#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

print('SZ')

d = sc.download('https://www.sz.ch/behoerden/information-medien/medienmitteilungen/coronavirus.html/72-416-412-1379-6948')
soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find('a', string=re.compile(r'Coronaf.lle\s*im\s*Kanton\s*Schwyz'))['href']
xls = sc.xlsdownload(xls_url)
sc.timestamp()

rows = sc.parse_xls(xls)
if rows:
    last_row = rows[-1]
    print('Date and time:', last_row['Datum'].date().isoformat())
    print('Confirmed cases:', last_row['Bestätigte Fälle (kumuliert)'])
    print('Deaths:', last_row['Todesfälle (kumuliert)'])
    print('Recovered:', last_row['Genesene (kumuliert)'])
