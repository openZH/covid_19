#!/usr/bin/env python3

import csv
from io import StringIO
import scrape_common as sc
import scrape_tg_common as stc


def get_value(row, key):
    value = row[key]
    if value != '':
        return value
    return None


url = stc.get_tg_main_csv_url()
d_csv = sc.download(url, silent=True)

reader = csv.DictReader(StringIO(d_csv), delimiter=';')
for row in reader:
    if not row['date']:
        continue
    vd = sc.VaccinationData(canton='TG', url=row['source'])
    date = row['date']
    date = sc.date_from_text(date)
    vd.start_date = date.isoformat()
    vd.end_date = date.isoformat()
    vd.total_vaccinations = get_value(row, 'total_vaccinations')
    vd.doses_delivered = get_value(row, 'doses_delivered')
    if vd:
        print(vd)
