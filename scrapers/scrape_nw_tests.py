#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import scrape_common as sc
import scrape_nw_common as snc

url, soup = snc.get_nw_page()

td = sc.TestData(canton='NW', url=url)

item = soup.find(text=re.compile('Anzahl F.lle')).find_parent('p')
assert item, f"Could not find title item in {url}"

date = sc.find(r'Stand: (\d+\. .* 20\d{2})', item.text)
date = sc.date_from_text(date)
td.start_date = date.isoformat()
td.end_date = date.isoformat()

rows = item.find_next('table').findChildren('tr')
for row in rows:
    cols = row.findChildren('td')
    item = cols[0].text
    if re.match(r'Covid-19-Tests innert 24h.*', item, re.I):
        res = re.match(r'(\d+)\s+(\d+\.?\d?)%', cols[1].text)
        assert res
        td.total_tests = res[1]
        td.positivity_rate = res[2]

assert td
print(td)
