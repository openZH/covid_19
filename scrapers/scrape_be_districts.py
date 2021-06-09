#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from io import StringIO
import scrape_common as sc


# https://www.bfs.admin.ch/bfs/de/home/statistiken/kataloge-datenbanken/karten.assetdetail.5688189.html
district_ids = {
    241: 'Jura bernois',
    242: 'Biel/Bienne',
    243: 'Seeland',
    244: 'Oberaargau',
    245: 'Emmental',
    246: 'Bern-Mittelland',
    247: 'Thun',
    248: 'Obersimmental-Saanen',
    249: 'Frutigen-Niedersimmental',
    250: 'Interlaken-Oberhasli',
}

url = 'https://covid-kennzahlen.apps.be.ch/#/de/cockpit'
csv_url = 'https://raw.githubusercontent.com/openDataBE/covid19Data/develop/7_d_inzidenz_verwaltungskreis.csv'
d = sc.download(csv_url, silent=True)
reader = csv.DictReader(StringIO(d), delimiter=',')
for row in reader:
    #dd = sc.DistrictData(district=district, canton='BE')
    district_id = int(row['bfs_nummer'])
    dd = sc.DistrictData(district=district_ids[district_id], canton='BE')
    dd.url = url
    dd.district_id = district_id
    dd.population = row['einwohnerzahl']
    dd.date  = sc.date_from_text(row['datum'])
    dd.new_cases = round(float(row['7_d_inzidenz']) / 100e3 * int(row['einwohnerzahl']))
    print(dd)
