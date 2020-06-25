#!/usr/bin/env python3

import scrape_common as sc

url = 'https://www.ar.ch/verwaltung/departement-gesundheit-und-soziales/amt-fuer-gesundheit/informationsseite-coronavirus/'
d = sc.download(url, silent=True)
d = d.replace('&nbsp;', ' ')

# Contact Tracing with its own timestamp

dd_ct = sc.DayData(canton='AR', url=url)

t = sc.find(r'Contact\s+tracing\s+\(?.*?Stand\:?\s+([^\)]+)(Uhr)?.*?\)?', d) or \
    sc.find(r'Contact\s+tracing\s+\(?.*?Stand\:?\s+([0-9]+\.[0-9]+\.? \/ [0-9]+h).*?\)?', d)
dd_ct.datetime = t

dd_ct.isolated = sc.find(r'Aktuell\s+COVID-19-Erkrankte\s+in\s+Isolation:\s+<strong>(\d+)</strong>', d)
dd_ct.quarantined = sc.find(r'Aktuell\s+im\s+Kanton\s+wohnhafte\s+Kontaktpersonen\s+in\s+Quarantäne:\s+<strong>(\d+)</strong>', d)

print(dd_ct)
print('-' * 10)

# cases

dd = sc.DayData(canton='AR', url=url)
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
t = sc.find(r'Fälle\s+\(.*?Stand\:?\s+(.+?Uhr).*?\)', d) or \
    sc.find(r'Stand\:? (.+? Uhr).*?\)', d) or \
    sc.find(r'Stand ([0-9]+\.[0-9]+\.? \/ [0-9]+h)', d)
dd.datetime = t

# 2020-03-24 - 2020-03-27
# <li>laborbestätigte Fälle: <strong>44 </strong>Personen</li>
# <li>Todesfälle: <strong>2 </strong>Personen</li>

# 2020-04-23
# <li>laborbestätigte Fälle kumuliert: <strong>88 </strong>Personen</li>
# <li>aktuell hospitalisierte COVID-19-Patienten (inkl. Verdachtsfälle, Station + IPS): <strong>5</strong> Personen</li>
# IPS-COVID-19-Patienten (inkl. Verdachtsfälle, mit und ohne Beatmung):<br /> 		<strong>2</strong> Personen
# <li>Todesfälle kumuliert:&nbsp;<strong>3</strong><strong> </strong>Personen</li>

# 2020-04-24
# <li>laborbestätigte Fälle kumuliert: <strong>88 </strong>Personen</li>
# <li>aktuell hospitalisierte COVID-19-Patienten (inkl. Verdachtsfälle, Station + IPS):&nbsp;<strong>4</strong> Personen</li>
# <li>aktuelle IPS-COVID-19-Fälle (inkl. Verdachtsfälle, mit und ohne Beatmung): <strong>2</strong> Personen</li>
# <li>Todesfälle kumuliert:&nbsp;<strong>3</strong><strong> </strong>Personen</li>

# Use non-greedy matching for some parts.
dd.cases = sc.find(r'bestätigte(?:\sFälle)?.*?(?:\skumuliert)?:( |&nbsp;)*<strong>([0-9]+)[^<]*?<\/strong>', d, group=2)
dd.hospitalized = sc.find(r'hospitalisierte\s+COVID-19-Patienten\s+\(inkl\.\s+Verdachtsfälle,\s+Station\s+[+]\s+IPS\):\s+<strong>(\d+)</strong>', d) or \
    sc.find(r'Aktuell\s+hospitalisierte\s+Patienten\s+\(inkl\.\s+Verdachtsfälle\):\s+<strong>(\d+)</strong>', d)
dd.icu = sc.find(r'IPS-COVID-19-(?:Patienten|Fälle)\s+\(inkl\.\s+Verdachtsfälle,\s+mit\s+und\s+ohne\s+Beatmung\):(?:<br\s*/>)?\s+<strong>(\d+)</strong>\s+Personen', d) or \
    sc.find(r'Davon\s+IPS-Patienten\s+\(mit\s+und\s+ohne\s+Beatmung\):\s+<strong>(\d+)</strong>', d)
dd.deaths = sc.find(r'Todesfälle(?:\skumuliert)?:( |&nbsp;)*<strong>([0-9]+)[^<]*?<\/strong>', d, group=2)

print(dd)
