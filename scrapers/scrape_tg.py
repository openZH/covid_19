#!/usr/bin/env python3

import csv
from io import StringIO
import scrape_common as sc
import scrape_tg_common as stc


url = stc.get_tg_main_csv_url()
d_csv = sc.download(url, silent=True)

reader = csv.DictReader(StringIO(d_csv), delimiter=';')
is_first = True
for row in reader:
    if not row['date']:
        continue
    if not is_first:
        print('-' * 10)
    is_first = False
    dd = sc.DayData(canton='TG', url=row['source'])
    dd.datetime = f"{row['date']} {row['time']}"
    dd.cases = row['ncumul_conf']
    dd.deaths = row['ncumul_deceased']
    dd.hospitalized = row['current_hosp']
    dd.new_hosp = row['new_hosp']
    dd.recovered = row['ncumul_released']
    dd.icu = row['current_ICU']
    dd.isolated = row['num_isolated']
    print(dd)
