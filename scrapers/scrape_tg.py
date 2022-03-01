#!/usr/bin/env python3

import csv
from io import StringIO
import requests
import scrape_common as sc

# perma link to TG COVID dataset on opendata.swiss
r = requests.get(
    'https://opendata.swiss/api/3/action/ogdch_dataset_by_identifier',
    params={'identifier': 'dfs-ga-1@kanton-thurgau'}
)
dataset = r.json()['result']
resource = next(r for r in dataset['resources'] if r['mimetype'] == 'text/csv')

assert resource['download_url'], "Download URL not found"
    
d_csv = sc.download(resource['download_url'], silent=True)

reader = csv.DictReader(StringIO(d_csv), delimiter=';')
is_first = True
for row in reader:
    if not row['date']:
        continue
    if not is_first:
        print('-' * 10)
    is_first = False
    dd = sc.DayData(canton='TG', url=row['source'])
    dd.datetime = f"{row['date']} {row['time']}"
    dd.cases = row['ncumul_conf']
    dd.deaths = row['ncumul_deceased']
    dd.hospitalized = row['current_hosp']
    dd.new_hosp = row['new_hosp']
    dd.recovered = row['ncumul_released']
    dd.icu = row['current_icu']
    dd.isolated = row['num_isolated']
    print(dd)
