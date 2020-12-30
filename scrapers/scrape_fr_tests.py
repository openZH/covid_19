#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc
from scrape_fr_common import get_fr_xls

xls_url, xls = get_fr_xls()
rows = sc.parse_xls(xls, header_row=0, sheet_name='tests', enable_float=True)

for row in rows:
    td = sc.TestData(canton='FR', url=xls_url)
    td.week = row['semaine /Woche']
    td.year = '2020'
    tot_ag = int(row['Tests AG'])
    tot_pcr = int(row['Tests PCR'])
    td.total_tests = tot_ag + tot_pcr
    print(td)
