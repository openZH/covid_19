#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import datetime
from bs4 import BeautifulSoup
import scrape_common as sc

d = sc.download('https://www.sz.ch/behoerden/information-medien/medienmitteilungen/coronavirus.html/72-416-412-1379-6948', silent=True)
soup = BeautifulSoup(d, 'html.parser')

pdf_url = soup.find('a', string=re.compile(r'Medienmitteilung vom'))['href']
pdf_content = sc.pdfdownload(pdf_url, layout=True, silent=True)
date = sc.find(r'Stand:\s(\d+\.\s.*\s20\d{2})', pdf_content).replace('\n', ' ')
res = re.search(r'.*\s+\d+\s+\d+\s+\d+\s+(\d+)\s+(\d+)\s+(\d+)\s+', pdf_content)
is_first = True
if res is not None:
    dd = sc.DayData(canton='SZ', url=pdf_url)
    dd.datetime = date
    dd.hospitalized = res[1]
    dd.quarantined = res[2]
    dd.quarantine_riskareatravel = res[3]
    print(dd)
    is_first = False


try:
    xls_url = soup.find('a', string=re.compile(r'Coronaf.lle\s*im\s*Kanton\s*Schwyz'))['href']
except TypeError:
    print("Unable to determine xls url", file=sys.stderr)
    sys.exit(1)
xls = sc.xlsdownload(xls_url, silent=True)

rows = sc.parse_xls(xls)
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

    dd = sc.DayData(canton='SZ', url=xls_url)
    dd.datetime = row['Datum'].date().isoformat()
    if row['Zeit']:
        dd.datetime += ' ' + row['Zeit'].time().isoformat()
    dd.cases = row['Bestätigte Fälle (kumuliert)']
    dd.deaths = row['Todesfälle (kumuliert)']
    dd.recovered = row['Genesene (kumuliert)']
    print(dd)
