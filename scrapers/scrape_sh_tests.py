#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
from bs4 import BeautifulSoup
import scrape_common as sc
import scrape_sh_common as shc

main_url, xls = shc.get_sh_xlsx()

rows = sc.parse_xls(xls, sheet_name='Datensatz_Tests', header_row=0)
for row in rows:
    if not (row['Jahr'] or row['Kalenderwoche']):
        continue

    td = sc.TestData(canton='SH', url=main_url)
    td.year = row['Jahr']
    td.week = row['Kalenderwoche']

    td.pcr_total_tests = 0
    pcr_cols = ['Tests KAZ', 'Tests Apotheken', 'Tests KSSH', 'Test Praxen']
    for col in pcr_cols:
        if sc.represents_int(row[col]):
            td.pcr_total_tests += row[col]

    td.ag_total_tests = 0
    ag_cols = ['Schnelltests KAZ', 'Schnelltests Apotheken', 'Schnelltests KSSH', 'Schnelltest Praxen']
    for col in ag_cols:
        if sc.represents_int(row[col]):
            td.ag_total_tests += row[col]
    td.total_tests = td.pcr_total_tests + td.ag_total_tests
    print(td)
