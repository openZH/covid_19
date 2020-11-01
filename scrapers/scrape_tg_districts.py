#!/usr/bin/env python3

import csv
from io import StringIO
import requests
import scrape_common as sc

# perma link to TG COVID dataset on opendata.swiss
r = requests.get(
    'https://opendata.swiss/api/3/action/ogdch_dataset_by_identifier',
    params={'identifier': 'gesundheit_04-2020_stat@kanton-thurgau'}
)
dataset = r.json()['result']
resource = next(r for r in dataset['resources'] if r['name']['de'] == 'COVID19 Fallzahlen Kanton Thurgau auf Ebene Bezirk')

assert resource['download_url'], "Download URL not found"

d_csv = sc.download(resource['download_url'], silent=True, encoding='latin1')

reader = csv.DictReader(StringIO(d_csv), delimiter=';')
for row in reader:
    dd = sc.DistrictData(canton='TG')
    dd.district_id = row['DistrictId']
    dd.district = row['District']
    dd.population = row['Population']
    dd.week = row['Week']
    dd.year = row['Year']
    dd.new_cases = row['NewConfCases']
    dd.url = resource['download_url']
    print(dd)
