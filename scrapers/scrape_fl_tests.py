#!/usr/bin/env python3

import scrape_common as sc

url = 'https://www.llv.li/files/as/grafik_covid19_tests_pro_kw.xlsx'
xls = sc.xlsdownload(url, silent=True)
rows = sc.parse_xls(xls, header_row=61, sheet_name='gTests_AG')
year = '2020'
for row in rows:
    if row['B'] is None:
        # skip the footer line
        continue
    td = sc.TestData(canton='FL', url=url)
    td.week = int(sc.find(r'KW (\d+)', row['B']))
    if td.week == 1:
        year = '2021'
    td.year = year
    td.negative_tests = row['Negativ']
    td.positive_tests = row['Positiv']
    print(td)
