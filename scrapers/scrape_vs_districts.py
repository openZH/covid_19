#!/usr/bin/env python

import re

import scrape_common as sc
import scrape_vs_common as svc

# get the latest weekly PDF
url = svc.get_vs_latest_weekly_pdf_url()

# fetch the PDF
pdf = sc.download_content(url, silent=True)
week, year = svc.get_vs_weekly_general_data(pdf)

# second last page contains the district data
pages = int(sc.pdfinfo(pdf))
page = None
for p in range(1, pages):
    content = sc.pdftotext(pdf, page=p, layout=True)
    if sc.find(r'(Geografische)\s+.*', content):
        page = p
        break

assert page > 0
content = sc.pdftotext(pdf, page=page, layout=True, rect=[0, 443, 420, 50], fixed=2)

# strip everything including the "Anzahl Faelle" column + values
def strip_left_number(content):
    lines = content.split('\n')
    pos = None
    for line in lines:
        res = re.search(r'\s+(\d+)   ', line)
        if res is not None:
            if pos is None:
                pos = res.end()
            else:
                pos = min(pos, res.end())
    new_content = []
    for line in lines:
        new_content.append(line[pos:])
    return '\n'.join(new_content)


# strip from the right the "Inzidenz pro 100k Einwohner" column / description
def strip_right_items(content):
    lines = content.split('\n')
    pos = None
    for line in lines:
        res = re.search(r'(\d+|\d+\.\d+)\s?$', line)
        if res is not None:
            if pos is None:
                pos = res.start()
            else:
                pos = max(pos, res.start())
    new_content = []
    for line in lines:
        new_content.append(line[:pos])
    return '\n'.join(new_content)

# kill the left and right axis
content = strip_left_number(content)
# content = strip_right_items(content)

# remove strange characters at the end of the string
#content = content.rstrip()

"""
this results in something like this (13 columns expected for the districts)

                                                                                                                              6.6

                                  9          6                       7          2           5           8         15           1           6          16
"""

# approximate the width of each "column" in the table
# get the maxima and divide it by the 13 expected districts
length=None
for line in content.split('\n'):
    llenght = len(line)
    if length is None:
        length = llenght
    else:
        length = max(llenght, length)
length = round(length / 14.5)

# split up all lines by the length and use the "lowest line" value
district_values = []
for i in range(0, 13):
    value = ''
    for line in content.split('\n'):
        val = line[i * length:(i + 1) * length].strip()
        if val != '':
            value = val
    if value == '':
        value = 0
    district_values.append(int(value))


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


assert len(district_values) == 13, f'expected 13 district values, but got {len(district_values)} for {url}'
i = 0
for value in district_values:
    dd = sc.DistrictData(canton='VS', district=districts[i])
    dd.url = url
    dd.district_id = district_ids[i]
    dd.population = population[i]
    dd.week = week
    dd.year = year
    dd.new_cases = value
    print(dd)
    i += 1
