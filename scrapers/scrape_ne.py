#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrape_common as sc

print('NE')

xls_url = 'https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Documents/Covid-19-Statistiques/COVID19_PublicationInternet.xlsx'
xls = sc.xlsdownload(xls_url)
sc.timestamp()
rows = sc.parse_xls(xls)
if rows:
    last_row = rows[-1]
    print('Date and time:', last_row['A'].date().isoformat())
    print('Confirmed cases:', last_row['Cumul'])
    print('Hospitalized:', last_row['Total des cas hospitalisés'])
    print('ICU:', int(last_row['Soins intensifs (intubés)']) + int(last_row['Soins intensifs (non intubés)']))
    print('Vent:', last_row['Soins intensifs (intubés)'])
    print('Deaths:', last_row['Cumul des décès'])
