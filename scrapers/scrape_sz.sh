#!/usr/bin/env python3

import scrape_common as sc

print('SZ')

d = sc.download('https://www.sz.ch/behoerden/information-medien/medienmitteilungen/coronavirus.html/72-416-412-1379-6948')
sc.timestamp()

# 2020-03-25
"""        <li> <p>Aktuelle Fallzahlen im Kanton Schwyz (Stand: 25. März 2020): 99 Infizierte, 10 Genesene</p> </li> """

# 2020-03-26, morning
"""        <li> <p>Bestätigte Fälle im Kanton Schwyz (Stand: 26. März 2020): 99</p> </li> """

# 2020-03-26, afternoon
"""        <li> <p>99 bestätigte Fälle im Kanton Schwyz, 10 Genesene (Stand: 26. März 2020)</p> </li> """



print('Date and time:', sc.find(r'Stand: ([^)]+)\)', d))
cases = sc.find(r': ([0-9]+) Infizierte', d)
if not cases:
  cases = sc.find(r'Bestätigte Fälle .*?\): ([0-9]+)<', d)
if not cases:
  cases = sc.find(r'>([0-9]+) bestätigte Fälle', d)
print('Confirmed cases:', cases)

recovered = sc.find(r', ([0-9]+) Genesene', d)
if recovered:
  print('Recovered:', recovered)
