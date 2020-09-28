#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import datetime
import scrape_common as sc


data_url = 'https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp'
d = sc.download(data_url, silent=True)
soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find('a', href=re.compile(r'\.xlsx$'))['href']
if not xls_url.startswith('http'):
    xls_url = f'https://www.ag.ch{xls_url}'
    
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
rows = sc.parse_xls(xls, sheet_name='2. Contact Tracing', header_row=2)
for row in rows:
    if not isinstance(row['A'], datetime.datetime):
        continue


    dd = sc.DayData(canton='AG', url=xls_url)
    dd.datetime = f"{row['A'].date().isoformat()} {row['A'].time().isoformat()}"
    dd.isolated = row['Gesamtzahl aktuell betreuter Personen']
    dd.quarantined = row['Gesamtzahl aktuell betreuter Personen5']
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
    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)
