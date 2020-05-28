#!/usr/bin/env python3

import scrape_common as sc
import re


# get latest from list with all bulletins
d = sc.download(
    'https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp', silent=True)

url = sc.find(r'<a [^>]*href="([^"]+\.pdf)">.+Bulletin.+</a>', d)

# download latest PDF
pdf_url = 'https://www.ag.ch' + url
d = sc.pdfdownload(pdf_url, raw=True, silent=True)
# extract case numbers reported for previous days
data_rows = [row for row in d.split("\n")
             if re.search(r'^(Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag),\s+\d{2}\.\d{2}\.\d{4}\s+[\'’0-9]+$', row)]
for row in data_rows[0:-1]:
    dd = sc.DayData(canton='AG', url=pdf_url)
    m = re.search(
        r'^(?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag)?,?\s*(.+)\s+([0-9]+)$', re.sub(r'[\'’]', '', row))
    dd.datetime = m[1]
    dd.cases = m[2]
    print(dd)
    print('-' * 10)

# and now the latest data for the current day
d = d.replace("-\n", '')
d = d.replace("’", "")
d = d.replace("'", "")
dd = sc.DayData(canton='AG', url=pdf_url)
dd.datetime = sc.find(r'Aarau, (.+? Uhr)', d)
dd.cases = sc.find(r'zurzeit\s+([0-9]+)\s+bestätigte\s+Fälle', d)
dd.recovered = sc.find(r'([0-9]+)\s+Personen\s+als\s+ge(\-\s+)?heilt', d)
dd.hospitalized = sc.find( r'([0-9]+)\s+Person(en)?\s+sind\s+zurzeit\s+hospitalisiert', d)
dd.icu = sc.find(r'([0-9]+)\s+Person(en)?\s+auf\s+(der\s+)?Intensivstation(en)?', d)
dd.vent = sc.find(r'([0-9]+|alle)\s+Person(en)?\s+auf\s+(der\s+)Intensivstation(en)?.*(\s+künstlich\s+beatmet)', d) \
    or sc.find(r'([0-9]+|alle)\s+Personen\s+auf\s+der\s+Intensivstation\s+müssen\s+künstlich\s+beatmet\s+werden', d)
if dd.vent == 'alle':
    dd.vent = dd.icu
dd.deaths = sc.find(
    r'([0-9]+)\s+Person(en)?\s+an\s+den\s+Folgen\s+des\s+Coronavirus\s+verstorben', d)
dd.isolated = sc.find(r'betreut\s+sind\s+([0-9]+)\s+infizierte\s+Personen(en)?', d)
dd.quarantined = sc.find(r'([0-9]+)\s+enge\s+Kontaktperson(en)?', d)
print(dd)
