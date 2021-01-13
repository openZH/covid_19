#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import scrape_common as sc

html_url = 'https://www.besondere-lage.sites.be.ch/de/start/news/fallzahlen.html'
d = sc.download(html_url, silent=True)

soup = BeautifulSoup(d, 'html.parser')

for caption in soup.find_all('caption'):
    if caption.get_text() == 'Anzahl durchgeführte SARS-Cov-2 PCR-Tests':
        weeklytable = caption.find_parents('table')
    if caption.get_text() == 'Corona-Erkrankungen im Kanton Bern':
        dailytable = caption.find_parents('table')


# weekly tests
year = '2021'
for t in weeklytable:
    headers = [" ".join(cell.stripped_strings) for cell in t.find('tr').find_all('th')]

    for row in [r for r in t.find_all('tr') if r.find_all('td')]:
        td = sc.TestData(canton='BE', url=html_url)

        for col_num, cell in enumerate(row.find_all(['td'])):
            value = " ".join(cell.stripped_strings)
            if value:
                value = re.sub(r'[^\d\.]', '', value)

            if sc.find(r'^(Kalender.*)', headers[col_num]) is not None:
                td.week = value
                if( int(td.week) == 53 ):
                    year = '2020'
                td.year = year
            elif sc.find(r'^(Durchge.*Tests)', headers[col_num]):
                td.total_tests = int(value)
            elif sc.find(r'^(davon.*positiv)', headers[col_num]):
                td.positive_tests = int(value)
            elif sc.find(r'^(Positivit.ts.*)', headers[col_num]):
                td.positivity_rate = value

        if td:
            print(td)

# daily tests
for t in dailytable:
    headers = [" ".join(cell.stripped_strings) for cell in t.find('tr').find_all('th')]

    for row in [r for r in t.find_all('tr') if r.find_all('td')]:
        td = sc.TestData(canton='BE', url=html_url)

        for col_num, cell in enumerate(row.find_all(['td'])):
            value = " ".join(cell.stripped_strings)
            if value:
                value = re.sub(r'[^\d\.\ ]', '', value)

            if sc.find(r'^(Datum)', headers[col_num]) is not None:
                dateArr = re.search(r'(\d{2}).(\d{2}).(\d{2})', value)
                value = dateArr.group(0)
                date = sc.date_from_text(value).isoformat()
                td.start_date = date
                td.end_date = date
            elif sc.find(r'^(Durch-)', headers[col_num]):
                td.total_tests = int(value)

        if td:
            print(td)
