#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import scrape_common as sc
from collections import OrderedDict, defaultdict
from datetime import datetime

main_url = "https://www.baselland.ch/politik-und-behorden/direktionen/volkswirtschafts-und-gesundheitsdirektion/amt-fur-gesundheit/medizinische-dienste/kantonsarztlicher-dienst/aktuelles/covid-19-faelle-kanton-basel-landschaft"
main_site = sc.download(main_url, silent=True)

# 2020-04-08, two iframes
"""
    <iframe width="100%" class="iframeblock loading" onload="onIframeLoaded(this)" src="https://www.statistik.bl.ch/files/sites/Grafiken/COVID19/20200407_COVID19_BL.htm" scrolling="auto" height="600"></iframe>
    <iframe width="100%" class="iframeblock loading" onload="onIframeLoaded(this)" src="https://www.statistik.bl.ch/files/sites/Grafiken/COVID19/20200407_COVID19_BL_Hosp.htm" scrolling="auto" height="600"></iframe>
"""

def get_row_date(s):
    row_date = s.replace('-', '.')
    parts = row_date.split('.')
    s_date = datetime(day=int(parts[0]), month=int(parts[1]), year=int(parts[2]))
    key = s_date.date().isoformat()
    return (key, row_date)


rows = defaultdict(dict)
soup = BeautifulSoup(main_site, 'html.parser')
for iframe in soup.find_all('iframe'):
    iframe_url = (iframe['src'])

    d = sc.download(iframe_url, silent=True)

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

    # 2020-06-17
    """
    <pre id="data_1" style="display:none; margin-top: 20px;">
    Datum,&quot;Personen in Isolation&quot;,&quot;Personen in Quarantäne&quot;
    11-05-2020,0.0,0.0
    12-05-2020,2.0,1.0
    13-05-2020,2.0,1.0
    14-05-2020,2.0,1.0
    15-05-2020,2.0,1.0
    16-05-2020,3.0,2.0
    17-05-2020,3.0,3.0
    18-05-2020,3.0,3.0
    19-05-2020,3.0,3.0
    ...
    </pre>
    """

    

    d = d.replace('\n', ' ')

    # cases data
    data = sc.find(r'<pre id="data[^"]*".*?> ?Datum, Bestätigte Fälle, Geheilte (?:geschätzt|kalkuliert), (?:Verstorbene|Todesfälle)\s*([^<]+)</pre>', d)
    if data:
        for row in data.split(" "):
            c = row.split(',')
            row_date = c[0].replace('-', '.')
            rows[row_date]['date'] = row_date
            rows[row_date]['cases'] = c[1]
            rows[row_date]['deaths'] = c[3]
            rows[row_date]['recovered'] = c[2]
        continue

    # hospitalization data
    data = sc.find(r'<pre id="data[^"]*".*?> ?Datum, Normale Station, Intensivstation\s*([^<]+)</pre>', d)
    if data:
        for row in data.split(" "):
            c = row.split(',')
            if len(c) == 3:
                key, row_date = get_row_date(c[0])
                rows[key]['date'] = row_date
                if c[1] or c[2]:
                    rows[key]['hospitalized'] = int(c[1] or 0) + int(c[2] or 0)
                rows[key]['icu'] = c[2]
        continue

    # death and recovered data
    data = sc.find(r'<pre id="data[^"]*".*?> ?Datum, Geheilte kalkuliert, Aktive Fälle, Todesfälle\s*([^<]+)</pre>', d) or \
        sc.find(r'<pre id="data_1".*?> ?Datum,&quot;Geheilte \(kalkuliert\)&quot;,&quot;Aktive Fälle \(kalkuliert\)&quot;,&quot;Todesfälle&quot;\s*([^<]+)</pre>', d)
    if data:
        for row in data.split(" "):
            c = row.split(',')
            if len(c) == 4:
                key, row_date = get_row_date(c[0])
                rows[key]['date'] = row_date
                if c[1] or c[2] or c[3]:
                    rows[key]['cases'] = int(c[1] or 0) + int(c[2] or 0) + int(c[3] or 0)
                rows[key]['recovered'] = c[1]
                rows[key]['deaths'] = c[3]
        continue

    # hospitalization data
    data = sc.find(r'<pre id="data_1".*?> ?Datum,&quot;Normale Station&quot;,&quot;Intensivstation \(nicht beatmet\)&quot;,&quot;Intensivstation \(beatmet\)&quot;\s*([^<]+)</pre>', d)
    if data:
        for row in data.split(" "):
            c = row.split(',')
            if len(c) == 4:
                key, row_date = get_row_date(c[0])
                rows[key]['date'] = row_date
                if c[1] or c[2] or c[3]:
                    rows[key]['hospitalized'] = int(float(c[1] or 0) + float(c[2] or 0) + float(c[3] or 0))
                rows[key]['icu'] = (sc.safeint(c[2] or 0) + sc.safeint(c[3] or 0))
                rows[key]['vent'] = c[3]
        continue

    # contact tracing data
    data = sc.find(r'<pre id="data_1".*?> ?Datum,&quot;Personen in Isolation&quot;,&quot;Personen in Quarantäne&quot;\s*([^<]+)</pre>', d)
    if data:
        for row in data.split(" "):
            c = row.split(',')
            if len(c) == 3:
                key, row_date = get_row_date(c[0])
                rows[key]['date'] = row_date
                rows[key]['isolated'] = sc.safeint(c[1] or 0) 
                rows[key]['quarantined'] = sc.safeint(c[2] or 0)
        continue

    # we should never reach here unless there is an unknown iframe
    raise Exception(f"issue parsing data in iframe {iframe_url}")

# order dict by key to ensure the most recent entry is last
ordered_rows = OrderedDict(sorted(rows.items()))
is_first = True
for row_date, row in ordered_rows.items():
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='BL', url=main_url)
    dd.datetime = row['date']
    dd.cases = sc.safeint(row.get('cases'))
    dd.hospitalized = sc.safeint(row.get('hospitalized'))
    dd.icu = sc.safeint(row.get('icu'))
    dd.vent = sc.safeint(row.get('vent'))
    dd.deaths = sc.safeint(row.get('deaths'))
    dd.recovered = sc.safeint(row.get('recovered'))
    dd.quarantined = sc.safeint(row.get('quarantined'))
    dd.isolated = sc.safeint(row.get('isolated'))
    print(dd)
