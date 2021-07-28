#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
from bs4 import BeautifulSoup
import scrape_common as sc
import scrape_sh_common as shc

main_url, xls = shc.get_sh_xlsx()

rows = sc.parse_xls(xls, header_row=0)
is_first = True
for row in rows:
    if not isinstance(row['Datum'], datetime.datetime):
        continue
    if not (row['Positiv'] or row.search(r'Hospitalisation isoliert\s+bestätigt.*$') or row.search(r'Hospitalisiert.*Intensiv.*$') or row['Verstorben']):
        continue

    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='SH', url=main_url)
    dd.datetime = row['Datum'].date().isoformat()
    dd.cases = row['Positiv']

    if sc.represents_int(row.search(r'Hospitalisation isoliert\s+bestätigt.*$')) and sc.represents_int(row.search(r'Hospitalisiert.*Intensiv.*$')):
        dd.hospitalized = row.search(r'Hospitalisation isoliert\s+bestätigt.*$') + row.search(r'Hospitalisiert.*Intensiv.*$')
        dd.icu = row.search(r'Hospitalisiert.*Intensiv.*$')
    if row['Verstorben'] is not None:
        dd.deaths = row['Verstorben']

    isolated = row.search(r'Anzahl Personen\s+in Isolation.*')
    if isolated is not None:
        dd.isolated = isolated
    quarantined = row.search(r'Anzahl Personen\s+in Quarantäne\s+.*Kontaktpersonen.*')
    if quarantined is not None:
        dd.quarantined = quarantined
    quarantined_risk = row.search(r'Anzahl Personen\s+in Quarantäne\s+.*Rückkehr.*Risikoländer.*')
    if quarantined_risk is not None:
        dd.quarantine_riskareatravel = quarantined_risk

    print(dd)
