#!/usr/bin/env python3

import re
from io import StringIO
from bs4 import BeautifulSoup
import csv
import scrape_common as sc

print('ZG')
d = sc.download('https://www.zg.ch/behoerden/gesundheitsdirektion/amt-fuer-gesundheit/corona')
sc.timestamp()
soup = BeautifulSoup(d, 'html.parser')
d = sc.filter(r'Infizierte Personen|Genesene Personen|Verstorbene Personen|Stand:', d)
date_time_string = sc.find(r'Stand:? ([^<]+ Uhr)<', d)
print('Date and time:', date_time_string)
last_update = None
matches = re.search(r'(\d+)\.(\d+)\.(\d+)', date_time_string)
if matches is not None:
    last_update = f"{int(matches[1]):02d}.{int(matches[2]):02d}.{matches[3]}"
    print("last_update:", last_update)

detailed_stats = soup.find("a", text=re.compile("Detaillierte Statistik"))

cases = None
deaths = None
recovered = None
if detailed_stats and last_update is not None:
    d_detailed_stats = sc.download(detailed_stats['href'])
    csv_path = sc.find(r'csv_path:"([^"]+)"', d_detailed_stats)
    csv_url = f"https://www.zg.ch/{csv_path}"
    d_csv = sc.download(csv_url)
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
    for row in reader:
        if row['Datum'] == last_update:
            if row['Typ'] == 'Fallzahl':
                cases = int(row['Anzahl'])
                print('Confirmed cases:', cases)
            elif row['Typ'] == 'Hospitalisierte':
                print('Hospitalized:', int(row['Anzahl']))
            elif row['Typ'] == 'Hospitalisierte in Intensivpflege':
                print('ICU:', int(row['Anzahl']))
            elif row['Typ'] == 'Genesene':
                recovered = int(row['Anzahl'])
                print('Recovered:', recovered)
            elif row['Typ'] == 'Todesfälle':
                deaths = int(row['Anzahl'])
                print('Deaths:', deaths)

# 2020-03-23
"""
      <p>Infizierte Personen: 62</p>
<p>Genesene Personen: 10</p>
<p>Verstorbene Personen: 0</p>
<p>Stand: 23.3.2020, 8.00 Uhr</p>
"""
if cases is None:
    print('Confirmed cases:', sc.find(r'Infizierte Personen:? ([0-9]+)<', d))
if deaths is None:
    print('Deaths:', sc.find(r'Verstorbene Personen:? ([0-9]+)<', d))
if recovered is None:
    print('Recovered:', sc.find(r'Genesene Personen:? ([0-9]+)<', d))
