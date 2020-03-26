#!/usr/bin/env python3

import scrape_common as sc

print('UR')
d = sc.download('https://www.ur.ch/themen/2920')
sc.timestamp()
d = sc.filter(r'Personen gestiegen|Anstieg auf [0-9]+ Person|infiziert sind', d)

# 2020-03-24
"""
.......<h2 class="icmsH2Content">Coronafälle in Uri</h2><p class="icmsPContent"><strong>Der Kantonale Führungsstab hat am heutigen Lagerapport zur Kenntnis genommen, dass im Kanton Uri zurzeit 25 Personen mit dem Coronavirus infiziert sind (Stand: 24. März 2020, 12.00 Uhr). Eine Person ist hospitalisiert. Eine Person ist genesen.</strong>&nbsp;</p>.....
"""

# (Stand: 24. März 2020, 12.00 Uhr).
print('Date and time:', sc.find(r'\(Stand[A-Za-z ]*[:,]? ([^\)]+)\)', d))

a = sc.find(r' ([0-9]+) Personen gestiegen', d)
b = sc.find(r'Anstieg auf ([0-9]+) Person', d)
c = sc.find(r'zurzeit ([0-9]+) Person(en)? mit dem Coronavirus infiziert sind', d)
print('Confirmed cases:', a or b or c)

# Should we try extracting this:
""" Eine Person ist hospitalisiert. Eine Person ist genesen. """
# ?

