#!/usr/bin/env python3

import collections
import csv
import datetime
from io import StringIO
import scrape_common as sc


csv_url = 'https://www.zg.ch/behoerden/gesundheitsdirektion/statistikfachstelle/daten/themen/result-themen-14-03-07-i2-k4-b1.csv'
d_csv = sc.download(csv_url, silent=True)
"""
"Woche","Geschlecht","Anzahl Fälle","Meta","Type","Content"
2020-05-25,"männlich","151",NA,NA,NA
2020-06-01,"männlich","117",NA,NA,NA
"""

reader = csv.DictReader(StringIO(d_csv), delimiter=',')
data = collections.defaultdict(dict)
for row in reader:
    if row['Woche'] == 'NA':
        continue
    date = sc.date_from_text(row['Woche'])
    if date not in data:
        data[date] = 0
    data[date] += int(row['Anzahl Fälle'])

days = list(data.keys())
for day in days:
    td = sc.TestData(canton='ZG', url=csv_url)
    td.start_date = day.isoformat()
    td.end_date = (day + datetime.timedelta(days=6)).isoformat()
    td.total_tests = data[day]
    print(td)
