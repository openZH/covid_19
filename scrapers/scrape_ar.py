#!/usr/bin/env python3

import scrape_common as sc

print('AR')
d = sc.download('https://www.ar.ch/verwaltung/departement-gesundheit-und-soziales/amt-fuer-gesundheit/informationsseite-coronavirus/')
sc.timestamp()
# d = sc.filter('Aktuelle Informationen: Zahlen', d)


# 2020-03-23
"""
 <div id="c61590" class="csc-element  accordeon-element" ><h2 class="header header2 header-default ">Aktuelle Informationen: Zahlen </h2><div class="csc-textpic-text"><p class="bodytext">&nbsp;</p>
 <p class="bodytext">Appenzell Ausserrhoden hat (Stand 23. März 2020, 10.00 Uhr)<strong> </strong></p><ul><li>30 bestätigte Fälle</li> 	<li>7 Personen hospitalisiert, davon 2 Personen noch nicht bestätigt</li> 	<li>1 Person verstorben</li></ul><p class="bodytext"><strong>Hinweis</strong>: Die Fallzahlen zeigen nicht die Anzahl Ansteckungen mit dem Coronavirus, sondern die Anzahl Erkrankungen mit COVID-19. Es dauert bei den meisten Menschen etwa 7 Tage, bis sie nach der Ansteckung mit dem Coronavirus Symptome haben. Nur wenn sich alle Leute an die Regeln halten, kann die&nbsp;Verbreitung gestoppt werden. Die Lage ist ernst. Appenzell Ausserrhoden tut alles, damit die Bevölkerung versorgt werden kann.</p></div></div>
"""

# 2020-03-24
"""
 <p class="bodytext">Appenzell Ausserrhoden hat&nbsp;mit&nbsp; Stand 24.3. / 10h:<strong>
"""

# 2020-03-27
"""
<div id="c61640" class="csc-element  accordeon-element" ><h2 class="header header2 header-default ">Zahlen </h2><div class="csc-textpic-text"><h3>Fälle (Stand: 27.03.2020, 13.00 Uhr)</h3><ul><li>laborbestätigte Fälle: <strong>44 </strong>Personen</li>     <li>Todesfälle: <strong>2 </strong>Personen</li></ul><h3>Teststrasse Teufen (Stand: 27.03.2020, 08.00 Uhr)</h3>
<p class="bodytext"><strong>Hinweis</strong>: Vor dem Spital Herisau und Heiden sind ebenfalls Testcentren aufgebaut. Ausserdem führt eine mobile Einheit Tests durch. Die Teststrasse in Teufen bildet daher nur einen Teil ab.</p><ul><li>insgesamt&nbsp;durchgeführte Tests in Teufen: <strong>80 </strong></li></ul><h3>Hotline (Stand 27.03.2020, 08.00 Uhr)</h3><ul><li>Anfragen Vortag: <strong>51</strong></li>         <li>Anfragen insgesamt: <strong>940</strong></li></ul><h3>Kurzarbeit (Stand: 27.03.2020, 08.00 Uhr)</h3><ul><li>bewilligte Gesuche: <strong>381</strong></li>   <li>Anzahl betroffene Personen: <strong>2'755</strong></li></ul></div></div>
"""

# Use non-greedy matching.
t = sc.find(r'Stand\: (.+? Uhr)\)<', d)
if not t:
    t = sc.find(r'Stand ([0-9]+\.[0-9]+\.? \/ [0-9]+h)', d)
print('Date and time:', t)

# 2020-03-24 - 2020-03-27
# <li>laborbestätigte Fälle: <strong>44 </strong>Personen</li>
# <li>Todesfälle: <strong>2 </strong>Personen</li>

# Use non-greedy matching for some parts.
print('Confirmed cases:', sc.find(r'bestätigte Fälle:( |&nbsp;)*<strong>([0-9]+)[^<]*?<\/strong>', d, group=2))
print('Deaths:', sc.find(r'Todesfälle:( |&nbsp;)*<strong>([0-9]+)[^<]*?<\/strong>', d, group=2))
