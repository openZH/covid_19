#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
from bs4 import BeautifulSoup
import scrape_common as sc


xls_url = 'https://raw.githubusercontent.com/statistikZH/covid19_drop/master/Chiffres%20%20COVID-19%20Valais.xlsx'
main_url = 'https://www.vs.ch/de/web/coronavirus'
xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=1)
is_first = True
for i, row in enumerate(rows):
    if not isinstance(row['Date'], datetime.datetime):
        continue
    if not sc.represents_int(row['Cumul cas positifs']):
        continue
    if row['Nb nouveaux cas positifs'] is None and row["Nb nouvelles admissions à l'hôpital"] is None:
        continue

    dd = sc.DayData(canton='VS', url=main_url)
    dd.datetime = row['Date'].date().isoformat()
    dd.cases = row['Cumul cas positifs']
    dd.hospitalized = row['Total hospitalisations COVID-19']
    dd.new_hosp = row['Nb nouvelles admissions à l\'hôpital']
    dd.icu = row['Patients COVID-19 aux SI total (y.c. intubés)']
    dd.vent = row['Patients COVID-19 intubés']
    dd.deaths = row['Cumul décès COVID-19']
    dd.isolated = row['Nombre de cas en cours d\'isolement']
    dd.quarantined = row['Nombre de contacts en cours de quarantaine']
    dd.quarantine_riskareatravel = row['Nombre de voyageurs en cours de quarantaine']

    if row['Nb de nouvelles sorties'] is not None:
        dd.recovered = sum(r['Nb de nouvelles sorties'] for r in rows[:i+1])
    if not is_first:
        print('-' * 10)
    is_first = False
    print(dd)
