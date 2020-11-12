#!/usr/bin/env python3

import csv
from io import StringIO
import re
import datetime
from bs4 import BeautifulSoup
import scrape_common as sc


def fix_lu_date(date):
    res = re.match(r'(20\d{2})/(\d+)/(\d+)', date)
    assert res, 'date could not be matched!'
    date = datetime.date(int(res[1]), int(res[2]) + 1, int(res[3]))
    return date.isoformat()


hosp_url = 'https://www.lustat.ch/analysen/gesundheit/corona-reporting/hospitalisationen'
hosp_csv = 'https://www.lustat.ch/files_ftp/daten/covid/cov_hospitalisationen.csv'

is_first = True
data = sc.download(hosp_csv, silent=True, encoding='utf-8-sig')
reader = csv.DictReader(StringIO(data), delimiter=';')
for row in reader:
    dd = sc.DayData(canton='LU', url=hosp_url)
    dd.datetime = fix_lu_date(row['utcdatum'])
    dd.hospitalized = row['current_hosp']
    dd.vent = row['current_vent']
    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)


cases_url = 'https://www.lustat.ch/analysen/gesundheit/corona-reporting/entwicklungen-seit-maerz-2020'
cases_csv = 'https://www.lustat.ch/files_ftp/daten/covid/cov_faelle_g2.csv'

data = sc.download(cases_csv, silent=True, encoding='utf-8-sig')
reader = csv.DictReader(StringIO(data), delimiter=';')
for row in reader:
    dd = sc.DayData(canton='LU', url=cases_url)
    dd.datetime = fix_lu_date(row['utcdatum'])
    dd.cases = row['cumnew_conf']
    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)


deceased_csv = 'https://www.lustat.ch/files_ftp/daten/covid/cov_todesfaelle.csv'

is_first = True
data = sc.download(deceased_csv, silent=True, encoding='utf-8-sig')
reader = csv.DictReader(StringIO(data), delimiter=';')
deaths = 0
for row in reader:
    dd = sc.DayData(canton='LU', url=cases_url)
    dd.datetime = fix_lu_date(row['utcdatum'])
    deaths += int(row['new_deceased'])
    dd.deaths = deaths
    if dd:
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)


url = 'https://www.lustat.ch/analysen/gesundheit/corona-reporting'
d = sc.download(url, silent=True)
soup = BeautifulSoup(d, 'html.parser')
header = soup.find('h2', string=re.compile(r'Aktuellste Zahlen'))
paragraph = header.find_next('p')
date = sc.find(r'Am (\d+\.\d+\.20\d{2})', paragraph.text)
table = header.find_next('table')

for row in table.find_all('tr'):
    columns = row.find_all('td')
    if len(columns) == 2:
        dd = sc.DayData(canton='LU', url=url)
        dd.datetime = date
        category = columns[0].text
        value = columns[1].text.replace(' ', '')
        if category == 'In Isolation':
            dd.isolated = value
        if category == 'In Quarantäne':
            dd.quarantined = value
        if category == 'Reiserückkehrer in Quarantäne':
            dd.quarantine_riskareatravel = value

        if dd:
            if not is_first:
                print('-' * 10)
            is_first = False
            print(dd)
