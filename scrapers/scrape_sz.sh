#!/usr/bin/env python3

import scrape_common as sc

print('SZ')

d = sc.download('https://www.sz.ch/behoerden/information-medien/medienmitteilungen/coronavirus.html/72-416-412-1379-6948')
sc.timestamp()

# 2020-03-25
"""        <li> <p>Aktuelle Fallzahlen im Kanton Schwyz (Stand: 25. März 2020): 99 Infizierte, 10 Genesene</p> </li> """

print('Date and time:', sc.find(r'Stand: ([^)]+)\)', d))
print('Confirmed cases:', sc.find(r': ([0-9]+) Infizierte', d))
print('Recovered:', sc.find(r', ([0-9]+) Genesene', d))
