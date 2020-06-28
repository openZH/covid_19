#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import scrape_common as sc

html_url = 'https://www.besondere-lage.sites.be.ch/besondere-lage_sites/de/index/corona/index.html'
d = sc.download(html_url, silent=True)

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

# 2020-04-17
"""
    <table cellspacing="0" summary="Laufend aktualisierte Zahlen zu den Corona-Erkrankungen im Kanton Bern">
        <colgroup>
                <col width="5%"></col>
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
                <td headers="th_top_5147_1A"><strong>17.04.20</strong><br />
08.00 h</td>
                        <td headers="th_top_5147_2A">1'553</td>
                        <td headers="th_top_5147_3A">69</td>
                        <td headers="th_top_5147_4A">44</td>
                        <td headers="th_top_5147_5A">25</td>
                        <td headers="th_top_5147_6A">13</td>
                        <td headers="th_top_5147_7A">67</td>
                        </tr>
        <tr class="colored">
                <td headers="th_top_5147_1A"><strong>16.04.20</strong><br />
08.00 h</td>
                        <td headers="th_top_5147_2A">1'515</td>
                        <td headers="th_top_5147_3A">70</td>
                        <td headers="th_top_5147_4A">44</td>
                        <td headers="th_top_5147_5A">26</td>
                        <td headers="th_top_5147_6A">12</td>
                        <td headers="th_top_5147_7A">55</td>
                        </tr>
        </tbody>
    </table>
"""

soup = BeautifulSoup(d, 'html.parser')
rows = []
for t in soup.find_all('table'):
    if t.attrs['summary'] == 'Laufend aktualisierte Zahlen zu den Corona-Erkrankungen im Kanton Bern':
        headers = [" ".join(cell.stripped_strings) for cell in t.find('tr').find_all('th')]

        is_first = True
        for row in [r for r in t.find_all('tr') if r.find_all('td')]:
            if "Nachmeldung" in row.text:
                continue
            if re.search(r'Daten.*bereini.*gung', row.text.replace("\n", " ")):
                continue
            if not is_first:
                print('-' * 10)
            is_first = False

            print('BE')
            sc.timestamp()
            print('Downloading:', html_url)

            col_num = 0
            for cell in row.find_all(['td']):
                value = cell.string
                if value:
                    value = value.replace("'", "")
                    value = value.replace("*", "")

                if headers[col_num] == 'Datum':
                    print('Date and time:', " ".join(cell.stripped_strings))
                elif headers[col_num] == 'Fälle positiv':
                    print('Confirmed cases:', value)
                elif 'Todes' in headers[col_num]:
                    print('Deaths:', value)
                elif headers[col_num] == 'Im Spital gesamt':
                    print('Hospitalized:', value)
                elif 'beatmet' in headers[col_num]:
                    print('Vent:', value)
                elif 'Intensiv' in headers[col_num] and 'gesamt' in headers[col_num]:
                    print('ICU:', value)
                col_num += 1
