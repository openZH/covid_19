#!/usr/bin/env python3

import datetime
import scrape_common as sc
import scrape_ag_common as sac


xls_url = sac.get_ag_xls_url()
xls = sc.xlsdownload(xls_url, silent=True)
is_first = True

# quarantine_riskareatravel
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

# quarantine + isolation
rows = sc.parse_xls(xls, sheet_name='2. Contact Tracing', header_row=0, skip_rows=2)
for row in rows:
    if not isinstance(row['A'], datetime.datetime):
        continue

    dd = sc.DayData(canton='AG', url=xls_url)
    dd.datetime = f"{row['A'].date().isoformat()} {row['A'].time().isoformat()}"
    dd.isolated = row['C']
    dd.quarantined = row['F']
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

    non_icu = row['Bestätigte Fälle ohne IPS/IMC']
    icu = row['Bestätigte Fälle IPS/IMC']
    if sc.represents_int(non_icu) and sc.represents_int(icu):
        dd.hospitalized = int(non_icu) + int(icu)
        dd.icu = icu
    dd.deaths = row['Gesamtzahl14']
    dd.recovered = row['Gesamtzahl17']

    # TODO: remove if source is fixed
    ignore_dates = [
        '2020-05-11',
        '2020-05-12',
        '2020-05-13',
        '2020-05-15',
        '2020-06-04',
        '2020-06-08',
        '2020-06-19',
        '2020-07-07',
        '2020-10-12',
    ]
    if row['A'].date().isoformat() in ignore_dates:
        dd.recovered = ''

    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)
