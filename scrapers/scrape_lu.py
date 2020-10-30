#!/usr/bin/env python3

import re
import datetime
from bs4 import BeautifulSoup
import scrape_common as sc

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
is_first = True
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
