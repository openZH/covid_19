#!/usr/bin/env python3

import scrape_common as sc

print('SO')
d = sc.download("https://corona.so.ch/")
sc.timestamp()
d = sc.filter("Situation Kanton Solothurn.*Stand|Anzahl positiv getesteter Erkrankungsfälle|Verstorben:", d)
d = d.replace('<strong>', '').replace('</strong>', '')

# 2020-03-23
"""
 <p class="bodytext"><strong>Situation Kanton Solothurn (Stand 23.03.2020, 12:00)</strong></p><ul><li>Anzahl positiv getesteter Erkrankungsfälle: 95 Personen</li> 	<li>Verstorben:<strong> </strong>1 Person</li></ul><p class="bodytext"> </p></div></div>
"""
# 2020-04-02
"""
 <p class="bodytext"><strong>Situation Kanton Solothurn (Stand 02.04.2020, 0:00 Uhr)</strong></p><ul><li>Anzahl positiv getesteter Erkrankungsfälle: 227 (+11 im Vergleich zum Vortag)</li> 	<li>Verstorbene Personen:<strong> </strong>3 (keine Veränderung im Vergleich zum Vortag)</li></ul><p class="bodytext"> </p></div></div>
"""
# 2020-04-03
"""
<p class="bodytext"><strong>Situation Kanton Solothurn (Stand 03.04.2020, 0:00 Uhr)</strong></p><ul><li>Anzahl positiv getesteter Erkrankungsfälle: 237 (+10 im Vergleich zum Vortag)</li> 	<li>Im Kanton hospitalisierte Patientinnen und Patienten: 17 (+3 im Vergleich zum Vortag)</li> 	<li>Verstorbene Personen:<strong> </strong>3 (keine Veränderung im Vergleich zum Vortag)</li></ul><p class="bodytext"> </p></div></div>
"""

print("Date and time:", sc.find(r'\(Stand ([^\)]+)\)<', d))
print("Confirmed cases:", sc.find(r'Anzahl\s*positiv\s*getesteter\s*Erkrankungsfälle\s*:\s*([0-9]+)\b', d))
print("Hospitalized:", sc.find(r'Im\s*Kanton\s*hospitalisierte\s*(?:Patientinnen und Patienten|[^:]*)\s*:\s*([0-9]+)\b', d))
print("Deaths:", sc.find(r'Verstorben(?:e Personen)?\s*:\s*([0-9]+)\b', d))
