#!/usr/bin/env python3

import scrape_common as sc

print('NW')
d = sc.download('https://www.nw.ch/gesundheitsamtdienste/6044')
sc.timestamp()
d = d.replace('&nbsp;', ' ')
d = d.replace('<strong>', ' ').replace('</strong>', ' ')
# d = sc.filter(r'Stand:|Bisher (ist bei|sind)|Positiv getestete Personen:|Am Virus verstorbene Personen:', d)

# <p class="icmsPContent icms-wysiwyg-first"><em>Stand: 21.&nbsp;März 2020, 18.15&nbsp; Uhr</em></p>
# <p class="icmsPContent">Bisher ist bei 33&nbsp;Personen&nbsp;im Kanton Nidwalden das Coronavirus nachgewiesen worden.&nbsp;<a id="Veranstaltungen" name="Veranstaltungen"></a></p>

# <p class="icmsPContent icms-wysiwyg-first"><em>Stand: 24.&nbsp;März 2020, 15.15&nbsp;Uhr</em></p>
# <p class="icmsPContent">Bisher sind 42&nbsp;Personen&nbsp;im Kanton Nidwalden positiv auf das Coronavirus getestet worden.&nbsp;<a id="Veranstaltungen" name="Veranstaltungen"></a></p>

# 2020-03-25
"""
<p class="icmsPContent icms-wysiwyg-first"><em>Stand: 25.&nbsp;März 2020, 15.30 Uhr</em></p>
...
<p class="icmsPContent">Bisher sind 44&nbsp;Personen&nbsp;im Kanton Nidwalden positiv auf das Coronavirus getestet worden.&nbsp;<a id="Veranstaltungen" name="Veranstaltungen"></a></p>
"""

# 2020-03-26
"""
            <div class="icms-text-container"><div class="icms-wysiwyg"><h2 class="icmsH2Content"><strong>Aktuelle Situation Kanton Nidwalden</strong></h2>

<p class="icmsPContent icms-wysiwyg-first"><em>Stand: 25.&nbsp;März 2020, 15.30 Uhr</em></p>

 <h3 class="icmsH3Content"><br />
 <strong>Anzahl&nbsp;Erkrankungen/Tote</strong></h3>

 <p class="icmsPContent">Positiv getestete Personen: 44<br />
 Am Virus verstorbene Personen: 0&nbsp;<a id="Veranstaltungen" name="Veranstaltungen"></a></p>
"""

# 2020-03-31
"""
<strong>Anzahl Fälle</strong></h3>

<p class="icmsPContent">Positiv getestete Personen: <strong>70&nbsp;</strong>(+7)<br />
Verstorbene Personen:&nbsp;<strong>0</strong></p>
"""

print('Date and time:', sc.find(r'em>Stand: *([^<]+)<\/em>', d))

a = sc.find(r'Bisher (ist bei|sind) ([0-9]+)(&nbsp;| )Pers', d, group=2)
b = sc.find(r'Positiv\s*getestete\s*Personen:\s*([0-9]+)\b', d)
print('Confirmed cases:', a or b)

print('Deaths:', sc.find(r'(?:Am\s*Virus\s*)?verstorbene\s*Persone?n?:\s*([0-9]+)\b', d))
