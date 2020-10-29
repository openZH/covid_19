#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import scrape_common as sc

url = 'https://www.fr.ch/sante/covid-19/coronavirus-statistiques-evolution-de-la-situation-dans-le-canton'
d = sc.download(url, silent=True)

soup = BeautifulSoup(d, 'html.parser')

json_data = soup.find('script', type="application/json").string
json_data = json.loads(json_data)
easychart = json_data['easychart']
content = easychart['338566-0-field_graphique_content']

csv = content['csv']
csv = json.loads(csv)

config = content['config']
config = json.loads(config)
xaxis = config['xAxis']
categories = xaxis[0]['categories']

for (tot, pos), week in zip(csv[1:], categories):
    tot = int(tot)
    pos = int(pos)
    td = sc.TestData(canton='FR', url=url)
    td.week = week
    td.year = '2020'
    td.positive_tests = pos
    td.negative_tests = tot - pos
    td.positivity_rate = float(pos / tot) * 100
    td.positivity_rate = round(10 * td.positivity_rate) / 10
    print(td)
