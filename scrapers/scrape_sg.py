#!/usr/bin/env python3

import re
import datetime
import sys
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://www.sg.ch/tools/informationen-coronavirus.html'
d = sc.download(url, silent=True)
d = d.replace('&nbsp;', ' ')

soup = BeautifulSoup(d, 'html.parser')

# hospitalized

dd_hosp = sc.DayData(canton='SG', url=url)
hosp_table = soup.find(string=re.compile(r"Spit.*?ler:\s+Covid-19-Patienten\s+im\s+Kanton\s+St\.\s*Gallen")).find_next('table')
table_text = " ".join(hosp_table.stripped_strings)

hosp_date = hosp_table.find_next(string=re.compile("Stand")).string
dd_hosp.datetime = sc.find(r'Stand:?\s*(.+[0-9]{4})', hosp_date)

rows = hosp_table.find_all('tr')

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 2, f"Number of header columns changed, {len(headers)} != 2"
assert headers[0].text.strip() == "Covid-19 Patienten in St.Galler Spitälern"
assert headers[1].text == "Anzahl"

for i in range(1, len(rows)):
    cells = rows[i].find_all('td')
    if cells[0].text.strip() == 'Total Covid-19 Patienten':
        dd_hosp.hospitalized = cells[1].text
    elif cells[0].text.strip() == 'davon auf Intensivstation ohne Beatmung':
        dd_hosp.icu = cells[1].text
    elif cells[0].text.strip() == 'davon auf Intensivstation mit Beatmung':
        dd_hosp.vent = cells[1].text

print(dd_hosp)

print('-' * 10)

# cases

dd_cases = sc.DayData(canton='SG', url=url)
cases_table = soup.find(string=re.compile(r"Aktuelle\s+Lage\s+im\s+Kanton\s+St\.\s*Gallen")).find_next('table')
table_text = " ".join(cases_table.stripped_strings)
dd_cases.datetime = sc.find(r'Datenstand:\s+([0-9]+\.\s*[0-9]{2}\.\s*[0-9]{4})', table_text)

rows = cases_table.find_all('tr')
assert len(rows) == 3, f"Number of rows changed, {len(rows)} != 3"

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 3, f"Number of header columns changed, {len(headers)} != 3"
assert headers[1].text == "Anzahl"

case_cells = rows[1].find_all('td')
assert len(case_cells) == 3, f"Number of columns changed, {len(case_cells)} != 3"
assert case_cells[0].text == 'Laborbestätigte Fälle (kumuliert)'
dd_cases.cases = case_cells[1].string

death_cells = rows[2].find_all('td')
assert len(death_cells) == 3, f"Number of columns changed, {len(death_cells)} != 3"
assert death_cells[0].text == 'Verstorbene (kumuliert)'
dd_cases.deaths = death_cells[1].string

print(dd_cases)
print('-' * 10)

# isolated / quarantined cases

isolation_table = soup.find(string=re.compile(r"Contact Tracing: Anzahl der betreuten Personen")).find_next('table')

dd_isolation = sc.DayData(canton='SG', url=url)
dd_isolation.datetime = sc.find('Stand ([0-9]{2}.[0-9]{2}.[0-9]{4} [0-9]{2}:[0-9]{2})h', isolation_table.text)
dd_isolation.isolated = isolation_table.find(string=re.compile(r'Indexf.lle im Tracing / in Isolation')).find_next('td').find_next('td').text
dd_isolation.quarantined = isolation_table.find(string=re.compile(r'Kontaktpersonen im Tracing / in Quarant.ne')).find_next('td').find_next('td').text

print(dd_isolation)
