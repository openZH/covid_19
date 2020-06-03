#!/usr/bin/env python3

import re
import sys
from bs4 import BeautifulSoup
import scrape_common as sc

print('TG')
d = sc.download('https://www.tg.ch/news/fachdossier-coronavirus.html/10552')
sc.timestamp()
d = d.replace('&nbsp;', ' ')

# 2020-03-25
"""
      <li>Anzahl bestätigter Fälle: 96</li> 
     <p><em>Stand 25.3.20</em></p> 
"""

# 2020-04-03
"""
    <div class="box box--blue"> 
     <h2>Aktuelle Fallzahlen im Kanton Thurgau</h2> 
     <ul> 
      <li>Anzahl bestätigter Fälle: 198</li> 
      <li>davon&nbsp;5 verstorben</li> 
     </ul> 
     <p><em>Stand 3.4.20</em></p> 
    </div> 
"""

row_day, row_month, row_year = [int(n) for n in sc.find(r'Stand\s*([^<]+)<', d).split('.')]
main_date = f"{row_day:02d}.{row_month:02d}.20{row_year}"
print('Date and time:', main_date)
print('Confirmed cases:', sc.find(r'(?:Anzahl)?\s*bestätigter\s*Fälle:?\s*([0-9]+)\b', d))
print('Deaths:', sc.find(r'\b([0-9]+)\s*verstorb', d) or sc.find(r'Verstorben:?\s*([0-9]+)', d))
print('Hospitalized:', sc.find(r'Hospitalisiert:\s*([0-9]+)', d))
print('ICU:', sc.find(r'davon auf der Intensivstation:\s+([0-9]+)', d))

# fetch full data
soup = BeautifulSoup(d, 'html.parser')
try:
    fulldata_url = soup.find('a', string=re.compile(r'Corona-Virus-Entwicklung\s+im\s+Kanton\s+Thurgau'))['href']
except TypeError:
    print("Unable to determine full data url", file=sys.stderr)
    sys.exit(1)

d = sc.download(fulldata_url, silent=True)
d = d.replace('\n', ' ')
rows = {}
data = sc.find(
    r'<pre id="csv_COVID19" style="display: none;">\s*Datum,Positiv getestet,Hospitalisiert,Intensivstation\s+([^<]+)</pre>',
    d)
if data:
    for row in data.split(" "):
        c = row.split(',')
        if len(c) != 4:
            continue
        row_year, row_month, row_day = [int(n) for n in c[0].split('/')]
        row_date = f"{row_day:02d}.{row_month:02d}.{row_year}"
        rows[row_date] = {'hospitalized': c[2], 'icu': c[3]}

data = sc.find(
    r'<pre id="csv_COVID19_cum_TG_CH" style="display: none;">\s*Datum,Thurgau:Positiv Gestestete,Thurgau: Verstorbene,Schweiz: Positiv Gestestete,Schweiz: Verstorbene\s+([^<]+)</pre>',
    d
)
if data:
    for row in data.split(" "):
        c = row.split(',')
        if len(c) != 5:
            continue
        row_year, row_month, row_day = [int(n) for n in c[0].split('/')]
        row_date = f"{row_day:02d}.{row_month:02d}.{row_year}"
        dd = sc.DayData(canton='TG', url=fulldata_url)
        dd.datetime = row_date
        dd.cases = c[1]
        dd.deaths = c[2]
        if row_date in rows:
            dd.hospitalized = rows[row_date]['hospitalized']
            dd.icu = rows[row_date]['icu']
        if row_date != main_date:
            print('-' * 10)
            print(dd)

