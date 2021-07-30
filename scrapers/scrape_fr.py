#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from io import StringIO
import datetime
import sys
import scrape_common as sc
from scrape_fr_common import get_fr_csv


csv_url, csv_data, main_url = get_fr_csv()
reader = csv.DictReader(StringIO(csv_data), delimiter=';')
is_first = True

for row in reader:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='FR', url=main_url)
    dd.datetime = row['Date / Datum']
    for key, val in row.items():
        if sc.find(r'(Total cas av.r.s).*', key):
            dd.cases = val
        elif sc.find(r'(Personnes hospitalis.es).*', key):
            dd.hospitalized = val
        elif sc.find(r'(aux soins intensifs).*', key):
            dd.icu = val
        elif sc.find(r'(Total d.c.s).*', key):
            dd.deaths = val
        elif sc.find(r'(Total Sorties de l\'h.pital).*', key):
            dd.recovered = val

    assert dd
    print(dd)
