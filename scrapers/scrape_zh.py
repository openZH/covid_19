#!/usr/bin/env python3

import csv
import re
from io import StringIO
from bs4 import BeautifulSoup
import scrape_common as sc

url = "https://www.zh.ch/de/gesundheit/coronavirus.html"

# get quarantined and isolated from website
dd_iso_q = sc.DayData(canton='ZH', url=url)
d = sc.download(url, silent=True)

soup = BeautifulSoup(d, 'html.parser')
main_table = soup.select_one('#main_table').find_next('table')
captions = soup.select_one('#main_table').find_next_siblings('figcaption')
caption = " ".join([c.text for c in captions])

date_match = re.search(r'Diese Zahlen wurden publiziert am (?P<date>\d+\.\s*\w+\s+20\d{2}) um (?P<time>\d{2}\.\d{2}\s+Uhr)', caption)
dd_iso_q.datetime = f"{date_match['date']} {date_match['time']}"

rows = main_table.find_all('tr')

headers = rows[0].find_all('td') or rows[0].find_all('th')
assert len(headers) == 2, f"Number of header columns changed, {len(headers)} != 2"
assert headers[0].text.strip() == "Kategorie"

for i in range(1, len(rows)):
    header = rows[i].find('th').text.strip()
    value = rows[i].find('td').text.strip()
    value = value.replace("'", "")
    if not sc.represents_int(value):
        continue

    if header == 'Personen in Isolation':
        dd_iso_q.isolated = int(value)
    elif header == 'Personen in Quarantäne':
        dd_iso_q.quarantined = int(value)

print(dd_iso_q)

csv_url = 'https://raw.githubusercontent.com/openzh/covid_19/master/fallzahlen_kanton_zh/COVID19_Fallzahlen_Kanton_ZH_total.csv'
d_csv = sc.download(csv_url, silent=True)
reader = csv.DictReader(StringIO(d_csv), delimiter=',')

for row in reader:
    print('-' * 10)
    dd = sc.DayData(canton='ZH', url=url)
    dd.datetime = f"{row['date']} {row['time']}"
    dd.cases = row['ncumul_conf']
    dd.deaths = row['ncumul_deceased']
    dd.hospitalized = row['current_hosp']
    dd.vent = row['current_vent']
    dd.icu = row['current_icu']
    print(dd)
    



