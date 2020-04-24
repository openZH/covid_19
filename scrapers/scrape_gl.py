#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

d = sc.download('https://www.gl.ch/verwaltung/finanzen-und-gesundheit/gesundheit/coronavirus.html/4817', silent=True)


soup = BeautifulSoup(d, 'html.parser')
box = soup.find('div', class_="box--error")
xls_url = box.find('a', string=re.compile(r'.*Dokument.*')).get('href')

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls)
for i, row in enumerate(rows):
    print('GL')
    sc.timestamp()
    print('Downloading:', xls_url)
    if row['Zeit']:
        print('Date and time:', row['Datum'].date().isoformat(), row['Zeit'].time().isoformat())
    else:
        print('Date and time:', row['Datum'].date().isoformat())
    print('Confirmed cases:', row['Bestätigte Fälle (kumuliert)'])
    print('Hospitalized:', row['Personen in Spitalpflege'])
    print('Deaths:', row['Todesfälle (kumuliert)'])
    # do not print record delimiter for last record
    # this is an indicator for the next script to check
    # for expected values.
    if len(rows) - 1 > i:
        print('-' * 10)
