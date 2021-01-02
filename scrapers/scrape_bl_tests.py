#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import scrape_common as sc
import scrape_bl_common as sbc
from datetime import timedelta


# weekly data
bulletin_urls = sbc.get_all_bl_bulletin_urls()
for bulletin_url in bulletin_urls:
    bulletin_content = sc.download(bulletin_url, silent=True)
    soup = BeautifulSoup(bulletin_content, 'html.parser')
    content = soup.find(string=re.compile(r'Per heute .*')).string
    content = sbc.strip_bl_bulletin_numbers(content)

    date = sc.find(r'Per heute \w+, (\d+\. \w+ 20\d{2})', content)
    date = sc.date_from_text(date)
    # previous week
    date = date - timedelta(days=7)

    td = sc.TestData(canton='BL', url=bulletin_url)
    td.week = date.isocalendar()[1]
    td.year = date.year
    td.total_tests = sc.find(r'In der Vorwoche wurden (\d+) PCR-Tests', content)
    td.positivity_rate = sc.find(r'von diesen waren (\d+\.?,?\d?) Prozent positiv', content)
    if td.total_tests and td.positivity_rate:
        td.positivity_rate = td.positivity_rate.replace(',', '.')
        print(td)


# daily data
main_url = 'https://www.baselland.ch/politik-und-behorden/direktionen/volkswirtschafts-und-gesundheitsdirektion/amt-fur-gesundheit/medizinische-dienste/kantonsarztlicher-dienst/aktuelles/covid-19-faelle-kanton-basel-landschaft/covid-19-bl-tests'
main_content = sc.download(main_url, silent=True)
soup = BeautifulSoup(main_content, 'html.parser')

def create_bs_test_data(date):
    td = sc.TestData(canton='BL', url=main_url)
    td.start_date = date
    td.end_date = date
    return td

tests_data = {}

for iframe in soup.find_all('iframe'):
    iframe_url = iframe['src']
    d = sc.download(iframe_url, silent=True)
    d = d.replace('\n', ' ')

    # Taegliche PCR-Tests BL
    data = sc.find(r'<pre id="data[^"]*".*?> ?Datum,&quot;Negative PCR-Tests&quot;,&quot;Positive PCR-Tests&quot;\s*([^<]+)</pre>', d)
    if data:
        for row in data.split(" "):
            c = row.split(',')
            date = sc.date_from_text(c[0].replace('-', '.'))
            date = date.isoformat()
            if date not in tests_data:
                tests_data[date] = create_bs_test_data(date)
            tests_data[date].negative_tests = round(float(c[1]))
            tests_data[date].positive_tests = round(float(c[2]))
        continue

    # Taegliche Positivitaetsrate BL
    data = sc.find(r'<pre id="data[^"]*".*?> ?Datum,&quot;T.gliche Positivit.tsrate BL in %&quot;\s*([^<]+)</pre>', d)
    if data:
        for row in data.split(" "):
            c = row.split(',')
            date = sc.date_from_text(c[0].replace('-', '.'))
            date = date.isoformat()
            if date not in tests_data:
                tests_data[date] = create_bs_test_data(date)
            tests_data[date].positivity_rate = c[1]
        continue

for date, td in tests_data.items():
    print(td)
