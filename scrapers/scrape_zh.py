#!/usr/bin/env python3

import csv
import re
from io import StringIO
import scrape_common as sc

url = "https://www.zh.ch/de/gesundheit/coronavirus.html"
csv_url = 'https://raw.githubusercontent.com/openzh/covid_19/master/fallzahlen_kanton_zh/COVID19_Fallzahlen_Kanton_ZH_total.csv'
d_csv = sc.download(csv_url, silent=True)
reader = csv.DictReader(StringIO(d_csv), delimiter=',')

is_first = True
for row in reader:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='ZH', url=url)
    dd.datetime = f"{row['date']} {row['time']}"
    dd.cases = row['ncumul_conf']
    dd.deaths = row['ncumul_deceased']
    dd.hospitalized = row['current_hosp']
    dd.vent = row['current_vent']
    dd.icu = row['current_icu']
    dd.isolated = row['current_isolated']
    dd_iso_q.quarantined = row['current_quarantined']
    print(dd)
    



