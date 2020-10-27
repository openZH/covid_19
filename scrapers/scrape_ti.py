#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import scrape_common as sc

# get pdf and xlsx URL from covid19 page of TI
main_url = 'https://www4.ti.ch/dss/dsp/covid19/home/'
d = sc.download(main_url, silent=True)
soup = BeautifulSoup(d, 'html.parser')

pdf_url = soup.find('a', string=re.compile(r'Dati stato.*')).get('href')
pdf_url = f'https://www4.ti.ch/{pdf_url}'
pdf_content = sc.pdfdownload(pdf_url, silent=True, raw=True)

dd = sc.DayData(canton='TI', url=pdf_url)
dd.datetime = sc.find(r'(Stato )?(\d+\.\d+\.20\d{2})', pdf_content, group=2)
dd.isolated = sc.find(r'(\d+)\sPersone\sin\sisolamento', pdf_content)
dd.quarantined = sc.find(r'(\d+)\sPersone\sin\squarantena', pdf_content)
is_first = True
if dd:
    print(dd)
    is_first = False


xls_url = soup.find(href=re.compile("\.xlsx$")).get('href')
assert xls_url, "URL is empty"

if not xls_url.startswith('http'):
    xls_url = f'https://www4.ti.ch/{xls_url}'

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
for row in rows:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='TI', url=xls_url)
    dd.datetime = f"{row['Data'].date().isoformat()}"
    if row['Ora']:
        dd.datetime += f"T{row['Ora'].time().isoformat()}"
    dd.cases = row['Totale casi confermati']
    dd.hospitalized = row['Pazienti ricoverati attualmente']
    dd.icu = row['Pazienti in cure intense']
    dd.vent = row['Pazienti ventilati']
    dd.recovered = row['Totale pazienti dimessi da ospedali']
    dd.deaths = row['Totale decessi']
    print(dd)
