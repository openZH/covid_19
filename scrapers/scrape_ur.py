#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://www.ur.ch/themen/2962'
d = sc.download(url, silent=True)

# 2020-03-26 (and possibly earlier) from https://www.ur.ch/themen/2962
# 2020-07-07 they changed the title, so we're using the table header to find the table
"""
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


soup = BeautifulSoup(d, 'html.parser')
data_table = soup.find(string=re.compile(r'Positiv\s+getestete\s+Erkrankungsfälle')).find_parent('table')

assert data_table, "Can't find data table"

dd = sc.DayData(canton='UR', url=url)
dd.datetime = sc.find(r'Stand[A-Za-z ]*[:,]? ([^<)]+ Uhr)<', d)

headers = data_table.find_all('th')
assert len(headers) == 4, f"Number of header columns changed, {len(headers)} != 4"
assert headers[0].text == "Positiv getestete Erkrankungsfälle"
assert headers[1].text == "Hospitalisiert"
assert headers[2].text == "Verstorben"
assert headers[3].text == "Genesen"

cells = data_table.find_all('td')
assert len(cells) == 4, f"Number of columns changed, {len(cells)} != 4"

dd.cases = cells[0].text
dd.hospitalized = cells[1].text
dd.deaths = cells[2].text
dd.recovered = cells[3].text

print(dd)
