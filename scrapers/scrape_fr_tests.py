#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc
from scrape_fr_common import get_fr_csv

"""
csv_url, csv_data, main_url = get_fr_csv()
reader = csv.DictReader(StringIO(csv_data), delimiter=';')


year = '2020'

for row in rows:
    week = row['semaine /Woche']
    if not week:
        continue

    if week == 1:
        year = '2021'

    td = sc.TestData(canton='FR', url=main_url)
    td.week = int(week)
    td.year = year
    td.pcr_total_tests = int(row['Tests PCR'])
    if row['Taux/Rate PCR']:
        td.pcr_positivity_rate = round(row['Taux/Rate PCR'] * 100)
    td.ag_total_tests = int(row['Tests AG'])
    if row['Taux/Rate AG']:
        td.ag_positivity_rate = round(row['Taux/Rate AG'] * 100)
    td.total_tests = td.pcr_total_tests + td.ag_total_tests
    print(td)
"""
