#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc


test_data = {}

# positive, negative and total values
url = 'https://infocovid.smc.unige.ch/session/84651e11a4c40236825aff0a468f20b2/download/save_plot_nombre_tests_data?w='
xls = sc.xlsdownload(url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
for row in rows:
    td = sc.TestData(canton='GE', url=url)
    td.week = row['semaine']
    td.year = '2020'
    td.total_tests = row['total']
    td.positive_tests = row['positifs']
    td.negative_tests = row['négatifs']
    test_data[td.week] = td

# positivity rate
url = 'https://infocovid.smc.unige.ch/session/84651e11a4c40236825aff0a468f20b2/download/save_plot_positivity_data?w='
xls = sc.xlsdownload(url, silent=True)
rows = sc.parse_xls(xls, header_row=0, enable_float=True)
for row in rows:
    week = row['semaine']
    assert week in test_data, f'week {week} was not found in {test_data}'
    td = test_data[week]
    td.positivity_rate = float(row['positivity'])

for week, td in test_data.items():
    print(td)
