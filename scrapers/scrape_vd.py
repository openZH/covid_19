#!/usr/bin/env python3

import scrape_common as sc
import re
import requests

# https://www.vd.ch/toutes-les-actualites/hotline-et-informations-sur-le-coronavirus/point-de-situation-statistique-dans-le-canton-de-vaud/
# includes a content from datawrapper ( https://datawrapper.dwcdn.net/tr5bJ/14/ ),
# which provides actual data and table rendering.
# Here we instead use datawrapper API directly to fetch the data.

print('VD')

url = 'https://api.datawrapper.de/v3/charts/tr5bJ/data'
print('Downloading:', url)
# The bearer authentication token provided by Alex Robert ( https://github.com/AlexBobAlex )
data = requests.get(url,
                    headers={'accept': 'text/csv',
                             'Authorization': 'Bearer 6868e7b3be4d7a69eff00b1a434ea37af3dac1e76f32d9087fc544dbb3f4e229'})
sc.timestamp()
d = data.text

# Date	Hospitalisations en cours	Dont soins intensifs	Sortis de l'hôpital	Décès	Total cas confirmés
# 10.03.2020	36	8	5	1	130
# 11.03.2020	38	7	5	3	200

rows = d.split('\n')

# Remove empty rows
rows = [row for row in rows if len(row.strip())]

headers = rows[0].split('\t')
assert headers[0:6] == ["Date", "Hospitalisations en cours", "Dont soins intensifs", "Sortis de l'hôpital", "Décès", "Total cas confirmés"], f"Table header mismatch: Got: {headers}"

last_row = rows[-1].split('\t')
print('Date and time:', last_row[0])
print('Confirmed cases:', last_row[5])
print('Deaths:', last_row[4])
print('Hospitalized:', last_row[1])
print('ICU:', last_row[2])
if last_row[3].isnumeric():
      print('Recovered:', last_row[3])
