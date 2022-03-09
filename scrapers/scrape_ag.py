#!/usr/bin/env python3

import datetime
import scrape_common as sc
import scrape_ag_common as sac


xls_url = sac.get_ag_xls_url()
xls = sc.xlsdownload(xls_url, silent=True)
is_first = True

# quarantine_riskareatravel
"""
rows = sc.parse_xls(xls, sheet_name='5. Quarantäne nach Einreise', header_row=2)
for row in rows:
    if not isinstance(row['A'], datetime.datetime):
        continue


    dd = sc.DayData(canton='AG', url=xls_url)
    dd.datetime = f"{row['A'].date().isoformat()} {row['A'].time().isoformat()}"
    dd.quarantine_riskareatravel = row['Gesamtzahl aktuell betreuter Personen']
    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)
"""

# quarantine + isolation
rows = sc.parse_xls(xls, sheet_name='2. Contact Tracing', header_row=2)
for row in rows:
    if not isinstance(row['A'], datetime.datetime):
        continue

    dd = sc.DayData(canton='AG', url=xls_url)
    dd.datetime = f"{row['A'].date().isoformat()} {row['A'].time().isoformat()}"
    isolated = row['Gesamtzahl aktuell betreuter Personen']
    if sc.represents_int(isolated):
        dd.isolated = isolated
    #dd.quarantined = row['Gesamtzahl aktuell betreuter Personen5']
    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)

# cases + hospitalization
rows = sc.parse_xls(xls, sheet_name='1. Covid-19-Daten', header_row=2)
for row in rows:
    if not isinstance(row['A'], datetime.datetime):
        continue

    dd = sc.DayData(canton='AG', url=xls_url)
    dd.datetime = f"{row['A'].date().isoformat()} {row['A'].time().isoformat()}"
    dd.cases = row['Gesamtzahl']

    non_icu = row['Bestätigte Fälle Bettenstation (ohne IPS/IMC)']
    icu = row['Bestätigte Fälle Intensivpflegestation (IPS)']
    icf = row['Bestätigte Fälle Intermediate Care (IMC)']
    if sc.represents_int(non_icu) and sc.represents_int(icu) and sc.represents_int(icf):
        dd.hospitalized = int(non_icu) + int(icu) + int(icf)
        dd.icu = icu
        dd.icf = icf
    dd.deaths = row['Gesamtzahl21']
    dd.recovered = row['Gesamtzahl25']

    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)
