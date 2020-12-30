#!/usr/bin/env python3

import scrape_common as sc
import scrape_ag_common as sac


xls_url = sac.get_ag_xls_url()
xls = sc.xlsdownload(xls_url, silent=True)

rows = sc.parse_xls(xls, sheet_name='1.3 Labortests', header_row=1, enable_float=True)
for row in rows:
    if not row['Anzahl Tests']:
        continue

    td = sc.TestData(canton='AG', url=xls_url)
    td.week = int(row['Kalenderwoche'])
    td.year = '2020'
    td.positive_tests = int(row['Positive Tests'])
    td.negative_tests = int(row['Negative Tests'])
    td.total_tests = int(row['Anzahl Tests'])
    td.positivity_rate = float(row['Positivitätsrate'])
    if td:
        print(td)
