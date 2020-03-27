#!/usr/bin/env python3

import scrape_common as sc

print('ZH')
d = sc.download("https://gd.zh.ch/internet/gesundheitsdirektion/de/themen/coronavirus.html")
sc.timestamp()
d = sc.filter(r"Im Kanton Zürich sind zurzeit|\(Stand|Total ([0-9]+) Todesfälle", d)
#                                 <h2>Aktuelle Situation im Kanton Zürich (24.3.2020, 9.30 Uhr)</h2>
#                         
#                         
#                         
#                         <p>Im Kanton Zürich sind zurzeit 1211 Personen positiv auf das Coronavirus getestet worden. Total 5 Todesfälle (78-jährig, 80, 88, 96, 97).</p>
# <p>(Stand 24.3.2020, 9.30 Uhr)</p>


# 2020-03-26
"""
				<h2>Aktuelle Situation im Kanton Zürich (26.3.2020, 9.30 Uhr)</h2>
			
			
			
			<p>Im Kanton Zürich sind zurzeit 1476 Personen positiv auf das Coronavirus getestet worden.</p>
<p>152 positiv Getestete befinden sich in Spitalbehandlung, davon werden 32 künstlich beatmet.</p>
<p>Total 9 Todesfälle (78-jährig, 78, 80, 80, 85, 88, 90, 96, 97).</p>
<p>Die Gesundheitsdirektion beschafft sich eine Maschine, die täglich automatisch bis zu 32'000 FFP2-Schutzmasken herstellen kann. In der zweiten Hälfte des Monats April ist die Maschine betriebsbereit.&nbsp;</p>
<p>(Stand 26.3.2020, 9.30 Uhr)</p>
"""

print("Date and time:", sc.find('Stand (.+) Uhr', d))
print("Confirmed cases:", sc.find('Im .* Zürich .* ([0-9]+) Person(en)? posit', d))
deaths = sc.find('Im .* Zürich .* Total ([0-9]+) Todesfälle', d)
if not deaths:
  deaths = sc.find('Total ([0-9]+) Todesfälle', d)
print("Deaths:", deaths)
