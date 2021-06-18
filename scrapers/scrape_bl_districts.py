#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import scrape_common as sc
import scrape_bl_common as sbc
from collections import defaultdict, OrderedDict
from datetime import datetime

main_url = "https://www.baselland.ch/politik-und-behorden/direktionen/volkswirtschafts-und-gesundheitsdirektion/amt-fur-gesundheit/medizinische-dienste/kantonsarztlicher-dienst/aktuelles/covid-19-faelle-kanton-basel-landschaft"
main_site = sc.download(main_url, silent=True)

# 2020-04-08, two iframes
"""
    <iframe width="100%" class="iframeblock loading" onload="onIframeLoaded(this)" src="https://www.statistik.bl.ch/files/sites/Grafiken/COVID19/20200407_COVID19_BL.htm" scrolling="auto" height="600"></iframe>
    <iframe width="100%" class="iframeblock loading" onload="onIframeLoaded(this)" src="https://www.statistik.bl.ch/files/sites/Grafiken/COVID19/20200407_COVID19_BL_Hosp.htm" scrolling="auto" height="600"></iframe>
"""


def parse_row_date(s):
    return sbc.parse_bl_date(s)[0]


rows = defaultdict(dict)
soup = BeautifulSoup(main_site, 'html.parser')
for iframe in soup.find_all('iframe'):
    iframe_url = (iframe['src'])

    if iframe_url.find('/dbw/360') <= 0:
        continue

    d = sc.download(iframe_url, silent=True)

    # 2020-07-29
    """
    <pre id="data_1" style="display:none; margin-top: 20px;">
    Datum,&quot;Personen in Isolation&quot;,&quot;Personen in Quarantäne (Tracing)&quot;,&quot;Personen in Quarantäne (Rückreise Risikoländer)&quot;
    11-05-2020,0.0,0.0,
    """

    d = d.replace('\n', ' ')

    # district data!
    data = sc.find(r'<pre id="data_1".*?> ?Datum,&quot;Bezirk Arlesheim&quot;,&quot;Bezirk Laufen&quot;,&quot;Bezirk Liestal&quot;,&quot;Bezirk Sissach&quot;,&quot;Bezirk Waldenburg&quot;\s*([^<]+)</pre>', d)
    if data:
        # take "Fallzahlen Bezirke BL ab Juni 2020", but not the 14d averaged one
        for row in data.split(" "):
            c = row.split(',')
            assert len(c) == 6, f"Number of fields changed, {len(c)} != 6"
            row_date = parse_row_date(c[0])
            rows[row_date]['date'] = row_date
            rows[row_date]['Arlesheim'] = sc.safeint(c[1])
            rows[row_date]['Laufen'] = sc.safeint(c[2])
            rows[row_date]['Liestal'] = sc.safeint(c[3])
            rows[row_date]['Sissach'] = sc.safeint(c[4])
            rows[row_date]['Waldenburg'] = sc.safeint(c[5])
        break

assert rows, "Couldn't find district data in iframes"

# https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/karten.assetdetail.5688189.html
district_ids = {
    'Arlesheim': 1301,
    'Laufen': 1302,
    'Liestal': 1303,
    'Sissach': 1304,
    'Waldenburg': 1305,
}

# https://www.statistik.bl.ch/web_portal/1
population = {
    'Arlesheim': 157253,
    'Laufen': 20141,
    'Liestal': 61201,
    'Sissach': 36051,
    'Waldenburg': 16119,
}

# based on https://github.com/openZH/covid_19/issues/1185#issuecomment-709952315
initial_cases = {
    'Arlesheim': 0,
    'Laufen': 0,
    'Liestal': 0,
    'Sissach': 0,
    'Waldenburg': 0,
}

# order dict by key to ensure the most recent entry is last
ordered_rows = OrderedDict(sorted(rows.items()))

#for row_date, row in ordered_rows.items():
#    for district, district_id in district_ids.items():

for district, district_id in district_ids.items():
    last_total_cases_val = initial_cases[district]
    if district == 'Arlesheim':
        # 2020-05-31 is 527
        last_total_cases_val = 0

    for row_date, row in ordered_rows.items():
        dd = sc.DistrictData(canton='BL', district=district)
        dd.district_id = district_id
        dd.population = population[district]
        dd.url = main_url
        dd.date = row['date']
        dd.total_cases = row[district] + initial_cases[district]
        dd.new_cases = dd.total_cases - last_total_cases_val
        last_total_cases_val = dd.total_cases
        print(dd)
