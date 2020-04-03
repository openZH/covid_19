#!/usr/bin/env python3

import scrape_common as sc
from bs4 import BeautifulSoup
import datetime
import re

print('LU')
d = sc.download('https://gesundheit.lu.ch/themen/Humanmedizin/Infektionskrankheiten/Coronavirus')
sc.timestamp()

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

print('Date and time:', sc.find(r'Aktuelle\s*Fallzahlen\s*im\s*Kanton\s*Luzern.*\(Stand:\s*(.+?)\)', d))

soup = BeautifulSoup(d, 'html.parser')
table = soup.find(string=re.compile(r'Informationen\s*des\s*Kantons')).find_parent('li').find('table')

assert table, "Table not found"

rows = table.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    assert len(cells) == 2, "Number of columns changed, not 2"

    header_str = "".join([str(x) for x in cells[0].contents]) 
    value = int(cells[1].find('p').string)
    if re.search('Bestätigte Fälle|Positiv getestet', header_str):
        print('Confirmed cases:', value)
    if re.search('Hospitalisiert', header_str):
        print('Hospitalized:', value)
    if re.search('Todesfälle', header_str):
        print('Deaths:', value)
    if re.search('Intensivpflege', header_str):
        print('ICU:', value)
