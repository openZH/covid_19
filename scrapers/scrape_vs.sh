#!/usr/bin/env python3

import scrape_common as sc

print('VS')
d = sc.download('https://www.vs.ch/de/web/coronavirus')
sc.timestamp()
d = sc.filter(r'bestätigte Fälle', d)

# <p>21.03.2020: Derzeit gibt es 359 bestätigte Fälle von Coronavirus-Infektionen im Kanton.&nbsp;Insgesamt hat das Virus bisher den Tod von 9&nbsp;Personen im Wallis verursacht.</p>

print('Date and time:', sc.find(r'<p>([0-9]+\.[0-9]+\.202[0-2]): Derzeit', d))
print('Confirmed cases:', sc.find(r'es ([0-9]+) bestätigte Fälle', d))
print('Deaths:', sc.find(r'Tod von ([0-9]+)( |&nbsp;)Person', d))
