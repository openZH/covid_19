#!/usr/bin/env python3

import scrape_common as sc

print('AG')

# From the new website:
d = sc.download('https://www.ag.ch/de/themen_1/coronavirus_2/alle_ereignisse/alle_ereignisse_1.jsp')
sc.timestamp()
d = sc.filter(r'Neues Lagebulletin', d)

# Use non-greedy match.
print('Date and time:', sc.find(r'class="timeline__time" datetime="00(.*?00)"', d))

print('Confirmed cases:', sc.find(r'zurzeit ([0-9]+) best(ä|&auml;)tigte F(ä|&auml;)lle', d))

print('Hospitalized:', sc.find(r' ([0-9]+) Person(en)? sind zurzeit hospitalisiert', d))

print('ICU:', sc.find(r' ([0-9]+) Person(en)? werden auf Intensivstationen behandelt', d))

print('Vent:', sc.find(r' ([0-9]+) Person(en)? k(ü|&uuml;)nstlich beatmet werden', d))

d = d.replace('zwei', '2')
print('Deaths:', sc.find(r'([0-9]+) Person(en)? an den Folgen des Coronavirus verstorben', d))
