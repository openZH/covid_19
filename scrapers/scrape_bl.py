#!/usr/bin/env python3

from bs4 import BeautifulSoup
import scrape_common as sc

print('BL')

main_site = sc.download("https://www.baselland.ch/politik-und-behorden/direktionen/volkswirtschafts-und-gesundheitsdirektion/amt-fur-gesundheit/medizinische-dienste/kantonsarztlicher-dienst/aktuelles/covid-19-faelle-kanton-basel-landschaft")

# 2020-04-08, two iframes
"""
    <iframe width="100%" class="iframeblock loading" onload="onIframeLoaded(this)" src="https://www.statistik.bl.ch/files/sites/Grafiken/COVID19/20200407_COVID19_BL.htm" scrolling="auto" height="600"></iframe>
    <iframe width="100%" class="iframeblock loading" onload="onIframeLoaded(this)" src="https://www.statistik.bl.ch/files/sites/Grafiken/COVID19/20200407_COVID19_BL_Hosp.htm" scrolling="auto" height="600"></iframe>
"""

soup = BeautifulSoup(main_site, 'html.parser')
for iframe in soup.find_all('iframe'):
    iframe_url = (iframe['src'])

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

    # 2020-04-08, in _Hosp.html
    """
<pre id="data" style="display:none;">
Datum, Normale Station, Intensivstation
28-02-2020,,
29-02-2020,1,
...
05-04-2020,54,19
06-04-2020,50,17
07-04-2020,48,18
</pre>

"""

    # 2020-04-17
    """
<pre id="data" style="display:none;">
Datum, Geheilte kalkuliert, Aktive Fälle, Todesfälle
28-02-2020,,1,
29-02-2020,,2,
01-03-2020,,2,
02-03-2020,,2,
03-03-2020,,2,
04-03-2020,,2,
05-03-2020,,6,
06-03-2020,,6,
...
</pre>
"""

    d = d.replace('\n', ' ')
    # Extract last line. Use non-greedy matching.
    data = sc.find(r'<pre id="data".*?> ?Datum, Bestätigte Fälle, Geheilte (?:geschätzt|kalkuliert), (?:Verstorbene|Todesfälle).*? ([^ ]+) ?</pre>', d)
    if data:
        c = data.split(',')

        print('Date and time:', c[0].replace('-', '.'))  # 24-03-2020 -> 24.03.2020
        print('Confirmed cases:', c[1])
        print('Deaths:', c[3])
        print('Recovered:', c[2])
    else:
        data = sc.find(r'<pre id="data".*?> ?Datum, Normale Station, Intensivstation.*? ([^ ]+) ?</pre>', d)
        if data:
            c = data.split(',')
            print('Date and time:', c[0].replace('-', '.'))  # 24-03-2020 -> 24.03.2020
            print('Hospitalized:', int(c[1]) + int(c[2]))
            print('ICU:', c[2])
        else:
            data = sc.find(r'<pre id="data".*?> ?Datum, Geheilte kalkuliert, Aktive Fälle, Todesfälle.*? ([^ ]+) ?</pre>', d)
            if data:
                c = data.split(',')
                print('Date and time:', c[0].replace('-', '.'))  # 24-03-2020 -> 24.03.2020
                print('Confirmed cases:', int(c[1]) + int(c[2]) + int(c[3]))
                print('Recovered:', c[1])
                print('Deaths:', c[3])
