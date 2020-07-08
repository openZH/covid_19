#!/usr/bin/env python3

import csv
from io import StringIO
import scrape_common as sc

url = "https://www.zh.ch/de/gesundheit/coronavirus.html#-1310230111"

# get quarantined and isolated from website
dd_iso_q = sc.DayData(canton='ZH', url=url)
d = sc.download(url, silent=True)

# 2020-04-07
"""
<h3>Die Situation im Kanton Zürich am Dienstag, 7. April 2020, 15.00 Uhr</h3>
"""

date_time_info = sc.find('publiziert am (.+) Uhr', d)
date_time_info = date_time_info.replace(' um', ',') + ' Uhr'
dd_iso_q.datetime = date_time_info
dd_iso_q.isolated = sc.find(r'"-790711785">(\d+)</h4>', d)
dd_iso_q.quarantined = sc.find(r'-790704311">(\d+)</h4>', d)

print(dd_iso_q)

csv_url = 'https://raw.githubusercontent.com/openzh/covid_19/master/fallzahlen_kanton_zh/COVID19_Fallzahlen_Kanton_ZH_total.csv'
d_csv = sc.download(csv_url, silent=True)
reader = csv.DictReader(StringIO(d_csv), delimiter=',')

for row in reader:
    print('-' * 10)
    dd = sc.DayData(canton='ZH', url=url)
    dd.datetime = f"{row['date']} {row['time']}"
    dd.cases = row['ncumul_conf']
    dd.deaths = row['ncumul_deceased']
    dd.hospitalized = row['current_hosp']
    dd.vent = row['current_vent']
    print(dd)
    



