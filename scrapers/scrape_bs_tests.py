#!/usr/bin/env python3

import csv
from io import StringIO
import scrape_common as sc


url = 'https://data.bs.ch/explore/dataset/100094/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B'
data = sc.download(url, silent=True)

reader = csv.DictReader(StringIO(data), delimiter=';')
for row in reader:
    td = sc.TestData(canton='BS', url=url)
    td.start_date = row['Datum']
    td.end_date = row['Datum']
    td.positive_tests = int(row['Positive Tests'])
    td.negative_tests = int(row['Negative Tests'])
    td.positivity_rate = float(row['Anteil positive Tests in Prozent'])
    # prettify output a bit
    td.positivity_rate = round(10 * td.positivity_rate) / 10
    if td:
        print(td)
