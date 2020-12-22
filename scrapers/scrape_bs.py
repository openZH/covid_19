#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from io import StringIO
import scrape_common as sc

d_csv = sc.download('https://data.bs.ch/explore/dataset/100073/download/?format=csv&timezone=Europe/Zurich&lang=en&use_labels_for_header=false&csv_separator=,', silent=True)

reader = csv.DictReader(StringIO(d_csv), delimiter=',')
is_first = True
for row in reader:
    if not is_first:
        print('-' * 10)
    is_first = False
    dd = sc.DayData(canton='BS', url=row['source'])
    dd.datetime = f"{row['date']} {row['time']}"
    dd.cases = sc.safeint(row['ncumul_conf'])
    dd.new_hosp = row['new_hosp']
    dd.hospitalized = row['current_hosp']
    dd.icu = row['current_icu']
    dd.vent = row['current_vent']
    dd.recovered = row['ncumul_released']
    dd.deaths = row['ncumul_deceased']
    dd.isolated = row['current_isolated']
    dd.quarantined = row['current_quarantined']
    dd.confirmed_non_resident = row['ncumul_confirmed_non_resident']
    dd.hosp_non_resident = row['current_hosp_non_resident']
    dd.quarantine_riskareatravel = row['current_quarantined_riskareatravel']
    dd.quarantine_total = row['current_quarantined_total']
    dd.hosp_resident = row['current_hosp_resident']
    print(dd)
