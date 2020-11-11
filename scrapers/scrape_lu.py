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


start_url = 'https://gesundheit.lu.ch/themen/Humanmedizin/Infektionskrankheiten/Informationen_Coronavirus'
d = sc.download(start_url, silent=True)
soup = BeautifulSoup(d, 'html.parser')
cases_url = soup.find(string=re.compile(r'Aktuelle Zahlen.*Kanton\s+Luzern')).find_previous('a')['href']
if not cases_url.startswith('http'):
    cases_url = f"https://gesundheit.lu.ch{cases_url}"
d = sc.download(cases_url, silent=True)
d = d.replace('&nbsp;', ' ')

case_date_str = sc.find(r'Fallzahlen\s*im\s*Kanton\s*Luzern.*\(Stand:\s*(.+?)\,', d)
hosp_date_str = sc.find(r'Hospitalisierungen.*\(Stand:\s*(.+?)\,', d)
isolated_date_str = sc.find(r'Isolation.*\(Stand:\s*(.+?)\,', d)

soup = BeautifulSoup(d, 'html.parser')
tables = soup.find_all('table')
assert tables, f"Couldn't find tables on {cases_url}"
for table in tables:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='LU', url=cases_url)
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        assert len(cells) == 2, "Number of columns changed, not 2"

        header_str = "".join([str(x) for x in cells[0].contents])

        value_str = cells[1].find('p') or cells[1]
        if value_str is None:
            continue
        value_str = value_str.string.replace('*', '')
        value = int(value_str)
        if re.search('Bestätigte Fälle|Positiv getestet', header_str):
            dd.datetime = case_date_str
            dd.cases = value
        if re.search('Todesfälle', header_str):
            dd.datetime = case_date_str
            dd.deaths = value
        if re.search('Hospitalisiert', header_str):
            dd.datetime = hosp_date_str
            dd.hospitalized = value
        if re.search('Intensivpflege', header_str):
            dd.datetime = hosp_date_str
            dd.icu = value
        if re.search('Personen in Isolation', header_str):
            dd.datetime = isolated_date_str
            dd.isolated = value
        if re.search('Personen in Quarantäne', header_str):
            dd.datetime = isolated_date_str
            dd.quarantined = value

    print(dd)
