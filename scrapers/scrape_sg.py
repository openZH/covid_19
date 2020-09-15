#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc

# hospitalized
url_hospitalized = 'https://stada.sg.ch/covid/C19_Faelle_hospitalisiert.html'
soup = BeautifulSoup(sc.download(url_hospitalized, silent=True), 'html.parser')
dd_hosp = sc.DayData(canton='SG', url=url_hospitalized)
hosp_table = soup.find('table')

hosp_date = hosp_table.find_next(string=re.compile("Stand")).string
dd_hosp.datetime = sc.find(r'Stand:?\s*(.+[0-9]{4})', hosp_date)

rows = hosp_table.find_all('tr')

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 2, f"Number of header columns changed, {len(headers)} != 2"
assert headers[1].text.strip() == "Anzahl"

for i in range(1, len(rows)):
    cells = rows[i].find_all('td')
    if cells[0].text.strip() == 'Total Covid-19 Patienten':
        dd_hosp.hospitalized = cells[1].text
    elif cells[0].text.strip() == '...davon auf Intensivstation ohne Beatmung':
        dd_hosp.icu = int(cells[1].text)
    elif cells[0].text.strip() == '...davon auf Intensivstation mit Beatmung':
        dd_hosp.vent = int(cells[1].text)

if dd_hosp.vent:
    dd_hosp.icu += dd_hosp.vent
print(dd_hosp)

print('-' * 10)

# isolated / quarantined cases
url_isolated = 'https://stada.sg.ch/covid/ContactTracing.html'
soup = BeautifulSoup(sc.download(url_isolated, silent=True), 'html.parser')
dd_isolated = sc.DayData(canton='SG', url=url_isolated)
isolated_table = soup.find('table')

isolated_date = isolated_table.find_next(string=re.compile("Stand")).string
dd_isolated.datetime = sc.find(r'Stand:?\s*(.+[0-9]{4})', isolated_date)

rows = isolated_table.find_all('tr')

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 2, f"Number of header columns changed, {len(headers)} != 2"
assert headers[1].text.strip() == "Anzahl"

for i in range(1, len(rows)):
    cells = rows[i].find_all('td')
    if cells[0].text.strip() == 'Positiv Getestete im Tracing / in Quarantäne':
        tmp = cells[1].text.strip()
        if tmp != '...':
            dd_isolated.isolated = tmp
    elif cells[0].text.strip() == 'Kontaktpersonen im Tracing / in Quarantäne':
        tmp = cells[1].text.strip()
        if tmp != '...':
            dd_isolated.quarantined = int(tmp)

if dd_isolated.isolated is not None or dd_isolated.quarantined is not None:
    print(dd_isolated)
    print('-' * 10)

# cases
url_cases = 'https://stada.sg.ch/covid/BAG_uebersicht.html'
soup = BeautifulSoup(sc.download(url_cases, silent=True), 'html.parser')
dd_cases = sc.DayData(canton='SG', url=url_cases)
cases_table = soup.find('table')

hosp_date = cases_table.find_next(string=re.compile("Stand")).string
dd_cases.datetime = sc.find(r'Stand:?\s*(.+[0-9]{4})', hosp_date)

rows = cases_table.find_all('tr')

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 2, f"Number of header columns changed, {len(headers)} != 2"
assert headers[1].text.strip() == "Anzahl"

for row in rows:
    cells = row.find_all('td')
    if len(cells) == 2:
        if cells[0].text.strip() == 'Laborbestätigte Fälle kumuliert (seit März 2020)':
            dd_cases.cases = cells[1].string
        elif cells[0].text.strip() == 'Todesfälle kumuliert (seit März 2020)':
            dd_cases.deaths = cells[1].string

print(dd_cases)
