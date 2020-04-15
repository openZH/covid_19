#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc

print('SO')
d = sc.download("https://corona.so.ch/index.php?id=27979")
sc.timestamp()
soup = BeautifulSoup(d, 'html.parser')
data_table = soup.find('h2', text=re.compile("Situation Kanton Solothurn")).find_next("table")
headers = [cell.string for cell in data_table.find('tr').find_all('th')]
data = {}
for row in data_table.find_all('tr'):
    col_num = 0
    for cell in row.find_all(['td']):
        if headers[col_num] == 'Datum':
            data['Date'] = cell.string
        elif headers[col_num] == 'Zeit':
            data['Time'] = cell.string
        elif headers[col_num] == 'Bestätigte Fälle (kumuliert)':
            data['Cases'] = cell.string
        elif headers[col_num] == 'Todesfälle (kumuliert)':
            data['Deaths'] = cell.string
        elif headers[col_num] == 'Im Kanton Hospitalisierte Personen':
            data['Hospitalized'] = cell.string
        col_num += 1

if 'Date' in data and 'Time' in data and 'Cases' in data and 'Hospitalized' in data and 'Deaths' in data:
    print(f"Date and time: {data['Date']} {data['Time']}")
    print(f"Confirmed cases: {data['Cases']}")
    print(f"Hospitalized: {data['Hospitalized']}")
    print(f"Deaths: {data['Deaths']}")

else:
    d = sc.download("https://corona.so.ch/")
    d = sc.filter("Situation Kanton Solothurn.*Stand|Anzahl positiv getesteter Erkrankungsfälle|Verstorben:", d)
    d = d.replace('<strong>', '').replace('</strong>', '')

    # 2020-03-23
    """
 <p class="bodytext"><strong>Situation Kanton Solothurn (Stand 23.03.2020, 12:00)</strong></p><ul><li>Anzahl positiv getesteter Erkrankungsfälle: 95 Personen</li> 	<li>Verstorben:<strong> </strong>1 Person</li></ul><p class="bodytext"> </p></div></div>
"""
    # 2020-04-02
    """
 <p class="bodytext"><strong>Situation Kanton Solothurn (Stand 02.04.2020, 0:00 Uhr)</strong></p><ul><li>Anzahl positiv getesteter Erkrankungsfälle: 227 (+11 im Vergleich zum Vortag)</li> 	<li>Verstorbene Personen:<strong> </strong>3 (keine Veränderung im Vergleich zum Vortag)</li></ul><p class="bodytext"> </p></div></div>
"""
    # 2020-04-03
    """
<p class="bodytext"><strong>Situation Kanton Solothurn (Stand 03.04.2020, 0:00 Uhr)</strong></p><ul><li>Anzahl positiv getesteter Erkrankungsfälle: 237 (+10 im Vergleich zum Vortag)</li> 	<li>Im Kanton hospitalisierte Patientinnen und Patienten: 17 (+3 im Vergleich zum Vortag)</li> 	<li>Verstorbene Personen:<strong> </strong>3 (keine Veränderung im Vergleich zum Vortag)</li></ul><p class="bodytext"> </p></div></div>
"""

    print("Date and time:", sc.find(r'\(Stand ([^\)]+)\)<', d))
    print("Confirmed cases:", sc.find(r'Anzahl\s*positiv\s*getesteter\s*Erkrankungsfälle\s*:\s*([0-9]+)\b', d))
    print("Hospitalized:", sc.find(r'Im\s*Kanton\s*hospitalisierte\s*(?:Patientinnen und Patienten|[^:]*)\s*:\s*([0-9]+)\b', d))
    print("Deaths:", sc.find(r'Verstorben(?:e Personen)?\s*:\s*([0-9]+)\b', d))
