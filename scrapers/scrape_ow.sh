#!/usr/bin/env python3

import scrape_common as sc

print('OW')
d = sc.download('https://www.ow.ch/de/verwaltung/dienstleistungen/?dienst_id=5962', encoding='windows-1252')
sc.timestamp()
d = sc.filter(r'>Stand |ist bei [0-9]+ Personen', d)

#<p class="object-pages-img"><img src="../../images/5e73948a8f49f.jpg"  alt="Kampagne BAG" style="width:600;height:293;border:0;" /></p><br /><div class="object-pages-description"><p class="icmsPContent icms-wysiwyg-first"><em>Stand 23.03.2020</em></p>
#...
#...
# <h3 class="icmsH3Content"><strong>Anzahl Infizierte</strong></h3>
# 
# <p class="icmsPContent">Bisher ist bei 25 Personen im Kanton Obwalden das Coronavirus nachgewiesen worden.</p>

print('Date and time:', sc.find(r'Stand ([^<]+)<', d))
print('Confirmed cases:', sc.find(r'ist bei ([0-9]+) Personen', d))
