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
assert len(rows) == 2, f"Number of rows changed, {len(rows)} != 2"

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 3, f"Number of header columns changed, {len(headers)} != 3"
assert headers[0].text.strip() == "Total Covid-19-Patienten"
assert headers[1].text == "Patienten auf der Intensivstation"
assert headers[2].text == "Davon Patienten mit Beatmung"

cells = rows[1].find_all('td')
assert len(cells) == 3, f"Number of columns changed, {len(cells)} != 3"

dd_hosp.hospitalized = cells[0].text
dd_hosp.icu = cells[1].text
dd_hosp.vent = cells[2].text

print(dd_hosp)

print('-' * 10)

# cases

dd_cases = sc.DayData(canton='SG', url=url)
cases_table = soup.find(string=re.compile(r"Aktuelle\s+Lage\s+im\s+Kanton\s+St\.\s*Gallen")).find_next('table')
table_text = " ".join(cases_table.stripped_strings)
dd_cases.datetime = sc.find(r'Stand ([0-9]+\.\s*[A-Za-z]*\s*[0-9]{4})', table_text)

rows = cases_table.find_all('tr')
assert len(rows) == 3, f"Number of rows changed, {len(rows)} != 3"

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 3, f"Number of header columns changed, {len(headers)} != 3"
assert headers[1].text == "Anzahl"

case_cells = rows[1].find_all('td')
assert len(case_cells) == 3, f"Number of columns changed, {len(case_cells)} != 3"
assert case_cells[0].text == 'Laborbestätigte Fälle (kummuliert)'
dd_cases.cases = case_cells[1].string

death_cells = rows[2].find_all('td')
assert len(death_cells) == 3, f"Number of columns changed, {len(death_cells)} != 3"
assert death_cells[0].text == 'Verstorbene (kummuliert)'
dd_cases.deaths = death_cells[1].string

print(dd_cases)

