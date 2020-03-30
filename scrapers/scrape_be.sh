#!/usr/bin/env python3

import scrape_common as sc

print('BE')
d = sc.download('https://www.besondere-lage.sites.be.ch/besondere-lage_sites/de/index/corona/index.html')
sc.timestamp()

# d = d.filter('table cellspacing="0" summary="Laufend aktualisierte Zahlen') # and 20 next lines.

# 2020-03-30
"""
<div class="tabelle floatingComponent section">
    <h2>Corona Erkrankungen im Kanton Bern</h2>
    <div class="scrolltable">
        <table cellspacing="0" summary="Laufend aktualisierte Zahlen zu den Corona-Erkrankungen im Kanton Bern">
            <colgroup>
                <col width="10%">
                <col width="10%">
                <col width="10%">
                <col width="10%">
                <col width="10%">
                <col width="10%">
                <col width="10%">
            </colgroup>
            <thead>
                <tr>
                    <th id="th_top_5147_1A"><strong>Datum</strong></th>
                    <th id="th_top_5147_2A"><strong>Fälle</strong><br> positiv
                    </th>
                    <th id="th_top_5147_3A">Im<br>
                        <strong>Spital</strong><br> gesamt
                    </th>
                    <th id="th_top_5147_4A">Davon<br> normale
                        <br>
                        <strong>Betten-<br>
 station</strong></th>
                    <th id="th_top_5147_5A">Davon<br>
                        <strong>Intensiv-<br>
 station</strong><br> gesamt
                    </th>
                    <th id="th_top_5147_6A">Davon<br> Intensiv-
                        <br> pflege
                        <br>
                        <strong>beatmet</strong></th>
                    <th id="th_top_5147_7A"><strong>Todes-<br>
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
    </div>
</div>
"""

# This isn't really the best method, but it works for now.
print('Date and time:', sc.find(r'<td headers="th_top_5147_1A">(.+)<', d))
print('Confirmed cases:', sc.find(r'<td headers="th_top_5147_2A">([0-9]+)<', d))
print('Hospitalized:', sc.find(r'<td headers="th_top_5147_3A">([0-9]+)<', d))
print('ICU:', sc.find(r'<td headers="th_top_5147_5A">([0-9]+)<', d))
print('Vent:', sc.find(r'<td headers="th_top_5147_6A">([0-9]+)<', d))
print('Deaths:', sc.find(r'<td headers="th_top_5147_7A">([0-9]+)<', d))
