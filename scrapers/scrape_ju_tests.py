#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

base_url = 'https://www.jura.ch'
url = f'{base_url}/fr/Autorites/Coronavirus/Chiffres-H-JU/Evolution-des-cas-COVID-19-dans-le-Jura.html'
d = sc.download(url, silent=True)
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')

pdf_url = soup.find('a', title=re.compile(r'.*PDF.*')).get('href')
if not pdf_url.startswith('http'):
    pdf_url = f'{base_url}{pdf_url}'
pdf_url = pdf_url.replace('?download=1', '')

pdf = sc.download_content(pdf_url, silent=True)

td = sc.TestData(canton='JU', url=pdf_url)

content = sc.pdftotext(pdf, page=1)
td.week = sc.find(r'Situation semaine épidémiologique (\d+)', content)
td.year = sc.find(r'Du \d+.* (\d{4})', content)

content = sc.pdftotext(pdf, page=2)
td.total_tests = sc.find(r'Nombre de tests\d?\s+(\d+)', content)
res = re.match(r'.*Nombre de tests positifs .*\s+(\d+)\s+\((\d+\.?\d?)%\s?\d?\)', content, re.DOTALL | re.MULTILINE)
assert res, 'failed to find number of positive tests and positivity rate'
td.positive_tests = res[1]
td.positivity_rate = res[2]

print(td)
