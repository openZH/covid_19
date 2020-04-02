#!/usr/bin/env python3

import json
import scrape_common as sc

print('GR')

d = sc.download('https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/_layouts/15/GenericDataFeed/feed.aspx?PageID=26&ID=g_1175d522_e609_4287_93af_d14c9efd5218&FORMAT=JSONRAW')

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
  {"date":"2020-04-02","time":"","abbreviation_canton_and_fl":"GR","ncumul_tested":"","ncumul_conf":"569","ncumul_hosp":"59","ncumul_ICU":"","ncumul_vent":"","ncumul_released":"","ncumul_deceased":"23","source":"https://www.gr.ch/coronavirus"}]
"""

sc.timestamp()

json_data = json.loads(d)

# Sort by date, just in case. ISO 8601 is used, so we can just sort using strings.
json_data.sort(key=lambda x: x['date'])

last_row = json_data[-1]

# {'date': '2020-03-27', 'time': '', 'abbreviation_canton_and_fl': 'GR', 'ncumul_tested': '', 'ncumul_conf': '409', 'ncumul_hosp': '52', 'ncumul_ICU': '', 'ncumul_vent': '', 'ncumul_released': '', 'ncumul_deceased': '9', 'source': 'https://www.gr.ch/coronavirus'}
if last_row['time']:
  print('Date and time:', '{}T{}'.format(last_row['date'], last_row['time']))
else:
  print('Date and time:', last_row['date'])
if last_row['ncumul_tested']:
  print('Tested:', last_row['ncumul_tested'])
print('Confirmed cases:', last_row['ncumul_conf'])
if last_row['ncumul_hosp']:
  print('Hospitalized:', last_row['ncumul_hosp'])
if last_row['ncumul_ICU']:
  print('ICU:', last_row['ncumul_ICU'])
if last_row['ncumul_vent']:
  print('Vent:', last_row['ncumul_vent'])
if last_row['ncumul_released']:
  print('Recovered:', last_row['ncumul_released'])
if last_row['ncumul_deceased']:
  print('Deaths:', last_row['ncumul_deceased'])
