#!/usr/bin/env python3

import scrape_common as sc

print('OW')
d = sc.download('https://www.ow.ch/de/verwaltung/dienstleistungen/?dienst_id=5962', encoding='windows-1252')
sc.timestamp()
d = d.replace('&nbsp;', ' ')
d = sc.filter(r'>Stand |ist bei [0-9]+ *Personen', d)

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

print('Date and time:', sc.find(r'Stand ([^<]+)<', d))
print('Confirmed cases:', sc.find(r'ist bei ([0-9]+) *Personen', d))
