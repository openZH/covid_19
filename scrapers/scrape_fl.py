#!/usr/bin/env python3

import scrape_common as sc
import sys
import re
from bs4 import BeautifulSoup


# get the daily bulletins
base_url = 'https://www.regierung.li'
d = sc.download(f'{base_url}/ministerien/ministerium-fuer-gesellschaft/medienmitteilungen/', silent=True)
soup = BeautifulSoup(d, 'html.parser')

is_first = True
bulletins = soup.find_all('a', text=re.compile(r'.*Situationsbericht.*'))
for bulletin in bulletins:
    url = f"{base_url}{bulletin.get('href')}"
    bulletin_d = sc.download(url, silent=True)
    bulletin_soup = BeautifulSoup(bulletin_d, 'html.parser')

    dd = sc.DayData(canton='FL', url=url)

    title = bulletin_soup.find('h1', text=re.compile(r'.*Situationsbericht.*'))
    dd.datetime = sc.find(r'Situationsbericht vom (.*? 20\d{2})', title.text)

    content = title.find_next('div').text
    content = re.sub(r'(\d+)’(\d+)', r'\1\2', content)

    dd.cases = sc.find(r"insgesamt\s+([0-9]+)\s+laborbestätigte\s+Fälle", content)
    dd.deaths = sc.find(r'(Damit\s+traten\s+)?(?:bisher|bislang)\s+(traten\s+)?(?P<death>\d+)\s+(Todesfall|Todesfälle)', content, flags=re.I, group='death')

    if re.search(r'Alle\s+weiteren\s+Erkrankten\s+sind\s+in\s+der\s+Zwischenzeit\s+genesen', content):
        dd.recovered = int(dd.cases) - int(dd.deaths)

    m = re.search(r'(\S+)\s+Erkrankte\s+sind\s+derzeit\s+hospitalisiert', content)
    if m:
        dd.hospitalized = sc.int_or_word(m[1].lower())

    m = re.search(r'Gegenwärtig\s+befinden\s+sich\s+(\d+)\s+enge\s+Kontaktpersonen\s+in\s+Quarantäne.', content)
    if m:
        dd.quarantined = m[1]

    if dd:
        if not is_first:
            print('-' * 10)
        print(dd)
        is_first = False


# get the data from PDF file containing full history
history_url = 'https://www.llv.li/files/ag/aktuelle-fallzahlen.pdf'
d = sc.pdfdownload(history_url, layout=True, silent=True)
assert d, f"No content in history PDF found ({history_url})"
data_in_history_found = False
d = re.sub(r'(\d+)’(\d+)', r'\1\2', d)
rows = d.splitlines()
header = rows[2]
assert re.search(r'^Situationsbericht\s+vom\s+Datenstand\s+Anzahl\s+pos\.\s+Fälle\s+genesen\s+hospitalisiert\s+Todesfälle$', header), f"Header in PDF changed: {header}"
for row in rows:
    row = row.replace("'", "")
    m = re.search(r'^(?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag),\s+(?P<report_date>.+?\d{4})\s+(?P<date>.+?\s+Uhr)\s+(?P<cases>\d+)\s+(?P<recovered>\d+)\s+(?P<hosp>\d+)?\s+(?P<deaths>\d+)$', row)
    if m:
        data_in_history_found = True
        dd_full_list = sc.DayData(canton='FL', url=history_url)
        dd_full_list.datetime = m['report_date']
        dd_full_list.cases = m['cases']
        dd_full_list.recovered = m['recovered']
        dd_full_list.hospitalized = m['hosp']
        dd_full_list.deaths = m['deaths']
        if dd_full_list:
            if not is_first:
                print('-' * 10)
            is_first = False
            print(dd_full_list)

assert data_in_history_found, f"Unable to retrieve data from {history_url}"
