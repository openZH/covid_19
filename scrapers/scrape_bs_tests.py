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
    td.positive_tests = row['Positive Tests'] or None
    td.negative_tests = row['Negative Tests'] or None
    td.total_tests = row['Total Tests'] or None
    td.positivity_rate = row['Anteil positive Tests in Prozent'] or None
    if td:
        # prettify output a bit
        td.positivity_rate = round(10 * float(td.positivity_rate)) / 10
        print(td)
