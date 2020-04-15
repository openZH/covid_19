#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc

print('OW')
d = sc.download('https://www.ow.ch/de/verwaltung/dienstleistungen/?dienst_id=5962', encoding='windows-1252')
sc.timestamp()
d = d.replace('&nbsp;', ' ')

# 2020-03-23
"""
<p class="object-pages-img"><img src="../../images/5e73948a8f49f.jpg"  alt="Kampagne BAG" style="width:600;height:293;border:0;" /></p><br /><div class="object-pages-description"><p class="icmsPContent icms-wysiwyg-first"><em>Stand 23.03.2020</em></p>
...
...
<h3 class="icmsH3Content"><strong>Anzahl Infizierte</strong></h3>

<p class="icmsPContent">Bisher ist bei 25 Personen im Kanton Obwalden das Coronavirus nachgewiesen worden.</p>
"""

# 2020-03-27
"""
<p class="object-pages-img"><img src="../../images/5e73948a8f49f.jpg"  alt="Kampagne BAG" style="width:600;height:293;border:0;" /></p><br /><div class="object-pages-description"><p class="icmsPContent icms-wysiwyg-first"><em>Stand 27.03.2020</em></p>
...
...
<h3 class="icmsH3Content"><strong><a id="Fallzahl" name="Fallzahl"></a>Fallzahl Kanton Obwalden</strong></h3>

<p class="icmsPContent">Bisher ist bei 37&nbsp;Personen im Kanton Obwalden das Coronavirus nachgewiesen worden. Bereits genesene Personen sind in dieser Zahl ebenfalls enthalten&nbsp;(Stand: 27. M<E4>rz 2020).</p>
"""

# 2020-04-06
"""
<h3 class="icmsH3Content"><strong><a id="Fallzahl" name="Fallzahl"></a>Fallzahl Kanton Obwalden (Stand 6. April 2020, 15.00 Uhr)</strong></h3>

<ul>
	<li>Positiv getestete Personen: 60</li>
	<li>In Obwalden hospitalisierte Personen: 1</li>
	<li>Verstorbene Personen: 0</li>
</ul>
"""


print('Date and time:',
      sc.find(r'Stand ([^<]+ Uhr)', d) or sc.find(r'Stand ([^<]+)<', d))

soup = BeautifulSoup(d, 'html.parser')
i = 0
for row in soup.find(id='Fallzahl').find_next('table').find_all('tr'):
    i += 1
    cells = row.find_all('td')
    assert len(cells) >= 2, "Number of columns changed, not 2+"
    if i == 1: # Header.
        assert 'COVID-19' in str(cells[0].find('strong').string)
        assert 'Anzahl' in str(cells[1].find('strong').string)
        # assert 'Veränderung' in str(cells[2].find('strong').string)
        continue

    header_str = cells[0].find('span').string
    value = int(cells[1].find('span').string.split()[0])
    if re.search(r'Bestätigte Fälle|Positiv getestet', header_str):
        print('Confirmed cases:', value)
    if re.search(r'In OW hospitalisiert \(aktuell\):?', header_str):
        print('Hospitalized:', value)
    if re.search(r'Todesfälle', header_str):
        print('Deaths:', value)
