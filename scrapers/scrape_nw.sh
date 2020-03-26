#!/usr/bin/env python3

import scrape_common as sc

print('NW')
d = sc.download('https://www.nw.ch/gesundheitsamtdienste/6044')
sc.timestamp()
d = sc.filter(r'Stand:|Bisher (ist bei|sind)', d)

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

print('Date and time:', sc.find(r'em>Stand: *([^<]+)<\/em>', d))
print('Confirmed cases:', sc.find(r'Bisher (ist bei|sind) ([0-9]+)(&nbsp;| )Pers', d, group=2))
