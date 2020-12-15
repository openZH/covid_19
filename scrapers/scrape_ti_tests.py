#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import scrape_common as sc

main_url = 'https://www4.ti.ch/dss/dsp/covid19/home/'
d = sc.download(main_url, silent=True)
soup = BeautifulSoup(d, 'html.parser')

td = sc.TestData(canton='TI', url=main_url)

container = soup.find('h2', string=re.compile(r'Test PCR')).find_next('div')
for item in container.find_all('div'):
    divs = item.find_all('div')
    if len(divs) == 3:
        if divs[2].string:
            date = sc.find(r'.*?(\d+\.\d+\.\d{2})', divs[2].string)
            date = sc.date_from_text(date)
            td.start_date = date.isoformat()
            td.end_date = date.isoformat()
        if sc.find(r'^(Totale test).*', divs[1].string):
            td.total_tests = divs[0].string
        if sc.find(r'^(% test).*', divs[1].string):
            td.positivity_rate = divs[0].string

if td:
    assert td.start_date and td.end_date, 'failed to extract date'
    print(td)
