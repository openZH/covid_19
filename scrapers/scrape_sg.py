#!/usr/bin/env python3

import csv
from io import StringIO
import re
from bs4 import BeautifulSoup
import scrape_common as sc

main_url = 'https://www.sg.ch/tools/informationen-coronavirus.html'

# hospitalized
url_hospitalized = 'https://stada.sg.ch/covid/C19_Faelle_hospitalisiert.html'
soup = BeautifulSoup(sc.download(url_hospitalized, silent=True), 'html.parser')
dd_hosp = sc.DayData(canton='SG', url=main_url)
hosp_table = soup.find('table')

hosp_date = hosp_table.find_next(string=re.compile("Meldestand")).string
dd_hosp.datetime = sc.find(r'Stand:?\s*(.+[0-9]{4})', hosp_date)

rows = hosp_table.find_all('tr')

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 2, f"Number of header columns changed, {len(headers)} != 2"
assert headers[1].text.strip() == "Anzahl", f"Header text changed '{headers[1].text.strip()}' != 'Anzahl'"

for i in range(1, len(rows)):
    cells = rows[i].find_all('td')
    if cells[0].text.strip() == 'Total Patienten':
        dd_hosp.hospitalized = cells[1].text
    elif cells[0].text.strip() == '...davon auf Intensivstation ohne Beatmung':
        dd_hosp.icu = int(cells[1].text)
    elif cells[0].text.strip() == '...davon auf Intensivstation mit Beatmung':
        dd_hosp.vent = int(cells[1].text)

if dd_hosp.vent:
    dd_hosp.icu += dd_hosp.vent
print(dd_hosp)

print('-' * 10)

"""
# isolated / quarantined cases
url_isolated = 'https://stada.sg.ch/covid/ContactTracing.html'
soup = BeautifulSoup(sc.download(url_isolated, silent=True), 'html.parser')
dd_isolated = sc.DayData(canton='SG', url=main_url)
isolated_table = soup.find('table')

isolated_date = isolated_table.find_next(string=re.compile("Stand")).string
dd_isolated.datetime = sc.find(r'Stand:?\s*(.+[0-9]{4})', isolated_date)

rows = isolated_table.find_all('tr')

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 2, f"Number of header columns changed, {len(headers)} != 2"
assert headers[1].text.strip() == "Anzahl"

for i in range(1, len(rows)):
    cells = rows[i].find_all('td')
    if cells[0].text.strip() == 'Positiv Getestete im Tracing / in Isolation':
        value = cells[1].text.strip()
        if sc.represents_int(value):
            dd_isolated.isolated = int(value)
    elif cells[0].text.strip() == 'Kontaktpersonen im Tracing / in Quarantäne':
        value = cells[1].text.strip()
        if sc.represents_int(value):
            dd_isolated.quarantined = int(value)

if dd_isolated:
    print(dd_isolated)
    print('-' * 10)
"""


# historized cases
csv_url = 'https://www.sg.ch/ueber-den-kanton-st-gallen/statistik/covid-19/_jcr_content/Par/sgch_downloadlist/DownloadListPar/sgch_download.ocFile/KantonSG_C19-Faelle_download.csv'
d = sc.download(csv_url, silent=True)

# strip the "header" / description lines
d = "\n".join(d.split("\n")[5:])

reader = csv.DictReader(StringIO(d), delimiter=';')
for row in reader:
    dd = sc.DayData(canton='SG', url=main_url)
    dd.datetime = row['Falldatum']
    dd.cases = row['Total Kanton SG (kumuliert)']
    print(dd)
    print('-' * 10)


# latest cases
url_cases = 'https://stada.sg.ch/covid/BAG_uebersicht.html'
soup = BeautifulSoup(sc.download(url_cases, silent=True), 'html.parser')
dd_cases = sc.DayData(canton='SG', url=main_url)
cases_table = soup.find('table')

hosp_date = cases_table.find_next(string=re.compile("Stand")).string
dd_cases.datetime = sc.find(r'Stand:?\s*(.+[0-9]{4})', hosp_date)

rows = cases_table.find_all('tr')

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 2, f"Number of header columns changed, {len(headers)} != 2"
assert headers[1].text.strip() == "Anzahl", f"Header text changed '{headers[1].text.strip()}' != 'Anzahl'"

for row in rows:
    cells = row.find_all('td')
    if len(cells) == 2:
        if cells[0].text.strip() == 'Laborbestätigte Fälle kumuliert (seit März 2020)':
            dd_cases.cases = cells[1].text.strip()
        elif cells[0].text.strip() == 'Todesfälle kumuliert (seit März 2020)':
            dd_cases.deaths = cells[1].text.strip()

print(dd_cases)
