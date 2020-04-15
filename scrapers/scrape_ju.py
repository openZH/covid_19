#!/usr/bin/env python3

import re
import scrape_common as sc

print('JU')
d = sc.download('https://www.jura.ch/fr/Autorites/Coronavirus/Accueil/Coronavirus-Informations-officielles-a-la-population-jurassienne.html')
sc.timestamp()
# d = sc.filter(r'Situation .*2020', d) # + 2 lines before.

# 2020-03-27 (and few days before similar)
"""
<h3 class="default-subtitle">Cas d'infection au coronavirus COVID-19 dans le canton du Jura</h3>

 

<table border="0" cellspacing="0" style="width:100%">
        <thead>
                <tr>
                        <th scope="col">
                        <p class="wysiwyg-h6">Cas confirmés</p>
                        </th>
                        <th scope="col">
                        <p class="wysiwyg-h6">&nbsp;</p>
                        </th>
                </tr>
        </thead>
        <tbody>
                <tr>
                        <td>
                        <p class="wysiwyg-h6"><strong>112</strong></p>
                        </td>
                        <td><em>Situation 27 mars 2020 (16h)</em></td>
                </tr>
                <tr>
                        <td>&nbsp;</td>
                        <td><a href="/fr/Autorites/Coronavirus/Chiffres-H-JU/Evolution-des-cas-COVID-19-dans-le-Jura.html" target="_blank">Voir le détail</a></td>
                </tr>
        </tbody>
</table>
"""

# 2020-04-01
"""
                <tr>
                        <td>
                        <p class="wysiwyg-h6"><strong>144</strong></p>
                        </td>
                        <td><em>Situation 1er avril 2020 (16h)</em></td>
                </tr>
"""

print('Date and time:', sc.find(r'Situation (.+?)<\/em', d))
print('Confirmed cases:', sc.find(r'<p.*?<strong>([0-9]+)<', d))

d = sc.download('https://www.jura.ch/fr/Autorites/Coronavirus/Chiffres-H-JU/Evolution-des-cas-COVID-19-dans-le-Jura.html')
sc.timestamp()

# 2020-03-27 (and few days before similar)
"""
<table border="0" cellspacing="0" style="width:70%">
	<caption>Evolution du nombre de cas positifs COVID-19 dans le Jura</caption>
	<thead>
		<tr>
			<th scope="row">Date</th>
			<th scope="col">
			<p>Cas confirmés<br />
			(total)</p>
			</th>
			<td scope="col">
			<p><strong>Hospitalisés</strong></p>

			<p>&nbsp;</p>
			</td>
			<th scope="col">Soins<br />
			intensifs</th>
			<th scope="col">Décès</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th scope="row">3 mars 2020</th>
			<td>1</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
...
		<tr>
			<th scope="row">5 mars 2020</th>
			<td>2</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
...
		<tr>
			<td><strong>26 mars 2020</strong></td>
			<td>99</td>
			<td>16</td>
			<td>4</td>
		</tr>
		<tr>
			<td><strong>27 mars 2020</strong></td>
			<td>112</td>
			<td>16</td>
			<td>4</td>
		</tr>
		<tr>
			<th scope="row">&nbsp;</th>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
	</tbody>
</table>
"""

# 2020-04-01
"""
		<tr>
			<th scope="row">1<sup>er </sup>avril 2020</th>
			<td>144</td>
			<td>29</td>
			<td>5</td>
			<td>&nbsp;</td>
		</tr>

"""

m = re.search(r'<table[^>]*>\s*<caption>Evolution [^<]*</caption>\s*<thead>(.*)</thead>\s*<tbody>(.*)</tbody>\s*</table>', d, flags=re.I | re.MULTILINE | re.DOTALL)
if m:
    # m[1]  # Header.
    # TODO(baryluk): Verify partially header so order of columns is as expected.

    data = m[2]  # Rows.
    # Do some substitutions to make it easier.
    data = data.replace('&nbsp;', '')
    data = data.replace('<strong>', '').replace('</strong>', '')
    data = re.sub(r'<sup>.*?</sup>', ' ', data)

    # Split table into rows.
    rows = re.findall('<tr>(.*?)</tr>', data, flags=re.I | re.MULTILINE | re.DOTALL)
    # Do some minor cleanups
    rows = [row.strip() for row in rows]
    rows = [row.replace('\t', '').replace('\n', '') for row in rows]
    # Split each row content into columns.
    parsed_rows = []
    for row in rows:
        columns = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, flags=re.I)
        # Skip empty rows (no date, or no confirmed cases value).
        if len(columns[0]) == 0 or len(columns[1]) == 0:
            continue
        parsed_rows.append(columns)

    # Get last non-empty row.
    last_row = parsed_rows[-1]

    # The HTML has some columns completly missing, so fill them up.
    while len(last_row) < 5:
        last_row.append('')

    # Some rows do have more than 5 columns actually (6 columns), but these extra
    # columns are empty and don't have any meaning. So only use first 5 columns.
    date, cases, hospitalized, icu, death = last_row[0:5]

    # The date in table, is just a day without a time.
    # But make at least it is the same day as the other source.
    # In parser, we will use one which is more accurate.
    print('Date and time:', date)
    print('Confirmed cases:', cases)
    # These if checks, will still triger if the number is '0', because matched
    # values are strings. It will not triger if it is empty '' (or '&nbsp;').
    # Which is what we want.
    # It is probable, that mising values in the table, actually represent 0,
    # but it is unclear.
    if hospitalized:
        print('Hospitalized:', hospitalized)
    if icu:
        print('ICU:', icu)
    if death:
        print('Deaths:', death)
