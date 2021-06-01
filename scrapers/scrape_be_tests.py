#!/usr/bin/env python3

import csv
from io import StringIO
import scrape_common as sc

url = 'https://covid-kennzahlen.apps.be.ch/#/de/cockpit'

csv_url = 'https://raw.githubusercontent.com/openDataBE/covid19Data/develop/vortag_tests.csv'
d = sc.download(csv_url, silent=True)
reader = csv.DictReader(StringIO(d), delimiter=',')
for row in reader:
    td = sc.TestData(canton='BE', url=url)
    date = sc.date_from_text(row['datum']).isoformat()
    td.start_date = date
    td.end_date = date
    td.total_tests = row['durchgefuehrte_tests']
    td.positive_tests = row['positive_tests']
    td.positivity_rate = row['positivitaetsrate']
    print(td)
