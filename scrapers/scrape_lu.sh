#!/usr/bin/env python3

import scrape_common as sc

print('LU')
d = sc.download('https://gesundheit.lu.ch/themen/Humanmedizin/Infektionskrankheiten/Coronavirus')
sc.timestamp()

# 2020-03-25
"""
        <p class="teaser__text richtext"><p>Im Kanton Luzern gibt es 228 best&auml;tige F&auml;lle (Stand: 25. M&auml;rz 2020, 11:00 Uhr).&nbsp; Es gibt zwei Todesf&auml;lle im Zusammenhang dem Coronavirus zu beklagen. </p>
"""

d = sc.filter(r'Im Kanton Luzern gibt es', d)

print('Date and time:', sc.find(r'Stand: (.+)(Uhr)?\)', d))
print('Confirmed cases:', sc.find('gibt es ([0-9]+) best(&auml;|ä)tige F(&auml;|ä)lle', d))

deathsString = sc.find('Es gibt (.*) Todesf(&auml;|ä)lle', d)

deaths = sc.int_or_word(deathsString)
if not deaths is None:
  print('Deaths:', deaths)
