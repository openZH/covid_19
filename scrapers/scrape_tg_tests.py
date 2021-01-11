#!/usr/bin/env python3

import re
import scrape_common as sc

url = 'https://statistik.tg.ch/themen-und-daten/covid-19.html/10816'
content = sc.download(url, silent=True)

res = re.search(r".*categories: \[('KW.*)\],", content)
assert res, f'failed to extract weeks, got {res}'
weeks = res[1].split(',')

res = re.search(r".*name: 'Anzahl negativer Tests',\s+color: '.*',\s+data: \[(.*)\],", content)
assert res, f'failed to extract negative tests, got {res}'
negative_tests = res[1].split(',')

res = re.search(r".*name: 'Anzahl positiv getesteter Personen.?',\s+color: '.*',\s+data: \[(.*)\],", content)
assert res, f'failed to extract positive tests, got {res}'
positive_tests = res[1].split(',')

res = re.search(r".*name: 'Positivitätsrate',\s+color: '.*',\s+data: \[(.*)\],", content)
assert res, f'failed to extract positivtiy rate, got {res}'
positivity_rate = res[1].split(',')

assert len(weeks) == len(negative_tests) == len(positive_tests) == len(positivity_rate), f'Expected same length for weeks {len(weeks)}, neg. tests {len(negative_tests)}, pos. tests {len(positive_tests)}, pos. rate {len(positivity_rate)}'

year = '2020'
for week, neg, pos, rate in zip(weeks, negative_tests, positive_tests, positivity_rate):
    td = sc.TestData(canton='TG', url=url)
    td.week = sc.find(r'KW (\d+)', week)
    if int(td.week) == 1:
        year = '2021'
    td.year = year
    td.positive_tests = int(pos)
    td.negative_tests = int(neg)
    td.positivity_rate = float(rate)
    print(td)
