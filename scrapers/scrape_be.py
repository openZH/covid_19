#!/usr/bin/env python3

import csv
from io import StringIO
import re
import scrape_common as sc

url = 'https://covid-kennzahlen.apps.be.ch/#/de/cockpit'

csv_url = 'https://raw.githubusercontent.com/openDataBE/covid19Data/develop/total_faelle.csv'
d = sc.download(csv_url, silent=True)
reader = csv.DictReader(StringIO(d), delimiter=',')
is_first = True
for row in reader:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='BE', url=url)
    dd.datetime = row['datum']
    dd.cases = row['total_laborbestaetigte_faelle']
    dd.deaths = row['total_todesfaelle']
    print(dd)

csv_url = 'https://raw.githubusercontent.com/openDataBE/covid19Data/develop/spa_auslastung.csv'
d = sc.download(csv_url, silent=True)
reader = csv.DictReader(StringIO(d), delimiter=',')
is_first = True
for row in reader:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='BE', url=url)
    dd.datetime = row['datum']
    dd.hospitalized = row['personen_hospitalisiert']
    dd.vent = int(row['auf_intensivpflegestation_beatmet'])
    dd.icu = int(row['auf_intensivpflegestation_unbeatmet']) + dd.vent
    print(dd)

csv_url = 'https://raw.githubusercontent.com/openDataBE/covid19Data/develop/contact_tracing.csv'
d = sc.download(csv_url, silent=True)
reader = csv.DictReader(StringIO(d), delimiter=',')
is_first = True
for row in reader:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='BE', url=url)
    dd.datetime = row['datum']
    dd.quarantined = row['personen_in_quarantaene']
    dd.isolated = row['personen_in_isolation']
    print(dd)
