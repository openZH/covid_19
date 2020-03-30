#!/usr/bin/env python3

import scrape_common as sc
import re

print('BE')
d = sc.download('https://www.besondere-lage.sites.be.ch/besondere-lage_sites/de/index/corona/index.html')
sc.timestamp()

# 2020-03-30
"""
    <table cellspacing="0" summary="Laufend aktualisierte Zahlen zu den Corona-Erkrankungen im Kanton Bern">
        <colgroup>
                <col width="10%"></col>
                <col width="10%"></col>
                <col width="10%"></col>
                <col width="10%"></col>
                <col width="10%"></col>
                <col width="10%"></col>
                <col width="10%"></col>
                </colgroup>
        <thead>
        <tr>
                <th id="th_top_5147_1A"><strong>Datum</strong></th>
                        <th id="th_top_5147_2A"><strong>Fälle</strong><br />
positiv</th>
                        <th id="th_top_5147_3A">Im<br />
<strong>Spital</strong><br />
gesamt</th>
                        <th id="th_top_5147_4A">Davon<br />
normale<br />
<strong>Betten-<br />
 station</strong></th>
                        <th id="th_top_5147_5A">Davon<br />
<strong>Intensiv-<br />
 station</strong><br />
gesamt</th>
                        <th id="th_top_5147_6A">Davon<br />
Intensiv-<br />
pflege<br />
<strong>beatmet</strong></th>
                        <th id="th_top_5147_7A"><strong>Todes-<br />
 fälle</strong></th>
                        </tr>
        </thead>
        <tbody>
        <tr>
                <td headers="th_top_5147_1A">30.03.2020</td>
                        <td headers="th_top_5147_2A">826</td>
                        <td headers="th_top_5147_3A">112</td>
                        <td headers="th_top_5147_4A">91</td>
                        <td headers="th_top_5147_5A">21</td>
                        <td headers="th_top_5147_6A">17</td>
                        <td headers="th_top_5147_7A">13</td>
                        </tr>
        </tbody>
    </table>
"""

m = re.search(r'<table .*? summary="Laufend aktualisierte Zahlen zu den Corona-Erkrankungen im Kanton Bern">(.*?)<\/table>', d, flags=re.MULTILINE | re.DOTALL)
assert m, "Can't find table"

d = m[1].replace('\n', '')

print(d)

header = sc.find("<thead>\s*<tr>\s*(<th .*><strong>Datum</strong></th>\s*<th .*><strong>Fälle</strong><br />positiv</th>\s*<th .*>Im<br /><strong>Spital</strong><br />gesamt</th>\s*<th .*>Davon<br />normale<br /><strong>Betten-<br /> station</strong></th>\s*<th .*>Davon<br /><strong>Intensiv-<br /> station</strong><br />gesamt</th>\s*<th .*>Davon<br />Intensiv-<br />pflege<br /><strong>beatmet</strong></th>\s*<th .*><strong>Todes-<br /> fälle</strong></th>)\s*</tr>\s*</thead>", d)
assert header, "Header not matched"

# Search for:
"""
<tbody>
    <tr>
        <td headers="th_top_5147_1A">30.03.2020</td>
        <td headers="th_top_5147_2A">826</td>
        <td headers="th_top_5147_3A">112</td>
        <td headers="th_top_5147_4A">91</td>
        <td headers="th_top_5147_5A">21</td>
        <td headers="th_top_5147_6A">17</td>
        <td headers="th_top_5147_7A">13</td>
    </tr>
</tbody>
"""

r = re.search(r'<tbody>\s*<tr>\s*<td.*?>(\d{2}.\d{2}.\d{4})</td>\s*<td.*?>([0-9]+| *)</td>\s*<td.*?>([0-9]+| *)</td>\s*<td.*?>([0-9]+| *)</td>\s*<td.*?>([0-9]+| *)</td>\s*<td.*?>([0-9]+| *)</td>\s*<td.*?>([0-9]+| *)</td>', d, flags=re.I)
assert r, "Row missmatch"

print("Date and time:", r[1])
print("Confirmed cases:", r[2].strip())
print("Deaths:", r[7].strip())
print("Hospitalized:", r[3].strip())
print("ICU:", r[5].strip())
print("Vent:", r[6].strip())
