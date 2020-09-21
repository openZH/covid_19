#!/usr/bin/env python

import re
import sys

from bs4 import BeautifulSoup

import scrape_common as sc

# get the latest weekly PDF
base_url = 'https://www.vs.ch'
url = base_url + '/de/web/coronavirus/statistiques'
content = sc.download(url, silent=True)
soup = BeautifulSoup(content, 'html.parser')
link = soup.find(href=re.compile(r'Synthese.*Woche'))

# fetch the PDF
url = base_url + link['href'].replace(' ', '%20')
content = sc.pdfdownload(url, silent=True, page=1)
week = sc.find(r'Epidemiologische Situation Woche (\d+)', content)
year = sc.find(r'\d+\.\d+\.(\d{4})', content)

content = sc.pdfdownload(url, silent=True, page=11, layout=True, rect=[0, 403, 450, 50])

# kill the left most values
content = re.sub(r'^\d+\s', ' ', content)
content = re.sub(r'\n\d+ ', '\n ', content)

# remove right axis description
content = re.sub(r'([a-z|A-Z])', '', content)

# remove right axis and other percentage values
content = re.sub(r'(\d+\.\d)', '', content)

# remove strange characters at the end of the string
content = content.rstrip()

"""
this results in something like this (13 columns expected for the districts)

    0   1       3   1   7   3   8   2   22   2   4   10
           1
"""

lines = []
for line in content.split('\n'):
    res = re.search(r'\s?(\d+)\s?', line)
    if res is not None:
        lines.append(line)

cases = {}
for line in lines:
    for res in re.finditer(r'(\d+)', line):
        cases[res.start()] = int(res[1])
cases_sorted = dict(sorted(cases.items(), key=lambda item: item[0]))

# this is the order in the PDF
districts = [
    'Goms',
    'Raron',
    'Brig',
    'Visp',
    'Leuk',
    'Sierre',
    'Herens',
    'Sion',
    'Conthey',
    'Martigny',
    'Entremont',
    'St-Maurice',
    'Monthey',
]

district_ids = [
    2304,
    2309,
    2301,
    2313,
    2306,
    2311,
    2305,
    2312,
    2302,
    2307,
    2303,
    2310,
    2308,
]

population = [
    4440,
    10930,
    26910,
    28650,
    12360,
    49230,
    10860,
    47750,
    28910,
    47980,
    15260,
    13830,
    46840,
]


if len(cases_sorted) == 13:
    # for i in range(13):
    i = 0
    for key, value in cases_sorted.items():
        dd = sc.DistrictData(canton='VS', district=districts[i])
        dd.url = url
        dd.district_id = district_ids[i]
        dd.population = population[i]
        dd.week = week
        dd.year = year
        dd.new_cases = value
        print(dd)
        i += 1
else:
    print(f'expected 13 district values, but got {len(cases_sorted)} for {url}', file=sys.stderr)
