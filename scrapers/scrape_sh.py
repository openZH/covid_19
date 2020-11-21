#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import scrape_common as sc
import scrape_sh_common as shc

# A JavaScript content loaded from https://sh.ch/CMS/Webseite/Kanton-Schaffhausen/Beh-rde/Verwaltung/Departement-des-Innern/Gesundheitsamt-3209198-DE.html
xls_url = shc.get_sh_url_from_json('https://sh.ch/CMS/content.jsp?contentid=3666465&language=DE')
xls = sc.xlsdownload(xls_url, silent=True)

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

    print('SH')
    sc.timestamp()
    print('Downloading:', xls_url)
    if isinstance(row['Uhrzeit'], datetime.datetime):
        print('Date and time:', row['Datum'].date().isoformat(), row['Uhrzeit'].time().isoformat())
    elif row['Uhrzeit']:
        print('Date and time:', row['Datum'].strftime('%d.%m.%Y'), row['Uhrzeit'])
    else:
        print('Date and time:', row['Datum'].date().isoformat())

    print('Confirmed cases:', row['Positiv'])
    if sc.represents_int(row.search(r'Hospitalisation isoliert\s+bestätigt.*$')) and sc.represents_int(row.search(r'Hospitalisiert.*Intensiv.*$')):
        print('Hospitalized:', (row.search(r'Hospitalisation isoliert\s+bestätigt.*$') + row.search(r'Hospitalisiert.*Intensiv.*$')))
        print('ICU:', row.search(r'Hospitalisiert.*Intensiv.*$'))
    if row['Verstorben'] is not None:
        print('Deaths:', row['Verstorben'])

    isolated = row.search(r'Anzahl Personen\s+in Isolation.*')
    if isolated is not None:
        print('Isolated:', isolated)
    quarantined = row.search(r'Anzahl Personen\s+in Quarantäne\s+.*Kontaktpersonen.*')
    if quarantined is not None:
        print('Quarantined:', quarantined)
    quarantined_risk = row.search(r'Anzahl Personen\s+in Quarantäne\s+.*Rückkehr.*Risikoländer.*')
    if quarantined_risk is not None:
        print('Quarantined risk area travel:', quarantined_risk)
