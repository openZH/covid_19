#!/usr/bin/env python3

import collections
import csv
from io import StringIO
import scrape_common as sc


csv_url = 'https://www.zg.ch/behoerden/gesundheitsdirektion/statistikfachstelle/daten/themen/result-themen-14-03-12.csv'
d_csv = sc.download(csv_url, silent=True)
"""
"Datum","Typ","Anzahl","Meta","Type","Content"
"23.12.2020","Total verimpfte Dosen","250",NA,NA,NA
"24.12.2020","Total verimpfte Dosen","250",NA,NA,NA
"""

reader = csv.DictReader(StringIO(d_csv), delimiter=',')
data = collections.defaultdict(dict)
for row in reader:
    if row['Datum'] == 'NA':
        continue
    date = sc.date_from_text(row['Datum'])
    if date not in data:
        vd = sc.VaccinationData(canton='ZG', url=csv_url)
        vd.start_date = date.isoformat()
        vd.end_date = date.isoformat()
        data[date] = vd
    if row['Typ'] == 'Total verimpfte Dosen':
        data[date].total_vaccinations = row['Anzahl']
    elif row['Typ'] == 'Total 1. Impfung':
        data[date].first_doses = row['Anzahl']
    elif row['Typ'] == 'Total 2. Impfung':
        data[date].second_doses = row['Anzahl']

dates = list(data.keys())
for date in dates:
    print(data[date])
