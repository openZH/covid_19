#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc

print('GL')
d = sc.download('https://www.gl.ch/verwaltung/finanzen-und-gesundheit/gesundheit/coronavirus.html/4817')
sc.timestamp()


soup = BeautifulSoup(d, 'html.parser')
box = soup.find('div', class_="box--error")
xls_url = box.find('a', string=re.compile(r'.*Dokument.*')).get('href')
xls = sc.xlsdownload(xls_url)
sc.timestamp()

sheet = xls.sheet_by_index(0)
last_row = sheet.nrows - 1

date_value = sheet.cell_value(last_row, 0)
current_date = sc.xldate_as_datetime(sheet, date_value)
print('Date and time:', current_date.date().isoformat())

cases = int(sheet.cell_value(last_row, 1)) 
print('Confirmed cases:', cases)

hosp = int(sheet.cell_value(last_row, 2))
if hosp:
    print('Hospitalized:', hosp)

deaths = int(sheet.cell_value(last_row, 3))
if deaths:
    print('Deaths:', deaths)
