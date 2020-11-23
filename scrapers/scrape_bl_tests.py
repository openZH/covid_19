#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import scrape_common as sc
import scrape_bl_common as sbc
from datetime import timedelta


bulletin_url = sbc.get_latest_bl_bulletin_url()
bulletin_content = sc.download(bulletin_url, silent=True)
soup = BeautifulSoup(bulletin_content, 'html.parser')
content = soup.find('strong', string=re.compile(r'Per heute .*')).string
# strip unwanted characters
content = content.encode("ascii", errors="ignore").decode()

date = sc.find(r'Per heute \w+, (\d+\. \w+ 20\d{2})', content)
date = sc.date_from_text(date)
# previous week
date = date - timedelta(days=7)

td = sc.TestData(canton='BL', url=bulletin_url)
td.week = date.isocalendar()[1]
td.year = date.year

td.total_tests = sc.find(r'In der Vorwoche wurden (\d+) PCR-Tests', content)
td.positivity_rate = sc.find(r'von diesen waren (\d+\.?\d?) Prozent positiv', content)

if td:
    print(td)
