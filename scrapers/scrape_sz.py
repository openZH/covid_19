#!/usr/bin/env python3

import scrape_common as sc

print('SZ')

xls = sc.xlsdownload('https://www.sz.ch/public/upload/assets/45951/COVID-19_Fallzahlen_Kanton_Schwyz.xlsx')
sc.timestamp()

sheet = xls.sheet_by_index(0)
last_row = sheet.nrows - 1

date_value = sheet.cell_value(last_row, 0)
current_date = sc.xldate_as_datetime(sheet, date_value)
print('Date and time:', current_date.date().isoformat())

cases = int(sheet.cell_value(last_row, 1)) 
print('Confirmed cases:', cases)

deaths = int(sheet.cell_value(last_row, 2))
if deaths:
    print('Deaths:', deaths)

recovered = int(sheet.cell_value(last_row, 3))
if recovered:
    print('Recovered:', recovered)
