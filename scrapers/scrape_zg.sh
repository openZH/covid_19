#!/usr/bin/env python3

import scrape_common as sc

print('ZG')
d = sc.download('https://www.zg.ch/behoerden/gesundheitsdirektion/amt-fuer-gesundheit/corona')
sc.timestamp()
d = sc.filter(r'Infizierte Personen|Genesene Personen|Verstorbene Personen|Stand:', d)

# 2020-03-23
"""
      <p>Infizierte Personen: 62</p>
<p>Genesene Personen: 10</p>
<p>Verstorbene Personen: 0</p>
<p>Stand: 23.3.2020, 8.00 Uhr</p>
"""

print('Date and time:', sc.find(r'Stand:? ([^<]+ Uhr)<', d))
print('Confirmed cases:', sc.find(r'Infizierte Personen:? ([0-9]+)<', d))
print('Deaths:', sc.find(r'Verstorbene Personen:? ([0-9]+)<', d))
print('Recovered:', sc.find(r'Genesene Personen:? ([0-9]+)<', d))
