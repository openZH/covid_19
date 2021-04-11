#!/usr/bin/env python3

import scrape_common as sc
import scrape_ag_common as sac


def get_value_int(value):
    if value is not None and value != '':
        return int(value)
    return None


def get_value_float(value):
    if value is not None and value != '':
        return float(value)
    return None


xls_url = sac.get_ag_xls_url()
xls = sc.xlsdownload(xls_url, silent=True)

year = '2020'
rows = sc.parse_xls(xls, sheet_name='1.4 Labortests', header_row=1, enable_float=True)
for row in rows:
    if not row['Anzahl Tests']:
        continue
    if row['Anzahl Tests'] == 'Anzahl Tests':
        break

    td = sc.TestData(canton='AG', url=xls_url)
    td.week = int(row['Kalenderwoche'])
    if td.week == 1:
        year = '2021'
    td.year = year
    td.positive_tests = get_value_int(row['Positive Tests'])
    td.negative_tests = get_value_int(row['Negative Tests'])
    td.total_tests = int(row['Anzahl Tests'])
    td.positivity_rate = get_value_float(row['Positivitätsrate'])
    td.pcr_positivity_rate = get_value_float(row['F'])
    td.ag_positivity_rate = get_value_float(row['G'])
    if td:
        print(td)
