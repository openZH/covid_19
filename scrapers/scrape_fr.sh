#!/usr/bin/env python3

import scrape_common as sc
import re

print('FR')
d = sc.download('https://www.fr.ch/covid19/sante/covid-19/coronavirus-statistiques-evolution-de-la-situation-dans-le-canton')
# Or 'https://www.fr.ch/de/covid19/gesundheit/covid-19/coronavirus-statistik-ueber-die-entwicklungen-im-kanton'
sc.timestamp()

# 2020-03-26
"""
<div class="table-responsive">
<p>&nbsp;</p>

<table class="table table-condensed table-hover">
	<tbody>
		<tr>
			<td><strong>Date</strong></td>
			<td><strong>Personnes hospitalisées</strong></td>
			<td><strong>Total Décès</strong></td>
			<td><strong>Total cas avérés</strong></td>
		</tr>
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

m = re.search(r'<table class="table.*?">(.*?)</table>', d, flags=re.MULTILINE | re.DOTALL)
assert m, "Can't find table"

d = m[1]

header = sc.find("<tr>\s*(<t[dh]><strong>Date</strong></t[dh]>\s*<t[dh]><strong>Personnes hospitalisées</strong></t[dh]>\s*<t[dh]><strong>Total Décès</strong></t[dh]>\s*<t[dh]><strong>Total cas avérés</strong></t[dh]>)\s*</tr>", d)
assert header, "Header not matched"

d = d.replace('&nbsp;', '')

# Search for:
"""
		<tr>
			<td>26.03.20</td>
			<td>44</td>
			<td>11</td>
			<td>309</td>
		</tr>
"""

# For some magical reasons, it works without re.MULTILINE | re.DOTALL.
r = re.search(r'<tr>\s*<td.*?>(\d\d\.\d\d\.\d\d)</td>\s*<td.*?>([0-9]+| *)</td>\s*<td.*?>([0-9]+| *)</td>\s*<td.*?>([0-9]+| *)</td>', d, flags=re.I)
assert r, "First row missmatch"

print("Date and time:", r[1])
print("Confirmed cases:", r[4].strip())
print("Deaths:", r[3].strip())
print("Hospitalized:", r[2].strip())
