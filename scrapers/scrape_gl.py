#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from bs4 import BeautifulSoup
import csv
from io import StringIO
import scrape_common as sc
import scrape_gl_common as sgc

def split_whitespace(text):
    if not text:
        return []
    text = re.sub(r'\s\s+', ' ', text)
    return text.split(' ')

is_first = True

# weekly pdf
pdf_url = sgc.get_gl_pdf_url()
if pdf_url is not None:
    pdf = sc.download_content(pdf_url, silent=True)
    content = sc.pdftotext(pdf, page=1)
    content = re.sub(r'(\d+)\'(\d+)', r'\1\2', content)
    content = re.sub(r'(\d+)’(\d+)', r'\1\2', content)

    pdf_date = sc.find(r'Stand: (\d{2}\.\d{2}.\d{4})', content)
    pdf_date = sc.date_from_text(pdf_date)

    number_of_tests = sc.find(r'PCR-Tests/Schnelltests\sKanton Glarus\s(\d+)\s', content)
    if number_of_tests:
            dd = sc.DayData(canton='GL', url=pdf_url)
            dd.datetime = pdf_date
            dd.tested = number_of_tests
            is_first = False
            print(dd)


    content = sc.pdftotext(pdf, page=2, raw=True)
    dates = split_whitespace(sc.find(r'\n(\d+\.\d+\s+\d+\.\d+\s+.*)\nAnzahl\s+in\s+Isolation', content))
    isolation = split_whitespace(sc.find(r'\nAnzahl\s+in\s+Isolation\s+(\d.*)\n', content))
    quarantined = split_whitespace(sc.find(r'\nKontaktpersonen\s+in\s+Quarant.ne\s+(\d.*)\n', content))

    if len(dates) == len(isolation) == len(quarantined):
        for date, iso, qua in zip(dates, isolation, quarantined):
            if sc.find(r'(\d{2}\.12)', date):
                year = '2020'
            else:
                year = pdf_date.year
            dd = sc.DayData(canton='GL', url=pdf_url)
            dd.datetime = f'{date}.{year}'
            dd.isolated = iso
            dd.quarantined = qua
            if not is_first:
                print('-' * 10)
            is_first = False
            print(dd)
    else:
        print('PDF data is inconsistent!', file=sys.stderr)
        print(f'dates: {len(dates)}, isolation: {len(isolation)},  quarantined: {len(quarantined)}', file=sys.stderr)


# CSV from Google Spreadsheets
main_url = 'https://docs.google.com/spreadsheets/d/1Q7VoxM6wvbdsC84DLWrzyNymkcxUKqIXHy6BpB2Ez0k/edit#gid=0'
csv_url = 'https://docs.google.com/spreadsheets/d/1Q7VoxM6wvbdsC84DLWrzyNymkcxUKqIXHy6BpB2Ez0k/export?format=csv&id=1Q7VoxM6wvbdsC84DLWrzyNymkcxUKqIXHy6BpB2Ez0k&gid=0'
d_csv = sc.download(csv_url, silent=True)

reader = csv.DictReader(StringIO(d_csv), delimiter=',')
for row in reader:
    if row['Datum'] == '':
        continue
    if not is_first:
        print('-' * 10)
    is_first = False
    dd = sc.DayData(canton='GL', url=main_url)
    dd.datetime = row['Datum']
    dd.cases = row['Fallzahlen Total']
    dd.hospitalized = row['Personen in Spitalpflege']
    dd.deaths = row['Todesfälle (kumuliert)']
    print(dd)
