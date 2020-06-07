#!/usr/bin/env python3

import collections
import csv
from io import StringIO
import scrape_common as sc

csv_url = 'https://raw.githubusercontent.com/statzg/glibraries-stat-zug/master/daten/result-themen-14-03-01.csv'
d_csv = sc.download(csv_url, silent=True)
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

csv_url = 'https://www.zg.ch/behoerden/gesundheitsdirektion/statistikfachstelle/daten/themen/result-themen-14-03-06-e1.csv'
d_csv = sc.download(csv_url, silent=True)
reader = csv.DictReader(StringIO(d_csv), delimiter=',')
data2 = collections.defaultdict(dict)
for row in reader:
    if row['Typ'] == 'NA' or row['Datum'] == 'NA':
        continue
    date = sc.date_from_text(row['Datum'])
    data2[date.isoformat()][row['Typ']] = row['Anzahl']

main_url = 'https://www.zg.ch/behoerden/gesundheitsdirektion/statistikfachstelle/themen/gesundheit/corona'
is_first = True
for day in days:
    if not is_first:
        print('-' * 10)
    is_first = False

    print('ZG')
    sc.timestamp()
    print('Downloading:', main_url)
    print('Date and time:', day)
    print('Confirmed cases:', data[day]['Fallzahl'])
    print('Hospitalized:', data[day]['Hospitalisierte'])
    print('ICU:', data[day]['Hospitalisierte in Intensivpflege'])
    print('Recovered:', data[day]['Genesene'])
    print('Deaths:', data[day]['Todesfälle'])
    date = sc.date_from_text(day).isoformat()
    if date in data2 is not None and 'Positiv getestete Personen' in data2[date] is not None:
        print('Isolated:', data2[date]['Positiv getestete Personen'])
    if date in data2 and 'Total Personen' in data2[date] is not None:
        print('Quarantined:', data2[date]['Total Personen'])
