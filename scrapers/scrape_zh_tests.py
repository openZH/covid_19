#!/usr/bin/env python3

import csv
from io import StringIO
import scrape_common as sc


url = 'https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_kanton_zh/COVID19_Anteil_positiver_Test_pro_KW.csv'
data = sc.download(url, silent=True)

reader = csv.DictReader(StringIO(data), delimiter=',')
for row in reader:
    td = sc.TestData(canton='ZH', url=url)
    td.start_date = row['Woche_von']
    td.end_date = row['Woche_bis']
    td.week = row['Kalenderwoche']
    td.positive_tests = int(row['Anzahl_positiv'])
    td.negative_tests = int(row['Anzahl_negativ'])
    td.positivity_rate = float(row['Anteil_positiv'])
    print(td)
