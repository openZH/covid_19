#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

print('GL')
d = sc.download('https://www.gl.ch/verwaltung/finanzen-und-gesundheit/gesundheit/coronavirus.html/4817')
sc.timestamp()


soup = BeautifulSoup(d, 'html.parser')
box = soup.find('div', class_="box--error")
xls_url = box.find('a', string=re.compile(r'.*Dokument.*')).get('href')
xls = sc.xlsdownload(xls_url)
sc.timestamp()

rows = sc.parse_xls(xls)
if rows:
    last_row = rows[-1]
    print('Date and time:', last_row['Datum'].date().isoformat(), last_row['Zeit'].time().isoformat())
    print('Confirmed cases:', last_row['Bestätigte Fälle (kumuliert)'])
    print('Hospitalized:', last_row['Personen in Spitalpflege'])
    print('Deaths:', last_row['Todesfälle (kumuliert)'])
