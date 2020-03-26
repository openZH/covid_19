#!/usr/bin/env python3

import scrape_common as sc

print('GR')
d = sc.download('https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/info/Seiten/Start.aspx')
sc.timestamp()
d = sc.filter(r'>Fallzahlen|Best(ä|&auml;)tigte F(ä|&auml;)lle|Personen in Spitalpflege|Verstorbene Personen', d)
d = d.replace('&nbsp;', ' ')

print('Date and time:', sc.find(r'Fallzahlen ([^<]+)<', d).strip())
print('Confirmed cases:', sc.find('Best(ä|&auml;)tigte F(ä|&auml;)lle:? ([0-9]+)[^0-9]', d, group=3))
print('Deaths:', sc.find(r'Verstorbene Person(en)?: ([0-9]+)[^0-9]', d, group=2))
