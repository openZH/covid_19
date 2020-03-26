#!/usr/bin/env python3

import scrape_common as sc

print('SO')
d = sc.download("https://corona.so.ch/")
sc.timestamp()
d = sc.filter("Situation Kanton Solothurn.*Stand|Anzahl positiv getesteter Erkrankungsfälle|Verstorben:", d)

# 2020-03-23
"""
 <p class="bodytext"><strong>Situation Kanton Solothurn (Stand 23.03.2020, 12:00)</strong></p><ul><li>Anzahl positiv getesteter Erkrankungsfälle: 95 Personen</li> 	<li>Verstorben:<strong> </strong>1 Person</li></ul><p class="bodytext"> </p></div></div>
"""

print("Date and time:", sc.find(r'\(Stand ([^\)]+)\)<', d))
print("Confirmed cases:", sc.find(r'Anzahl positiv getesteter Erkrankungsfälle: ([0-9]+) ', d))
print("Deaths:", sc.find('Verstorben:(<strong> <\/strong>)?([0-9]+) ', d, group=2))
