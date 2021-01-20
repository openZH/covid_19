#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
from bs4 import BeautifulSoup
import scrape_common as sc
import scrape_vs_common as svc


pdf_url = svc.get_vs_daily_pdf_url()
content = sc.pdfdownload(pdf_url, silent=True, layout=True, page=1)

dd = sc.DayData(canton='VS', url=pdf_url)
dd.datetime = sc.find(r'(\d{2}/\d{2}/20\d{2})', content)
dd.datetime = re.sub(r'/', '.', dd.datetime)
dd.cases = svc.strip_value(sc.find(r'.*Cumul cas positifs.*\s+(\d+.\d+)\s+', content))
dd.deaths = svc.strip_value(sc.find(r'.*Cumul d.c.s.*\s+(\d+.\d+)\s+', content))
dd.hospitalized = svc.strip_value(sc.find(r'.*Hospitalisations en cours de cas COVID-19.*\s+(\d+)\s+', content))
dd.icu = svc.strip_value(sc.find(r'.*SI en cours.*\s+(\d+)\s+', content))
dd.vent = svc.strip_value(sc.find(r'.*Intubation en cours.*\s+(\d+)\s+', content))

is_first = True
if dd:
    is_first = False
    print(dd)


xls_url = 'https://raw.githubusercontent.com/statistikZH/covid19_drop/master/Chiffres%20COVID-19%20Valais.xlsx'
main_url = 'https://www.vs.ch/de/web/coronavirus'
xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=1)
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
    # Since 2020-10-19 VS does no longer publish data about isolation/quarantined
    #dd.isolated = row['Nombre de cas en cours d\'isolement']
    #dd.quarantined = row['Nombre de contacts en cours de quarantaine']
    #dd.quarantine_riskareatravel = row['Nombre de voyageurs en cours de quarantaine']

    if row['Nb de nouvelles sorties'] is not None:
        dd.recovered = sum(r['Nb de nouvelles sorties'] for r in rows[:i+1])
    if not is_first:
        print('-' * 10)
    is_first = False
    print(dd)
