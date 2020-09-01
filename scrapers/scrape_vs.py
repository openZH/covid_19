#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
from bs4 import BeautifulSoup
import scrape_common as sc

# parse weekly data for isolated and quarantined numbers
base_url = 'https://www.vs.ch'
stat_url = base_url + '/de/web/coronavirus/statistiques'
content = sc.download(stat_url, silent=True)
soup = BeautifulSoup(content, 'html.parser')
res = soup.find(string=re.compile(r'Synthese COVID19 VS Woche\d+')).find_previous('a')
weekly_pdf_url = base_url + res.attrs['href']
weekly_pdf_url = weekly_pdf_url.replace(' ', '%20')
content = sc.pdfdownload(weekly_pdf_url, silent=True)


# add isolated/quarantined to the existing DayData item
week_end_date = sc.find(r'vom (\d+)\. bis (\d+\.\d+\.20\d{2})', content, group=2)
week_end_date = sc.date_from_text(week_end_date).isoformat()

dd = sc.DayData(canton='VS', url=weekly_pdf_url)
dd.datetime = week_end_date
dd.isolated = sc.find(r'befanden\ssich\s(\d+)\spositive\sF.lle\snoch\simmer\sin\sIsolation', content)
dd.quarantined = sc.find(r'Isolation\sund\s(\d+)\sKontakte\sin\sQuarant.ne', content)
dd.quarantine_riskareatravel = sc.find(r'\s(\d+)\sReisende\sin\sQuarant.ne', content)
print(dd)

xls_url = 'https://raw.githubusercontent.com/statistikZH/covid19_drop/master/Chiffres%20%20COVID-19%20Valais.xlsx'
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
    if row['Nb de nouvelles sorties'] is not None:
        dd.recovered = sum(r['Nb de nouvelles sorties'] for r in rows[:i+1])

    print('-' * 10)
    print(dd)
