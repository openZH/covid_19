#!/usr/bin/env python3

import scrape_common as sc

print('GL')
d = sc.download('https://www.gl.ch/verwaltung/finanzen-und-gesundheit/gesundheit/coronavirus.html/4817')
sc.timestamp()
d = d.replace('&nbsp;', ' ')
d = d.replace('&auml;', 'ä')

d = sc.filter(r'Fallzahlen\s*Kanton\s*Glarus.+Update|Bestätigte\s*Fälle|Wahrscheinliche\s*Fälle|Hospitalisierungen|Verstorbene', d)

#      <li><strong><a href="#Fallzahlen">Fallzahlen Kanton Glarus</a> (Update 22.03.2020, 13.30 Uhr)</strong></li> 
#...
#      <h2><strong><a id="Fallzahlen" name="Fallzahlen"></a>Coronavirus: Update Kanton Glarus</strong></h2> 
#      <h2>Bestätigte Fälle:&nbsp;<strong>31</strong>&nbsp;</h2> 
#      <h2>Wahrscheinliche Fälle:&nbsp;<strong>--</strong></h2> 
#      <h2>Hospitalisierungen:&nbsp;<strong>3</strong>&nbsp;</h2> 

# 2020-03-26
"""
      <h2><strong><a id="Fallzahlen" name="Fallzahlen"></a>Coronavirus: Update Kanton Glarus</strong><br /> (Stand: 25.3.2020, 13:30 Uhr)</h2> 
      <h2>Bestätigte Fälle: <strong>40&nbsp;</strong>(Vortag: 33)&nbsp;<br /> Hospitalisierungen: <strong>2</strong>&nbsp;(Vortag: 3)</h2> 
      <p>Die Zahl der bestätigten Fälle umfasst die seit Messbeginn erfassten Personen, die positiv auf COVID-19 getestet wurden. Bereits wieder genesene Personen sind in diesen Zahlen ebenfalls enthalten.</p> 
"""

# 2020-04-03
# Note, that it misses numbers for hospitalized on this day / time.
"""
      <h2><strong><a id="Fallzahlen" name="Fallzahlen"></a>Coronavirus: Update Kanton Glarus</strong><br /> (Stand: 3.4.2020, 13:30 Uhr)</h2> 
      <h2>Bestätigte Fälle: <strong>59&nbsp;</strong>(+1)&nbsp;<br /> Personen in Spitalpflege: <strong>5 </strong>(+/-0)&nbsp;<br /> Verstorbene Personen: <strong>2 </strong>(+/-0)</h2> 
"""


d = d.replace('<strong>', '').replace('</strong>', '')

print('Date and time:', sc.find(r'Update\s*(.+ Uhr)\)<', d))
print('Confirmed cases:', sc.find(r'Bestätigte\s*Fälle\s*:\s*([0-9]+)\b', d))
print('Hospitalized:', sc.find(r'(?:Hospitalisierungen|Personen in Spitalpflege)\s*:\s*([0-9]+)\b', d))
print('Deaths:', sc.find(r'Verstorbene\s*Personen\s*:\s*([0-9+])\b', d))
