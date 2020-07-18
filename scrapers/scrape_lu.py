#!/usr/bin/env python3

import re
import datetime
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://gesundheit.lu.ch/themen/Humanmedizin/Infektionskrankheiten/Coronavirus'
d = sc.download(url, silent=True)

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

case_date_str = sc.find(r'Fallzahlen\s*im\s*Kanton\s*Luzern.*\(Stand:\s*(.+?)\,', d)
hosp_date_str = sc.find(r'Hospitalisierungen.*\(Stand:\s*(.+?)\,', d)
isolated_date_str = sc.find(r'Isolation.*\(Stand:\s*(.+?)\,', d)

soup = BeautifulSoup(d, 'html.parser')
is_first = True
for table in soup.find(string=re.compile(r'Informationen\s*des\s*Kantons')).find_parent('li').find_all('table'):
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='LU', url=url)
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        assert len(cells) == 2, "Number of columns changed, not 2"

        header_str = "".join([str(x) for x in cells[0].contents])

        value_str = cells[1].find('p') or cells[1]
        value = int(value_str.string)
        if re.search('Bestätigte Fälle|Positiv getestet', header_str):
            dd.datetime = case_date_str
            dd.cases = value
        if re.search('Todesfälle', header_str):
            dd.datetime = case_date_str
            dd.deaths = value
        if re.search('Hospitalisiert', header_str):
            dd.datetime = hosp_date_str
            dd.hospitalized = value
        if re.search('Intensivpflege', header_str):
            dd.datetime = hosp_date_str
            dd.icu = value
        if re.search('Personen in Isolation', header_str):
            dd.datetime = isolated_date_str
            dd.isolated = value
        if re.search('Personen in Quarantäne', header_str):
            dd.datetime = isolated_date_str
            dd.quarantined = value

    print(dd)
