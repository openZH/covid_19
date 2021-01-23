#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import requests
import scrape_common as sc


main_url = 'https://monitoring.unisante.ch/d/krLTmEfGk/donnees-vaccination-covid-19-vaud'
url = 'https://monitoring.unisante.ch/api/tsdb/query'

from_date = int(datetime.datetime(year=2021, month=1, day=1).timestamp() * 1000)
to_date = int(datetime.datetime.today().timestamp() * 1000)

query = {"from": f"{from_date}","to": f"{to_date}","queries":[{"refId":"A","intervalMs":1800000,"maxDataPoints":518,"datasourceId":11,"rawSql":"SELECT\r\n  count(hash) as \"Nombre de vaccinations\",\r\n  date(first_vac_date) as time\r\nFROM monitoring_lines_public\r\nWHERE first_vac_date is not null and done_elsewhere_first = '0' and  $__timeFilter(first_vac_date)\r\nGROUP by date(first_vac_date)","format":"time_series"}]}

req = requests.post(url, json=query)
data = req.json()

assert data['results']['A']['series'][0]['name'] == 'Nombre de vaccinations'
points = data['results']['A']['series'][0]['points']

for point in points:
    date = datetime.date.fromtimestamp(point[1] / 1000)
    vd = sc.VaccinationData(canton='VS', url=main_url)
    vd.start_date = date.isoformat()
    vd.end_date = date.isoformat()
    vd.total_vaccinations = point[0]
    print(vd)
