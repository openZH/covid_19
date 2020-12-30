#!/usr/bin/env python3

import csv
from io import StringIO
import scrape_common as sc


url = 'https://www.sg.ch/ueber-den-kanton-st-gallen/statistik/covid-19/_jcr_content/Par/sgch_downloadlist_729873930/DownloadListPar/sgch_download.ocFile/KantonSG_C19-Tests_download.csv'
data = sc.download(url, silent=True)

# strip the "header" / description lines
data = "\n".join(data.split("\n")[9:])

reader = csv.DictReader(StringIO(data), delimiter=';')
for row in reader:
    td = sc.TestData(canton='SG', url=url)
    td.start_date = row['Datum']
    td.end_date = row['Datum']
    td.positive_tests = row['Total positive Tests']
    td.negative_tests = row['Total negative Tests']
    td.total_tests = row['Total Tests']
    if row['Positiv in % vom Total']:
        td.positivity_rate = float(row['Positiv in % vom Total']) * 100
        td.positivity_rate = round(10 * td.positivity_rate) / 10
    print(td)
