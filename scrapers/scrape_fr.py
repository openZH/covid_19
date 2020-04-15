#!/usr/bin/env python3

import re
import scrape_common as sc

print('FR')
d = sc.download('https://www.fr.ch/covid19/sante/covid-19/coronavirus-statistiques-evolution-de-la-situation-dans-le-canton')
# Or 'https://www.fr.ch/de/covid19/gesundheit/covid-19/coronavirus-statistik-ueber-die-entwicklungen-im-kanton'
sc.timestamp()

# 2020-03-26
"""
<div class="table-responsive">
<p>&nbsp;</p>

<table class="table table-condensed table-striped">
	<thead>
		<tr>
			<th><strong>Date</strong></th>
			<th><strong>Personnes hospitalisées</strong></th>
			<th><strong>dont soins intensifs</strong></th>
			<th><strong>Total décès</strong></th>
			<th><strong>Total cas avérés</strong></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>26.03.20</td>
			<td>44</td>
			<td>11</td>
			<td>309</td>
		</tr>
...
		<tr>
			<td>12.03.20</td>
			<td>&nbsp;</td>
			<td>0</td>
			<td>22</td>
		</tr>
		<tr>
			<td>11.03.20</td>
			<td>&nbsp;</td>
			<td>0</td>
			<td>16</td>
		</tr>
	</tbody>
</table>
</div>
"""

# 2020-04-09
"""
	<thead>
		<tr>
			<th><strong>Date</strong></th>
			<th><strong>Personnes hospitalisées</strong></th>
			<th><strong>dont soins intensifs</strong></th>
			<th><strong>Total Sortis de l'hôpital</strong></th>
			<th><strong>Total décès</strong></th>
			<th><strong>Total cas avérés</strong></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>09.04.20</td>
			<td>80</td>
			<td>20</td>
			<td>84</td>
			<td>46</td>
			<td>786</td>
		</tr>
...
"""

m = re.search(r'<table class="table.*?">(.*?)</table>', d, flags=re.MULTILINE | re.DOTALL)
assert m, "Can't find table"

d = m[1]

d = d.replace('<strong>', '').replace('</strong>', '')

header = sc.find("<tr>\s*(<t[dh]>Date</t[dh]>\s*<t[dh]>Personnes hospitalisées</t[dh]>\s*<t[dh]>dont soins intensifs</t[dh]>\s*<t[dh]>Total Sortis de l'hôpital</t[dh]>\s*<t[dh]>Total Décès</t[dh]>\s*<t[dh]>Total cas avérés</t[dh]>)\s*</tr>", d)
assert header, "Header not matched"

d = d.replace('&nbsp;', '')

# Search for:
"""
		<tr>
			<td>26.03.20</td>
			<td>44</td>
			<td>5</td>
			<td>11</td>
			<td>309</td>
		</tr>
"""

# For some magical reasons, it works without re.MULTILINE | r.DOTALL.
r = re.search(r'<tr>\s*<td.*?>(?P<date>\d\d\.\d\d\.\d\d)</td>\s*<td.*?>(?P<hosp>[0-9]+| *)</td>\s*<td.*?>(?P<icu>[0-9]+| *)</td>\s*<td.*?>(?P<released>[0-9]+| *)</td>\s*<td.*?>(?P<deaths>[0-9]+| *)</td>\s*<td.*?>(?P<cases>[0-9]+| *)</td>', d, flags=re.I)
assert r, "First row missmatch"

print("Date and time:", r['date'])
print("Confirmed cases:", r['cases'].strip())
print("Deaths:", r['deaths'].strip())
print("Hospitalized:", r['hosp'].strip())
print("ICU:", r['icu'].strip())
# Released from hospitalisation.
print('Recovered:', r['released'].strip())
