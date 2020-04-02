#!/usr/bin/env python3

import re
import scrape_common as sc

print('SG')
d = sc.download("https://www.sg.ch/tools/informationen-coronavirus.html")
sc.timestamp()

# 2020-03-20
""" 									<div class="col-xs-12"><p>20.03.2020:<br/>Bestätigte Fälle: 98<br/><br/></p></div>"""

# 2020-03-25
"""									<div class="col-xs-12"><p>25.03.2020:</p><p>Bestätigte Fälle: 228<br/>Todesfälle: 1</p><p>Die Fallzahlen können nicht nach Regionen oder Gemeinden selektioniert werden. Es treten in allen Regionen des Kantons Fälle auf.&nbsp;</p><p>&nbsp;</p></div>"""


print('Date and time:', sc.find(r'<h4>([0-9]+\. (April|Mai|Juni) [0-9]+)<\/h4>', d))
print('Confirmed cases:', sc.find(r'laborbestätigte Fälle \(kumuliert\)<\/th>\s+<th[^>]+>([0-9]+)<\/th>', d.replace("\n", "")))
print('Deaths:', sc.find(r'>Verstorbene \(kumuliert\)<\/td>\s+<td>([0-9]+)<', d.replace("\n", "")))
