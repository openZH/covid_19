#!/usr/bin/env python

import datetime
import requests


class DistrictData:
    __initialized = False
    SEPARATOR = ','

    def __init__(self, canton='', district=''):
        self.date = None
        self.week = None
        self.canton = canton
        self.district = district
        self.population = None
        self.total_cases = None
        self.new_cases = None
        self.total_deceased = None
        self.new_deceased = None
        self.url = None
        self.__initialized = True

    def __setattr__(self, key, value):
        if self.__initialized and not hasattr(self, key):
            raise TypeError('unknown key: {0}'.format(key))
        object.__setattr__(self, key, value)

    def __str__(self):
        res = []
        res.append(self.date or '')
        res.append(self.week or '')
        res.append(self.canton)
        res.append(self.district)
        res.append(str(self.population) or '')
        res.append(str(self.total_cases) or '')
        res.append(str(self.new_cases) or '')
        res.append(str(self.total_deceased) or '')
        res.append(str(self.new_deceased) or '')
        res.append(self.url)
        return DistrictData.SEPARATOR.join(res)

    @staticmethod
    def header():
        return 'Date,Week,Canton,District,Population,TotalConfCases,NewConfCases,TotalDeaths,NewDeaths,SourceUrl'


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


limit = '100'
url = 'https://services1.arcgis.com/YAuo6vcW85VPu7OE/arcgis/rest/services/Fallzahlen_Pro_Region/FeatureServer/0/query?f=json&where=Datum%3E%3Dtimestamp%20%272020-02-01%2000%3A00%3A00%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Region%20asc&resultOffset=0&resultRecordCount=10000&resultType=standard&cacheHint=true'


resp = requests.get(url=url)
json_data = resp.json()

print(DistrictData.header())

for attributes in json_data['features']:
    element = attributes['attributes']

    dd = DistrictData(canton='GR', district=element['Region'])
    dd.url = url
    date = datetime.datetime.utcfromtimestamp(element['Datum'] / 1000)
    dd.date = date.date().isoformat()
    dd.total_cases = element['Faelle__kumuliert_']
    dd.new_cases = element['Neue_Faelle']
    dd.total_deceased = element['Verstorbene__kumuliert_']
    dd.new_deceased = element['Verstorbene']
    if dd.district in inhabitants:
        dd.population = inhabitants[dd.district]
    print(dd)
