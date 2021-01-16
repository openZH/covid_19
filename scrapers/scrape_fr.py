#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import sys
import scrape_common as sc
from scrape_fr_common import get_fr_xls

xls_url, xls, main_url = get_fr_xls()
rows = sc.parse_xls(xls, header_row=0)
is_first = True

col_info = (
    (r'.*Total cas avérés.*', 'Confirmed cases'),
    (r'.*Personnes hospitalisées.*', 'Hospitalized'),
    (r'.*aux soins intensifs.*', 'ICU'),
    (r'.*Total décès.*', 'Deaths'),
    (r'.*Total Sorties de l\'hôpital.*', 'Recovered')
)

for row in rows:
    row_date = row.search(r'.*Date.*')

    if not isinstance(row_date, datetime.datetime):
        print(f"WARNING: {row_date} is not a valid date, skipping.", file=sys.stderr)
        continue

    if not is_first:
        print('-' * 10)
    is_first = False

    print('FR')
    sc.timestamp()
    print('Downloading:', main_url)
    print('Date and time:', row_date.date().isoformat())
    for col in col_info:
        value = row.search(col[0])
        if value is not None:
            value = str(value).replace('*', '')
            print(f'{col[1]}:', value)
