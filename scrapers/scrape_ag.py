#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import scrape_common as sc

# get historical data from https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp
data_url = 'https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp'
d = sc.download(data_url, silent=True)

soup = BeautifulSoup(d, 'html.parser')

def parse_table(table, data_url, column_count, parse_fn):
    headers = [" ".join(cell.stripped_strings) for cell in table.find('tr').find_all('th')]
    for row in table.find_all('tr')[1:]:
        dd = sc.DayData(canton='AG', url=data_url)
        cells = row.find_all(['td'])

        assert len(cells) == column_count, f"Number of columns changed: {len(cells)} != {column_count}"

        col_num = 0
        for cell in cells:
            header = headers[col_num]
            value = cell.string
            value = value.replace("’", "")
            value = value.replace("'", "")
            dd = parse_fn(dd, value, header)
            col_num += 1

        print('-' * 10)
        print(dd)

# cases
cases_table = soup.find(string=re.compile(r'Verlauf\s+laborbest.*?tigte\s+F.*?lle')).find_parent('div').find('table')

def parse_cases(dd, value, header):
    if header == 'Datum':
        dd.datetime = sc.find(r'\w+,\s+(.*)$', value)
    if header == 'Gesamtzahl':
        dd.cases = value

    return dd

parse_table(cases_table, data_url, 3, parse_cases)


# deaths
deaths_table = soup.find(string=re.compile(r'Verlauf Todesf.*?lle')).find_parent('div').find('table')

def parse_deaths(dd, value, header):
    if header == 'Datum':
        dd.datetime = sc.find(r'\w+,\s+(.*)$', value)
    if header == 'Gesamtzahl':
        dd.deaths = value

    return dd

parse_table(deaths_table, data_url, 3, parse_deaths)

# isolation
iso_table = soup.find(string=re.compile(r'Verlauf infizierte Personen in Isolation')).find_parent('div').find('table')

def parse_isolation(dd, value, header):
    if header == 'Datum':
        dd.datetime = sc.find(r'\w+,\s+(.*)$', value)
    if header == 'Gesamtzahl aktuell betreuter Personen':
        dd.isolated = value

    return dd

parse_table(iso_table, data_url, 4, parse_isolation)

# quarantined 
q_table = soup.find(string=re.compile(r'Verlauf Kontaktpersonen in Quarant.*?ne')).find_parent('div').find('table')

def parse_quarantined(dd, value, header):
    if header == 'Datum':
        dd.datetime = sc.find(r'\w+,\s+(.*)$', value)
    if header == 'Gesamtzahl aktuell betreuter Personen':
        dd.quarantined = value

    return dd

parse_table(q_table, data_url, 4, parse_quarantined)

# quarantined risk area travel
q_rat_table = soup.find(string=re.compile(r'Quarant.*?ne nach Einreise')).find_parent('div').find('table')

q_rat_date= sc.find(r'Daten\s+von\s+(?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag),\s+(.+)', q_rat_table.find('caption').text)

def parse_quarantined_travel(dd, value, header):
    if header == 'Aktuell betreute Personen':
        dd.quarantine_riskareatravel = value
    dd.datetime = q_rat_date 

    return dd

parse_table(q_rat_table, data_url, 4, parse_quarantined_travel)

# fetch latest data from HTML table
url = 'https://www.ag.ch/de/themen_1/coronavirus_2/coronavirus.jsp'
d = sc.download(url, silent=True)
d = d.replace("’", "")
d = d.replace("'", "")

dd = sc.DayData(canton='AG', url=url)

date = sc.find(r'Stand: (?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag), (.+? Uhr)', d)
if date is None:
    date = sc.find(r'Daten\s+von\s+(?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag),\s+(.+)\s+\(nach Angaben BAG\)', d)
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

print('-' * 10)
print(dd)
