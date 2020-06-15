#!/usr/bin/env python3

import collections
import csv
from io import StringIO
import scrape_common as sc

main_url = 'https://www.zg.ch/behoerden/gesundheitsdirektion/statistikfachstelle/themen/gesundheit/corona'

ct_csv_url = 'https://www.zg.ch/behoerden/gesundheitsdirektion/statistikfachstelle/daten/themen/result-themen-14-03-06-e1.csv'
d_csv = sc.download(ct_csv_url, silent=True)
"""
"Typ","Datum","Anzahl","Meta","Type","Content"
"Positiv getestete Personen","01.03.2020","0",NA,NA,NA
"Positiv getestete Personen","02.03.2020","2",NA,NA,NA
"Positiv getestete Personen","03.03.2020","2",NA,NA,NA
"Positiv getestete Personen","04.03.2020","2",NA,NA,NA
"Positiv getestete Personen","05.03.2020","3",NA,NA,NA
"Positiv getestete Personen","06.03.2020","3",NA,NA,NA
"Positiv getestete Personen","07.03.2020","5",NA,NA,NA
"Positiv getestete Personen","08.03.2020","7",NA,NA,NA
"Positiv getestete Personen","09.03.2020","7",NA,NA,NA
"Positiv getestete Personen","10.03.2020","7",NA,NA,NA
"Positiv getestete Personen","11.03.2020","6",NA,NA,NA
"Positiv getestete Personen","12.03.2020","6",NA,NA,NA
"Positiv getestete Personen","13.03.2020","8",NA,NA,NAh
"Positiv getestete Personen","14.03.2020","10",NA,NA,NA
"Positiv getestete Personen","15.03.2020","11",NA,NA,NA
"Positiv getestete Personen","16.03.2020","19",NA,NA,NA
"Positiv getestete Personen","17.03.2020","22",NA,NA,NA
"""

reader = csv.DictReader(StringIO(d_csv), delimiter=',')
data = collections.defaultdict(dict)
for row in reader:
    if row['Typ'] == 'NA' or row['Datum'] == 'NA':
        continue
    date = sc.date_from_text(row['Datum'])
    data[date.isoformat()][row['Typ']] = row['Anzahl']

days = list(data.keys())
is_first = True
for day in days:
    if not is_first:
        print('-' * 10)
    is_first = False

    print('ZG')
    sc.timestamp()
    print('Downloading:', main_url)
    print('Date and time:', day)
    print('Isolated:', data[day]['Positiv getestete Personen'])
    print('Quarantined:', data[day]['Kontaktpersonen'])

cases_csv_url = 'https://www.zg.ch/behoerden/gesundheitsdirektion/statistikfachstelle/daten/themen/result-themen-14-03-01-e1.csv'
d_csv = sc.download(cases_csv_url, silent=True)
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
for day in days:
    print('-' * 10)
    print('ZG')
    sc.timestamp()
    print('Downloading:', main_url)
    print('Date and time:', day)
    print('Confirmed cases:', data[day]['Fallzahl'])
    print('Hospitalized:', data[day]['Hospitalisierte'])
    print('ICU:', data[day]['Hospitalisierte in Intensivpflege'])
    print('Recovered:', data[day]['Genesene'])
    print('Deaths:', data[day]['Todesfälle'])
