#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc
from scrape_fr_common import get_fr_xls

xls_url, xls = get_fr_xls()
rows = sc.parse_xls(xls, header_row=0, sheet_name='tests COVID19', enable_float=True)

for row in rows:
    td = sc.TestData(canton='FR', url=xls_url)
    td.week = sc.find(r'S (\d+)', row['Semaine'])
    td.year = '2020'
    tot = int(row['Total Testing Pop FR'])
    pos = int(row['Total POS Pop FR'])
    td.positive_tests = pos
    td.total_tests = tot
    print(td)
