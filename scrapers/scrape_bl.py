#!/usr/bin/env python3

import scrape_common as sc

print('BL')

main_site = sc.download("https://www.baselland.ch/politik-und-behorden/direktionen/volkswirtschafts-und-gesundheitsdirektion/amt-fur-gesundheit/medizinische-dienste/kantonsarztlicher-dienst/aktuelles/covid-19-faelle-kanton-basel-landschaft")

# 2020-03-31, iframe
"""
<iframe width="100%" class="iframeblock loading" onload="onIframeLoaded(this)" src="https://www.statistik.bl.ch/files/sites/Grafiken/COVID19/20200331_COVID19_BL.htm" scrolling="auto" height="600"></iframe>
"""

iframe = sc.filter(r'<iframe', main_site)
iframe_url = sc.find(r'src="(.+?)"', iframe)

d = sc.download(iframe_url)
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

# 2020-04-01
"""
<pre id="data" style="display:none;">
Datum, Bestätigte Fälle, Geheilte geschätzt, Verstorbene
28-02-2020,1,,
29-02-2020,2,,
...
31-03-2020,561,242,10
01-04-2020,588,249,11
</pre>
"""

# 2020-04-02
"""
<pre id="data" style="display:none;">
Datum, Bestätigte Fälle, Geheilte kalkuliert, Verstorbene
28-02-2020,1,,
...
02-04-2020,610,262,12
</pre>
"""

d = d.replace('\n', ' ')
# Extract last line. Use non-greedy matching.
d = sc.find(r'<pre id="data".*?> ?Datum, Bestätigte Fälle, Geheilte (?:geschätzt|kalkuliert), (?:Verstorbene|Todesfälle).*? ([^ ]+) ?</pre>', d)
assert d, "Can't find a data table"

c = d.split(',')

print('Date and time:', c[0].replace('-', '.'))  # 24-03-2020 -> 24.03.2020
print('Confirmed cases:', c[1])
print('Deaths:', c[3])
print('Recovered:', c[2])
