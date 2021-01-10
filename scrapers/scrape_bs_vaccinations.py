#!/usr/bin/env python3

import csv
from io import StringIO
import scrape_common as sc


url = 'https://data.bs.ch/explore/dataset/100111/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B'
data = sc.download(url, silent=True)

reader = csv.DictReader(StringIO(data), delimiter=';')
for row in reader:
    vd = sc.VaccinationData(canton='BS', url=url)
    vd.date = row['Datum']
    vd.total_vaccinations = row['Total geimpfte Personen ']
    if vd:
        print(vd)
