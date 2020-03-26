#!/usr/bin/env python3

import scrape_common as sc

print('GL')
d = sc.download('https://www.gl.ch/verwaltung/finanzen-und-gesundheit/gesundheit/coronavirus.html/4817')
sc.timestamp()

d = sc.filter(r'Fallzahlen Kanton Glarus.+Update|Best(ä|&auml;)tigte F(ä|&auml;)lle|Wahrscheinliche F(ä|&auml;)lle|Hospitalisierungen', d)

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

print('Date and time:', sc.find(r'Update (.+ Uhr)\)<', d))
print('Confirmed cases:', sc.find(r'Bestätigte Fälle: <strong>([0-9]+)(&nbsp;)?<', sc.filter(r'Best(ä|&auml;)tigte F(ä|&auml;)lle', d)))
print('Hospitalized:', sc.find(r'Hospitalisierungen: <strong>([0-9]+)(&nbsp;)?<', sc.filter(r'Hospitalisierungen', d)))
