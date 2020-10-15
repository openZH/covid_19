#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from bs4 import BeautifulSoup
import scrape_common as sc


def split_whitespace(text):
    if not text:
        return []
    text = re.sub(r'\s\s+', ' ', text)
    return text.split(' ')


d = sc.download('https://www.gl.ch/verwaltung/finanzen-und-gesundheit/gesundheit/coronavirus.html/4817', silent=True)
soup = BeautifulSoup(d, 'html.parser')

# weekly pdf
pdf_url = soup.find('a', string=re.compile(r'Grafik zur.*')).get('href')
pdf = sc.download_content(pdf_url, silent=True)
content = sc.pdftotext(pdf, page=1)
pdf_date = sc.find(r'Stand: (\d{2}\.\d{2}.\d{4})', content)
pdf_date = sc.date_from_text(pdf_date)
print(pdf_date)

content = sc.pdftotext(pdf, page=2, layout=True)
dates = split_whitespace(sc.find(r'\n\s+(\d+\.\d+\s+\d+\.\d+\s+.*)\n\s+Massenquarant.ne', content))
travel_q = split_whitespace(sc.find(r'\n\s+Einreisequarant.ne\s+(\d.*)\n', content))
isolation = split_whitespace(sc.find(r'\n\s+Isolation\s+(\d.*)\n', content))
quarantined = split_whitespace(sc.find(r'\n\s+KP Quarant.ne\s+(\d.*)\n', content))
ips = split_whitespace(sc.find(r'\n\s+Covid Patienten in IPS\s+(\d.*)\n', content))

is_first = True
if len(dates) == len(travel_q) == len(isolation) == len(quarantined) == len(ips):
    for date, tq, iso, qua, ip in zip(dates, travel_q, isolation, quarantined, ips):
        dd = sc.DayData(canton='GL', url=pdf_url)
        dd.datetime = f'{date}.{pdf_date.year}'
        dd.quarantine_riskareatravel = tq
        dd.isolated = iso
        dd.quarantined = qua
        dd.icu = ip
        if not is_first:
            print('-' * 10)
        is_first = False
        print(dd)
else:
    print('PDF data is inconsistent!', file=sys.stderr)
    print(f'dates: {len(dates)}, travel quarantined: {len(travel_q)},  isolation: {len(isolation)},  quarantined: {len(quarantined)}, IPS: {len(ips)}', file=sys.stderr)


# excel sheet
xls_url = soup.find('a', string=re.compile(r'.*Dokument\s*\[xlsx.*')).get('href')

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls)
for row in rows:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='GL', url=xls_url)
    dd.datetime = row['Datum'].date().isoformat()
    if row['Zeit']:
        dd.datetime = dd.datetime + ' ' + row['Zeit'].time().isoformat()
    dd.cases = row['Bestätigte Fälle (kumuliert)']
    dd.hospitalized = row['Personen in Spitalpflege']
    dd.deaths = row['Todesfälle (kumuliert)']
    print(dd)
