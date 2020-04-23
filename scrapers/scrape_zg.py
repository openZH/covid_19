#!/usr/bin/env python3

import collections
import csv
from io import StringIO
import scrape_common as sc

print('ZG')
sc.timestamp()

d_csv = sc.download('https://raw.githubusercontent.com/statzg/glibraries-stat-zug/master/daten/result-themen-14-03-01.csv')
"""
"Typ","Datum","Anzahl","Stand","Meta","Type","Content"
"Fallzahl","22.04.2020","176","2020-04-22 08:00:00",NA,NA,NA
"Fallzahl","23.04.2020","178","2020-04-23 08:00:00",NA,NA,NA
"Hospitalisierte","22.04.2020","6","2020-04-22 08:00:00",NA,NA,NA
"Hospitalisierte","23.04.2020","5","2020-04-23 08:00:00",NA,NA,NA
"Hospitalisierte in Intensivpflege","22.04.2020","3","2020-04-22 08:00:00",NA,NA,NA
"Hospitalisierte in Intensivpflege","23.04.2020","3","2020-04-23 08:00:00",NA,NA,NA
"Genesene","22.04.2020","131","2020-04-22 08:00:00",NA,NA,NA
"Genesene","23.04.2020","133","2020-04-23 08:00:00",NA,NA,NA
"Todesfälle","22.04.2020","8","2020-04-22 08:00:00",NA,NA,NA
"Todesfälle","23.04.2020","8","2020-04-23 08:00:00",NA,NA,NA
NA,NA,NA,NA,"1","datatypes","string,date,integer"
NA,NA,NA,NA,"1","title",""
NA,NA,NA,NA,"1","subtitle",""
NA,NA,NA,NA,"1","description","Aufgrund der kleinen Fallzahlen im Kanton Zug können die Veränderungen von Tag zu Tag stark schwanken. Veränderungen dürfen deshalb nicht als Trend interpretiert werden. Die Zahlen der Hospitalisierten umfasst jeweils auch Hospitalisierte in Intensivpflege. Die Fallzahlen und Todesfälle werden im Zeitverlauf summiert, die Hospitalisierungen umfassen nur die Hospitalisierungen des jeweiligen Tags."
NA,NA,NA,NA,"1","source","Kanton Zug, Amt für Gesundheit"
"""
reader = csv.DictReader(StringIO(d_csv), delimiter=',')
data = collections.defaultdict(dict)
for row in reader:
    if row['Typ'] == 'NA' or row['Datum'] == 'NA':
        continue
    data[row['Stand']][row['Typ']] = row['Anzahl']
days = list(data.keys())
last_day = data[days[-1]]
print('Date and time:', days[-1])
print('Confirmed cases:', last_day['Fallzahl'])
print('Hospitalized:', last_day['Hospitalisierte'])
print('ICU:', last_day['Hospitalisierte in Intensivpflege'])
print('Recovered:', last_day['Genesene'])
print('Deaths:', last_day['Todesfälle'])
