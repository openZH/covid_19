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
pages = sc.pdfinfo(pdf)

vd = sc.VaccinationData(canton='JU', url=pdf_url)

content = sc.pdftotext(pdf, page=1)
year = sc.find(r'Du \d+.* (\d{4})', content)

content = sc.pdftotext(pdf, page=pages, layout=True)

date = sc.find(r'Vaccination: .* au (\d+ \w+)', content)
date = sc.date_from_text(f'{date} {year}')
vd.date = date.isoformat()

# TODO not sure if this is the total for the week only and need to sum up all vaccinations
vd.total_vaccinations = sc.find(r'Total\s+\d+\s+\d+\s+(\d+)', content)

print(vd)
