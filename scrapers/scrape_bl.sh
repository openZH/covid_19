#!/usr/bin/env python3

import scrape_common as sc

print('BL')

d = sc.download('https://www.statistik.bl.ch/files/sites/Grafiken/COVID19/Grafik_COVID19_BL_Linie.htm')
sc.timestamp()

# 2020-03-24
"""
<pre id="data" style="display:none;">
Datum, Bestätigte Fälle, Verstorbene
28-02-2020,1,
29-02-2020,2,
01-03-2020,2,
02-03-2020,2,
...
21-03-2020,282,3
22-03-2020,289,3
23-03-2020,302,3
24-03-2020,306,4
</pre>
"""

d = d.replace('\n', ' ')
# Extract last line. Use non-greedy matching.
d = sc.find(r'<pre id="data".*?> ?Datum, Bestätigte Fälle, Verstorbene.*? ([^ ]+) ?</pre>', d)
assert d, "Can't find a data table"

c = d.split(',')

print('Date and time:', c[0].replace('-', '.'))  # 24-03-2020 -> 24.03.2020
print('Confirmed cases:', c[1])
print('Deaths:', c[2])
