#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import scrape_common as sc

html_url = 'https://www.besondere-lage.sites.be.ch/besondere-lage_sites/de/index/corona/index.html'
d = sc.download(html_url, silent=True)

soup = BeautifulSoup(d, 'html.parser')
for t in soup.find_all('table', {'summary': 'Laufend aktualisierte Zahlen zu den Corona-Erkrankungen im Kanton Bern'}):
    headers = [" ".join(cell.stripped_strings) for cell in t.find('tr').find_all('th')]

    is_first = True
    for row in [r for r in t.find_all('tr') if r.find_all('td')]:
        if not is_first:
            print('-' * 10)
        is_first = False

        dd = sc.DayData(canton='BE', url=html_url)

        for col_num, cell in enumerate(row.find_all(['td'])):
            value = " ".join(cell.stripped_strings)
            if value:
                value = value.replace("'", "")
            if value and '*' in value and not '**' in value:
                # the asteriks (*) indicates a not-current value
                # ** means "Datenkorrektur"
                continue
            if value and '(' in value:
                value = sc.find(r'(\d+)([\s<>br\w]*\(.*\))?', value)

            if headers[col_num] == 'Datum':
                date_string = "".join(list(cell.stripped_strings)[0:-1])
                # TODO remove this, once the source is fixed
                if date_string == '02.01.2020':
                    date_string = '02.01.2021'
                time_string = list(cell.stripped_strings)[-1]
                dd.datetime = f'{date_string} {time_string}'
            elif headers[col_num] == 'Fälle positiv':
                dd.cases = value
            elif 'Todes' in headers[col_num]:
                dd.deaths = value
            elif headers[col_num] == 'Im Spital gesamt':
                dd.hospitalized = value
            elif 'beatmet' in headers[col_num]:
                dd.vent = value
            elif 'Intensiv' in headers[col_num] and 'gesamt' in headers[col_num]:
                dd.icu = value

        print(dd)
