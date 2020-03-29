#!/usr/bin/env python3

import scrape_common as sc

print('VS')
d = sc.download('https://www.vs.ch/de/web/coronavirus')
sc.timestamp()
d = sc.filter(r'best(ä|&auml;)tigte\s*F(ä|&auml;)lle', d)
d = d.replace('&nbsp;', ' ')

# 2020-03-21
"""
 <p>21.03.2020: Derzeit gibt es 359 bestätigte Fälle von Coronavirus-Infektionen im Kanton.&nbsp;Insgesamt hat das Virus bisher den Tod von 9&nbsp;Personen im Wallis verursacht.</p>
"""

# 2020-03-29
"""
... <p>29.03.2020: Derzeit gibt es 964&nbsp;bestätigte Fälle von Coronavirus-Infektionen im Kanton.&nbsp;Insgesamt hat das Virus bisher den Tod von 21&nbsp;Personen im Wallis verursacht. Eine Übersicht über die epidemiologische Lage im Wallis ist  ...
"""

print('Date and time:', sc.find(r'<p>\s*([0-9]+\.[0-9]+\.202[0-2]):\s*Derzeit', d))
print('Confirmed cases:', sc.find(r'\b([0-9]+)\s*best(ä|&auml;)tigte\s*F(ä|&auml;)lle', d))
print('Deaths:', sc.find(r'Tod\s*von\s*([0-9]+)\s*Person', d))
