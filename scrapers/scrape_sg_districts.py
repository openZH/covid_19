#!/usr/bin/env python3

import csv
from io import StringIO
import scrape_common as sc

inhabitants = {
    'St.Gallen': 127198,
    'Rorschach': 44110,
    'Rheintal': 74580,
    'Werdenberg': 40239,
    'Sarganserland': 41736,
    'See-Gaster': 76913,
    'Toggenburg': 47272,
    'Wil': 77018,
}

district_ids = {
    'St.Gallen': 1721,
    'Rorschach': 1722,
    'Rheintal': 1723,
    'Werdenberg': 1724,
    'Sarganserland': 1725,
    'See-Gaster': 1726,
    'Toggenburg': 1727,
    'Wil': 1728,
}

url = 'https://www.sg.ch/ueber-den-kanton-st-gallen/statistik/covid-19/_jcr_content/Par/sgch_downloadlist/DownloadListPar/sgch_download.ocFile/KantonSG_C19-Faelle_download.csv'
d = sc.download(url, silent=True)

# strip the "header" / description lines
d = "\n".join(d.split("\n")[5:])

print(sc.DistrictData.header())

reader = csv.DictReader(StringIO(d), delimiter=';')
for row in reader:
    week = sc.find(r'W(\d+)', row['Kalenderwoche'])

    for key, value in inhabitants.items():
        dd = sc.DistrictData(canton='SG', district=key)
        dd.url = url
        dd.week = week
        dd.district_id = district_ids[key]
        dd.new_cases = row['Wahlkreis ' + key]
        dd.total_cases = row['Wahlkreis ' + key + ' (kumuliert)']
        dd.population = value
        print(dd)
