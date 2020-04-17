#!/usr/bin/env python3

from bs4 import BeautifulSoup
import collections
import csv
from io import StringIO
import re
import scrape_common as sc

print('ZG')
d = sc.download('https://www.zg.ch/behoerden/gesundheitsdirektion/amt-fuer-gesundheit/corona')
sc.timestamp()
soup = BeautifulSoup(d, 'html.parser')
d = sc.filter(r'Infizierte Personen|Genesene Personen|Verstorbene Personen|Stand:', d)
date_time_string = sc.find(r'Stand:? ([^<]+ Uhr)<', d)
last_update = None
matches = re.search(r'(\d+)\.(\d+)\.(\d+)', date_time_string)
if matches:
    last_update = f"{int(matches[1]):02d}.{int(matches[2]):02d}.{matches[3]}"

detailed_stats = soup.find("a", text=re.compile("Detaillierte Statistik"))

found_last_day = False

if detailed_stats and last_update is not None:
    d_detailed_stats = sc.download(detailed_stats['href'])
    csv_path = sc.find(r'csv_path:"([^"]+)"', d_detailed_stats)
    if csv_path.startswith('/'):
        csv_url = f"https://www.zg.ch/{csv_path}"
    else:
      csv_url = csv_path
    d_csv = sc.download(csv_url)
    sc.timestamp()
    """
"Typ","Datum","Anzahl","Meta","Type","Content"
"Fallzahl","01.03.2020","0",NA,NA,NA
...
"Fallzahl","09.04.2020","165",NA,NA,NA
"Hospitalisierte","01.03.2020","0",NA,NA,NA
...
"Hospitalisierte","09.04.2020","13",NA,NA,NA
"Hospitalisierte in Intensivpflege","01.03.2020","0",NA,NA,NA
...
"Hospitalisierte in Intensivpflege","09.04.2020","9",NA,NA,NA
"Genesene","01.03.2020","0",NA,NA,NA
...
"Genesene","09.04.2020","69",NA,NA,NA
"Todesfälle","01.03.2020","0",NA,NA,NA
...
"Todesfälle","09.04.2020","3",NA,NA,NA
NA,NA,NA,"1","datatypes","string,date,integer"
NA,NA,NA,"1","title",""
NA,NA,NA,"1","subtitle",""
NA,NA,NA,"1","description","Aufgrund der kleinen Fallzahlen im Kanton Zug können die Veränderungen von Tag zu Tag stark schwanken. Veränderungen dürfen deshalb nicht als Trend interpretiert werden. Die Zahlen der Hospitalisierten umfasst jeweils auch Hospitalisierte in Intensivpflege. Die Fallzahlen und Todesfälle werden im Zeitverlauf summiert, die Hospitatilierungen umfassen nur die Hospitalisierungen des jeweiligen Tags."
NA,NA,NA,"1","source","Kanton Zug, Amt für Gesundheit"
"""
    reader = csv.DictReader(StringIO(d_csv), delimiter=',')
    data = collections.defaultdict(dict)
    for row in reader:
        if row['Typ'] == 'NA' or row['Datum'] == 'NA':
            continue
        data[row['Datum']][row['Typ']] = row['Anzahl']
    days = list(data.keys())
    last_day = data[days[-1]]
    if (last_day == last_update and
        'Fallzahl' in last_day and
        'Hospitalisierte' in last_day and
        'Hospitalisierte in Intensivpflege' in last_day and
        'Genesene' in last_day and
        'Todesfälle' in last_day):
        found_last_day = True
        print('Date and time', days[-1])
        print('Confirmed cases:', last_day['Fallzahl'])
        print('Hospitalized:', last_day['Hospitalisierte'])
        print('ICU:', last_day['Hospitalisierte in Intensivpflege'])
        print('Recovered:', last_day['Genesene'])
        print('Deaths:', last_day['Todesfälle'])

# 2020-03-23
"""
      <p>Infizierte Personen: 62</p>
<p>Genesene Personen: 10</p>
<p>Verstorbene Personen: 0</p>
<p>Stand: 23.3.2020, 8.00 Uhr</p>
"""
if not found_last_day:
    print('Date and time:', date_time_string)
    print('Confirmed cases:', sc.find(r'Infizierte Personen:? ([0-9]+)<', d))
    print('Deaths:', sc.find(r'Verstorbene Personen:? ([0-9]+)<', d))
    print('Recovered:', sc.find(r'Genesene Personen:? ([0-9]+)<', d))
