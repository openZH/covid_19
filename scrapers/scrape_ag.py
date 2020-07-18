#!/usr/bin/env python3

from bs4 import BeautifulSoup
import scrape_common as sc

# fetch latest data from HTML table
url = 'https://www.ag.ch/de/themen_1/coronavirus_2/coronavirus.jsp'
d = sc.download(url, silent=True)
d = d.replace("’", "")
d = d.replace("'", "")

dd = sc.DayData(canton='AG', url=url)

date = sc.find(r'Stand: (?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag), (.+? Uhr)', d)
dd.datetime = date

soup = BeautifulSoup(d, 'html.parser')
rows = []
for t in soup.find_all('table'):
    headers = [" ".join(cell.stripped_strings) for cell in t.find('tr').find_all('th')]

    for row in [r for r in t.find_all('tr') if r.find_all('td')]:

        cells = row.find_all(['td'])

        col_num = 0
        for cell in cells:
            row_header = headers[col_num]
            col_header = cells[0].string
            value = cell.string
            if row_header == 'Gesamtzahl':
                if col_header == 'Laborbestätigte Fälle':
                    dd.cases = value
                if col_header == 'Todesfälle':
                    dd.deaths = value
            if row_header == 'Aktuell betreute Personen':
                if col_header == 'Infizierte Personen in Isolation':
                    dd.isolated = value
                if col_header == 'Kontaktpersonen in Quarantäne':
                    dd.quarantined = value
            col_num += 1

print(dd)
