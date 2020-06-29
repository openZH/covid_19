#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

main_url = "https://www.coronavirus.bs.ch/"
soup = BeautifulSoup(sc.download(main_url, silent=True), 'html.parser')
data_portal_url = soup.find('a', string=re.compile(r'Fallzahlen\s+Basel-Stadt'))['href']
json_url = re.sub(
    r'table/$',
    'download/?format=json&timezone=Europe/Zurich&lang=en',
    data_portal_url
)

is_first = True
for record in sorted(sc.jsondownload(json_url, silent=True), key=lambda record: record['fields']['date']):
    dd = sc.DayData(canton='BS', url=json_url)
    dd.datetime = record['fields']['timestamp']
    if 'ncumul_conf' in record['fields']:
        dd.cases = int(record['fields']['ncumul_conf'])
    if 'ncumul_deceased' in record['fields']:
        dd.deaths = int(record['fields']['ncumul_deceased'])
    if 'ncumul_confirmed_non_resident' in record['fields']:
        dd.confirmed_non_resident = int(record['fields']['ncumul_confirmed_non_resident'])
    if 'current_isolated' in record['fields']:
        dd.isolated = int(record['fields']['current_isolated'])
    if 'current_quarantined' in record['fields']:
        dd.quarantined = int(record['fields']['current_quarantined'])
    if 'current_icu' in record['fields']:
        dd.icu = int(record['fields']['current_icu'])
    if 'current_hosp' in record['fields']:
        dd.hospitalized = int(record['fields']['current_hosp'])
    if 'current_hosp_non_resident' in record['fields']:
        dd.hosp_non_resident = int(record['fields']['current_hosp_non_resident'])
    if 'ncumul_released' in record['fields']:
        dd.recovered = int(record['fields']['ncumul_released'])

    if not is_first:
        print('-' * 10)
    is_first = False
    print(dd)

