#!/usr/bin/env python3

import json
import scrape_common as sc

json_url = 'https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/_layouts/15/GenericDataFeed/feed.aspx?PageID=26&ID=g_1175d522_e609_4287_93af_d14c9efd5218&FORMAT=JSONRAW'
d = sc.download(json_url, silent=True)

# 2020-04-02
"""
[
  {"date":"2020-03-18","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"116","ncumul_hosp":"13","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"1","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-19","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"145","ncumul_hosp":"18","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"1","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-20","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"213","ncumul_hosp":"24","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"3","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-21","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"239","ncumul_hosp":"24","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"3","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-22","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"266","ncumul_hosp":"27","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"6","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-23","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"281","ncumul_hosp":"29","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"7","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-24","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"322","ncumul_hosp":"43","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"8","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-25","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"373","ncumul_hosp":"45","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"9","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-26","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"373","ncumul_hosp":"45","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"9","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-27","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"409","ncumul_hosp":"52","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"9","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-30","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"497","ncumul_hosp":"63","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"12","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-03-31","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"513","ncumul_hosp":"58","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"19","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-04-01","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"521","ncumul_hosp":"58","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"21","source":"https://www.gr.ch/coronavirus"},
  {"date":"2020-04-02","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"569","ncumul_hosp":"59","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"23","source":"https://www.gr.ch/coronavirus"}
]
"""

json_data = json.loads(d)

# Sort by date, just in case. ISO 8601 is used, so we can just sort using strings.
json_data.sort(key=lambda x: x['date'])

for i, row in enumerate(json_data):
    print('GR')
    sc.timestamp()
    print('Downloading:', json_url)

    if row['time']:
        print('Date and time:', f"{row['date']}T{row['time']}")
    else:
        print('Date and time:', row['date'])
    if row['ncumul_tested']:
        print('Tested:', row['ncumul_tested'])
    print('Confirmed cases:', row['ncumul_conf'])
    print('Hospitalized:', row['ncumul_hosp'])
    if row['ncumul_ICU']:
        print('ICU:', row['ncumul_ICU'])
    if row['ncumul_vent']:
        print('Vent:', row['ncumul_vent'])
    if row['ncumul_released']:
        print('Recovered:', row['ncumul_released'])
    print('Deaths:', row['ncumul_deceased'])

    if len(json_data) - 1 > i:
        print('-' * 10)

