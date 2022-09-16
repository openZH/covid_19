#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re
from typing import Optional
from io import StringIO
import datetime
import sys
import scrape_common as sc
from scrape_fr_common import get_fr_csv

def trim_val(val: str) -> Optional[int]:
    if len(val) > 0:
        return int(re.sub(r'(\d+)\s+(\d+)', r'\1\2', val))
    return None

csv_url, csv_data, main_url = get_fr_csv()
reader = csv.DictReader(StringIO(csv_data), delimiter=';')
is_first = True

for row in reader:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='FR', url=main_url)
    for key, val in row.items():
        if sc.find(r'(Date).*', key):
            dd.datetime = val
        if sc.find(r'(Total cas av.r.s).*', key):
            dd.cases = trim_val(val)
        elif sc.find(r'(Personnes hospitalis.es).*', key):
            dd.hospitalized = trim_val(val)
        elif sc.find(r'(aux soins intensifs).*', key):
            dd.icu = trim_val(val)
        elif sc.find(r'(Total d.c.s).*', key):
            dd.deaths = trim_val(val)
        elif sc.find(r'(Total Sorties de l\'h.pital).*', key):
            dd.recovered = trim_val(val)

    assert dd
    assert dd.datetime
    print(dd)
