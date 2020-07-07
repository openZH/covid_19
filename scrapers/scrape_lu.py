#!/usr/bin/env python3

import re
import datetime
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://gesundheit.lu.ch/themen/Humanmedizin/Infektionskrankheiten/Coronavirus'
d = sc.download(url, silent=True)
dd = sc.DayData(canton='LU', url=url)

# 2020-04-01
"""
<p><strong>Aktuelle Fallzahlen im Kanton Luzern&nbsp;</strong>(Stand: 1. April 2020, 11:00 Uhr)</p>
<table border="0" cellspacing="0" cellpadding="0">
    <tbody>
        <tr>
            <td valign="top" style="width: 151px;">
            <p><strong></strong>Bestätigte Fälle: </p>
            </td>
            <td valign="top" style="width: 47px;">
            <p style="text-align: right;">401</p>
            </td>
        </tr>
        <tr>
            <td valign="top" style="width: 151px;">
            <p>Hospitalisiert:</p>
            </td>
            <td valign="top" style="width: 47px;">
            <p style="text-align: right;">57</p>
            </td>
        </tr>
        <tr>
            <td valign="top" style="width: 151px;">
            <p>Intensivpflege:</p>
            </td>
            <td valign="top" style="width: 47px;">
            <p style="text-align: right;">12</p>
            </td>
        </tr>
        <tr>
            <td valign="top" style="width: 151px;">
            <p>Todesfälle: </p>
            </td>
            <td valign="top" style="width: 47px;">
            <p style="text-align: right;">7</p>
            </td>
        </tr>
    </tbody>
</table>
"""

# 2020-04-03
"""
...
        <tr>
            <td valign="top" style="width: 151px;">
            <p><strong></strong>Positiv getestet (kumuliert): </p>
            </td>
            <td valign="top" style="width: 47px;">
            <p style="text-align: right;">422</p>
            </td>
        </tr>
...
"""

# 2020-05-13
"""
         <tr>
            <td valign="top">
            <p>Intensivpflege (aktuell):</p>
            </td>
            <td style="text-align: right; vertical-align: top;">4</td>
        </tr>
"""

include_hosp = True
include_cases = True
include_isolated = True

case_date_str = sc.find(r'Fallzahlen\s*im\s*Kanton\s*Luzern.*\(Stand:\s*(.+?)\,', d)
hosp_date_str = sc.find(r'Hospitalisierungen.*\(Stand:\s*(.+?)\,', d)
isolated_date_str = sc.find(r'Isolation.*\(Stand:\s*(.+?)\,', d)

case_date = sc.date_from_text(case_date_str)
hosp_date = sc.date_from_text(hosp_date_str)
isolated_date = sc.date_from_text(isolated_date_str)

max_date = max(hosp_date, case_date, isolated_date)
if max_date > hosp_date:
    include_hosp = False
else:
    dd.datetime = hosp_date_str
if max_date > case_date:
    include_cases = False
else:
    dd.datetime = case_date_str
if max_date > isolated_date:
    include_isolated = False
else:
    dd.datetime = isolated_date_str

soup = BeautifulSoup(d, 'html.parser')
rows = []
for table in soup.find(string=re.compile(r'Informationen\s*des\s*Kantons')).find_parent('li').find_all('table'):
    rows += table.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    assert len(cells) == 2, "Number of columns changed, not 2"

    header_str = "".join([str(x) for x in cells[0].contents])

    value_str = cells[1].find('p') or cells[1]
    value = int(value_str.string)
    if re.search('Bestätigte Fälle|Positiv getestet', header_str) and include_cases:
        dd.cases = value
    if re.search('Todesfälle', header_str) and include_cases:
        dd.deaths = value
    if re.search('Hospitalisiert', header_str) and include_hosp:
        dd.hospitalized = value
    if re.search('Intensivpflege', header_str) and include_hosp:
        dd.icu = value
    if re.search('Personen in Isolation', header_str) and include_isolated:
        dd.isolated = value
    if re.search('Personen in Quarantäne', header_str) and include_isolated:
        dd.quarantined = value

print(dd)
