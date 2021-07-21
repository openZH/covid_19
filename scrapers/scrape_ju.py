#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
import sys
import traceback
from bs4 import BeautifulSoup
import requests
import scrape_common as sc


url = 'https://www.jura.ch/fr/Autorites/Coronavirus/Infos-Actualite/Statistiques-COVID/Evolution-des-cas-COVID-19-dans-le-Jura.html'


def download_data():
    json_url = 'https://wabi-west-europe-b-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true'

    req_data = '{"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{"Query":{"Version":2,"From":[{"Name":"t","Entity":"tableau","Type":0}],"Select":[{"Column":{"Expression":{"SourceRef":{"Source":"t"}},"Property":"Date"},"Name":"tableau.Date"},{"Column":{"Expression":{"SourceRef":{"Source":"t"}},"Property":"Nouveaux cas"},"Name":"Sum(tableau.Nouveaux_cas)"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"t"}},"Property":"Cumul des cas confirmÃ©s"}},"Function":0},"Name":"Sum(tableau.Cumul des cas)"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"t"}},"Property":"Cas actuellement hospitalisÃ©s"}},"Function":0},"Name":"Sum(tableau.Hospitalisations)"},{"Column":{"Expression":{"SourceRef":{"Source":"t"}},"Property":"Nouveaux dÃ©cÃ¨s"},"Name":"Sum(tableau.Nouveaux dÃ©cÃ¨s)"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"t"}},"Property":"Cas actuellement en soins intensifs"}},"Function":0},"Name":"Sum(tableau.Cas actuallement en soins intensifs)"}],"Where":[{"Condition":{"Comparison":{"ComparisonKind":2,"Left":{"Column":{"Expression":{"SourceRef":{"Source":"t"}},"Property":"Date"}},"Right":{"Literal":{"Value":"datetime\'2020-02-29T00:00:00\'"}}}}}],"OrderBy":[{"Direction":2,"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"t"}},"Property":"Date"}}}]},"Binding":{"Primary":{"Groupings":[{"Projections":[0,1,2,3,4,5]}]},"DataReduction":{"DataVolume":3,"Primary":{"Window":{"Count":500}}},"Version":1},"ExecutionMetricsKind":1}}]},"QueryId":"","ApplicationContext":{"DatasetId":"5268a522-8bbd-41a0-82c9-c842f7b82739","Sources":[{"ReportId":"f13b6b6f-82a9-40ad-a7ba-64c3c6e7565e","VisualId":"c8ae720f712bb1124e47"}]}}],"cancelQueries":[],"modelId":1961083}'

    http = requests.Session()
    headers = {
        'ActivityId': '13794e30-5afe-4904-a5d4-298294a8ea19',
        'Origin': 'https://app.powerbi.com',
        'Referer': 'https://app.powerbi.com/',
        'RequestId': '978d9a2f-a5c2-d2ae-52af-952ce6951d8c',
        'User-Agent': 'Mozilla Firefox Mozilla/5.0; openZH covid_19 at github',
        'X-PowerBI-ResourceKey': 'ae57abf2-47e2-420e-a5c0-69b0ef3380ab',
    }

    r = http.post(json_url, data=req_data, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()


json = download_data()
json = json['results']
json = json[0]
json = json['result']
json = json['data']
json = json['dsr']
json = json['DS']
json = json[0]
json = json['PH']
json = json[0]
json = json['DM0']

is_first = True
for item in json:
    data = item['C']
    r = None
    if 'R' in item:
        r = item['R']
    if len(data) > 0:
        dd = sc.DayData(canton='JU', url=url)
        date = int(data[0]) / 1000
        dd.datetime = datetime.datetime.utcfromtimestamp(date).isoformat()
        if not r:
            dd.cases = data[3]
            dd.hospitalized = data[4]
            dd.icu = data[5]
        elif r == 4:
            dd.cases = data[2]
            dd.hospitalized = data[3]
            dd.icu = data[4]
        elif r == 6:
            dd.cases = data[2]
            dd.hospitalized = data[3]
        elif r == 16:
            dd.cases = data[3]
            dd.icu = data[4]
        elif r == 20:
            dd.cases = data[2]
            dd.hospitalized = data[3]
        elif r == 36:
            dd.cases = data[2]
            dd.hospitalized = data[3]
        elif r == 44:
            dd.hospitalized = data[2]
        elif r == 46:
            dd.hospitalized = data[1]
        elif r == 38:
            dd.cases = data[1]
            dd.hospitalized = data[2]
        elif r == 52:
            dd.cases = data[2]
        elif r == 54:
            dd.cases = data[1]
        elif r == 60:
            pass
        elif r == 62:
            pass
        else:
            print(f'>>> unexpected r: {r}')

        if dd:
            if not is_first:
                print('-' * 10)
            is_first = False
            print(dd)
