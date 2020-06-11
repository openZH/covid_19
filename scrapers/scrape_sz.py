#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import datetime
from bs4 import BeautifulSoup
import scrape_common as sc

d = sc.download('https://www.sz.ch/behoerden/information-medien/medienmitteilungen/coronavirus.html/72-416-412-1379-6948', silent=True)
soup = BeautifulSoup(d, 'html.parser')
try:
    xls_url = soup.find('a', string=re.compile(r'Coronaf.lle\s*im\s*Kanton\s*Schwyz'))['href']
except TypeError:
    print("Unable to determine xls url", file=sys.stderr)
    sys.exit(1)
xls = sc.xlsdownload(xls_url, silent=True)

rows = sc.parse_xls(xls)
is_first = True
for row in rows:
    if not isinstance(row['Datum'], datetime.datetime):
        continue

    if not is_first:
        print('-' * 10)
    is_first = False

    # TODO: remove when source is fixed
    # handle wrong value on 2020-03-25, see issue #631
    if row['Datum'].date().isoformat() == '2020-03-25':
        row['Bestätigte Fälle (kumuliert)'] = ''

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
