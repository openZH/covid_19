#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import scrape_common as sc

xls_url = 'https://raw.githubusercontent.com/statistikZH/covid19_drop/master/Chiffres%20%20COVID-19%20Valais.xlsx'
main_url = 'https://www.vs.ch/de/web/coronavirus'
xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=1)
is_first = True
for i, row in enumerate(rows):
    if not isinstance(row['Date'], datetime.datetime):
        continue

    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='VS', url=main_url)
    dd.datetime = row['Date'].date().isoformat()
    dd.cases = row['Cumul cas positifs']
    dd.hospitalized = row['Total hospitalisations COVID-19']
    dd.new_hosp = row['Nb nouvelles admissions à l\'hôpital']
    dd.icu = row['Patients COVID-19 aux SI total (y.c. intubés)']
    dd.vent = row['Patients COVID-19 intubés']
    dd.deaths = row['Cumul décès COVID-19']
    dd.recovered = sum(r['Nb de nouvelles sorties'] for r in rows[:i+1])
    print(dd)

