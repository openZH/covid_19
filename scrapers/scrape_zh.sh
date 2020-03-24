#!/usr/bin/env python3

from scrape_common import *

print('ZH')
d = download("https://gd.zh.ch/internet/gesundheitsdirektion/de/themen/coronavirus.html")
timestamp()
d = filter(r"Im Kanton Zürich sind zurzeit|\(Stand", d)
#                                 <h2>Aktuelle Situation im Kanton Zürich (24.3.2020, 9.30 Uhr)</h2>
#                         
#                         
#                         
#                         <p>Im Kanton Zürich sind zurzeit 1211 Personen positiv auf das Coronavirus getestet worden. Total 5 Todesfälle (78-jährig, 80, 88, 96, 97).</p>
# <p>(Stand 24.3.2020, 9.30 Uhr)</p>


print("Date and time:", find('Stand (.+) Uhr', d))
print("Confirmed cases:", find('Im .* Zürich .* ([0-9]+) Person(en)? posit', d))
print("Deaths:", find('Im .* Zürich .* Total ([0-9]+) Todesfälle', d))
