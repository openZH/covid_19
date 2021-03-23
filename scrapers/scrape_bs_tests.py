#!/usr/bin/env python3

import csv
from io import StringIO
import scrape_common as sc


def prettify_positivity_rate(positivity_rate):
    if not positivity_rate:
        return None
    return round(10 * float(positivity_rate)) / 10


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

    td.pcr_positive_tests = row['Positive PCR Tests'] or None
    td.pcr_negative_tests = row['Negative PCR Tests'] or None
    td.pcr_total_tests = row['Total PCR Tests'] or None
    td.pcr_positivity_rate = row['Anteil positive PCR Tests in Prozent'] or None

    td.ag_positive_tests = row['Positive Antigen Schnelltests'] or None
    td.ag_negative_tests = row['Negative Antigen Schnelltests'] or None
    td.ag_total_tests = row['Total Antigen Schnelltests'] or None
    td.ag_positivity_rate = row['Anteil positive Antigen Schnelltests in Prozent'] or None

    if td:
        td.positivity_rate = prettify_positivity_rate(td.positivity_rate)
        td.pcr_positivity_rate = prettify_positivity_rate(td.pcr_positivity_rate)
        td.ag_positivity_rate = prettify_positivity_rate(td.ag_positivity_rate)
        print(td)
