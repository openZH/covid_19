#!/usr/bin/env python3

import scrape_common as sc
import re

print('AG')

# get latest from list with all bulletins
d = sc.download('https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp')

url = sc.find(r'<a [^>]*href="([^"]+\.pdf)">.+Bulletin.+</a>', d)

# download latest PDF
d = sc.pdfdownload('https://www.ag.ch' + url, raw=True)

sc.timestamp()

print('Date and time:', sc.find(r'Aarau, (.+? Uhr)', d))

print('Confirmed cases:', sc.find(r'zurzeit\s+([0-9]+)\s+bestätigte\s+Fälle', d))

print('Recovered:', sc.find(r'([0-9]+)\s+Personen.*?als\s+geheilt', d))

print('Hospitalized:', sc.find(r'([0-9]+)\s+Person(en)?\s+sind\s+zurzeit\s+hospitalisiert', d))

print('ICU:', sc.find(r'([0-9]+)\s+Person(en)?.*?auf\s+Intensivstationen', d))

print('Vent:', sc.find(r'([0-9]+)\s+Person(en)?\s+künstlich\s+beatmet', d))

print('Deaths:', sc.find(r'([0-9]+)\s+Person(en)?\s+an\s+den\s+Folgen\s+des\s+Coronavirus\s+verstorben', d))
