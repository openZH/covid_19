#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc
from scrape_fr_common import get_fr_xls

xls_url, xls = get_fr_xls()
rows = sc.parse_xls(xls, header_row=0, sheet_name='tests', enable_float=True)

year = '2020'

for row in rows:
    week = row['semaine /Woche']
    if not week:
        continue

    if week == 1:
        year = '2021'

    td = sc.TestData(canton='FR', url=xls_url)
    td.week = int(week)
    td.year = year
    tot_ag = int(row['Tests AG'])
    tot_pcr = int(row['Tests PCR'])
    td.total_tests = tot_ag + tot_pcr
    print(td)
