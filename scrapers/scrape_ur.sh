#!/usr/bin/env python3

import scrape_common as sc
import re

print('UR')
d = sc.download('https://www.ur.ch/themen/2962')
sc.timestamp()

# 2020-03-26 (and possibly earlier) from https://www.ur.ch/themen/2962
"""
<h2 class="icmsH2Content">Aktuelle Situation im Kanton Uri</h2>

<p class="icmsPContent">&nbsp;</p>

<table cellpadding="1" cellspacing="1" class="icms-wysiwyg-table" icms="CLEAN" style="width:600px">
	<caption>Stand: 26.03.2020, 12.00 Uhr</caption>
	<thead>
		<tr>
			<th scope="col">Positiv getestete Erkrankungsfälle</th>
			<th scope="col">Hospitalisiert</th>
			<th scope="col">Verstorben</th>
			<th scope="col">Genesen</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td icms="" style="text-align:center">38</td>
			<td icms="" style="text-align:center">4</td>
			<td icms="" style="text-align:center">0</td>
			<td icms="" style="text-align:center">2</td>
		</tr>
	</tbody>
</table>
"""


m = re.search(r'>Aktuelle Situation im Kanton Uri</h2>.*?<table[^>]*>(.+?)</table>', d, flags=re.MULTILINE | re.DOTALL)
assert m, "Can't find data table"
d = m[1]

print('Date and time:', sc.find(r'Stand[A-Za-z ]*[:,]? ([^<)]+ Uhr)<', d))

rows = re.findall('<tr>(.*?)</tr>', d, flags=re.DOTALL)

headers = re.findall('<th[^>]*>(.*?)</th>', rows[0])
assert headers[0] == "Positiv getestete Erkrankungsfälle"
assert headers[1] == "Hospitalisiert"
assert headers[2] == "Verstorben"
assert headers[3] == "Genesen"

first_row = rows[1].strip()

columns = re.findall('<td[^>]*>(.*?)</td>', first_row)

print('Confirmed cases:', columns[0])
print('Hospitalized:', columns[1])
print('Deaths:', columns[2])
print('Recovered:', columns[3])
