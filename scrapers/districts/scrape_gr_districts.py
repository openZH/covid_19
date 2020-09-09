#!/usr/bin/env python

import datetime
import requests

import scrape_common as sc

inhabitants = {
    'Albula': 8054,
    'Bernina': 4613,
    'Engiadina Bassa/Val Müstair': 9197,
    'Imboden': 21293,
    'Landquart': 25402,
    'Maloja': 18184,
    'Moesa': 8671,
    'Plessur': 42446,
    'Prättigau/Davos': 26089,
    'Surselva': 21289,
    'Viamala': 13783,
}

district_ids = {
    'Albula': 1841,
    'Bernina': 1842,
    'Engiadina Bassa/Val Müstair': 1843,
    'Imboden': 1844,
    'Landquart': 1845,
    'Maloja': 1846,
    'Moesa': 1847,
    'Plessur': 1848,
    'Prättigau/Davos': 1849,
    'Surselva': 1850,
    'Viamala': 1851,
}


limit = '100'
url = 'https://services1.arcgis.com/YAuo6vcW85VPu7OE/arcgis/rest/services/Fallzahlen_Pro_Region/FeatureServer/0/query?f=json&where=Datum%3E%3Dtimestamp%20%272020-02-01%2000%3A00%3A00%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Region%20asc&resultOffset=0&resultRecordCount=10000&resultType=standard&cacheHint=true'


resp = requests.get(url=url)
json_data = resp.json()

print(sc.DistrictData.header())

for attributes in json_data['features']:
    element = attributes['attributes']

    dd = sc.DistrictData(canton='GR', district=element['Region'])
    dd.url = url
    date = datetime.datetime.utcfromtimestamp(element['Datum'] / 1000)
    dd.date = date.date().isoformat()
    dd.total_cases = element['Faelle__kumuliert_']
    dd.new_cases = element['Neue_Faelle']
    dd.total_deceased = element['Verstorbene__kumuliert_']
    dd.new_deceased = element['Verstorbene']
    if dd.district in inhabitants:
        dd.population = inhabitants[dd.district]
    if dd.district in district_ids:
        dd.district_id = district_ids[dd.district]
    print(dd)
