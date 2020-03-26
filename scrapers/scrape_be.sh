#!/usr/bin/env python3

import scrape_common as sc

print('BE')
d = sc.download('https://www.besondere-lage.sites.be.ch/besondere-lage_sites/de/index/corona/index.html')
sc.timestamp()

# d = d.filter('table cellspacing="0" summary="Laufend aktualisierte Zahlen') # and 20 next lines.

# 2020-03-25
"""
		<a name="middlePar_tabelle_5147" style="visibility:hidden"></a><div class="tabelle floatingComponent section"><h2>Corona-Erkrankungen im Kanton Bern</h2><div class="scrolltable">
    <table cellspacing="0" summary="Laufend aktualisierte Zahlen zu den Corona-Erkrankungen im Kanton Bern">
        <colgroup>
                <col width="50%"></col>
                <col width="50%"></col>
                </colgroup>
        <thead>
        <tr>
                <th id="th_top_5147_1A">Fälle</th>
                        <th id="th_top_5147_2A">Todesfälle</th>
                        </tr>
        </thead>
        <tbody>
        <tr>
                <td headers="th_top_5147_1A"><strong>624</strong></td>
                        <td headers="th_top_5147_2A">6</td>
                        </tr>
        </tbody>
    </table>
</div></div>
<a name="middlePar_textbild_4bad" style="visibility:hidden"></a><div class="textBild floatingComponent section"><p>(Stand: 25. März 2020)</p>
"""

print('Date and time:', sc.find(r'Stand: (.+)\)', d))
# This isn't really the best method, but it works for now.
print('Confirmed cases:', sc.find(r'<td .*<strong>([0-9]+)<', d))
print('Deaths:', sc.find(r'<td[^<>]*>([0-9]+)</td>', d))
