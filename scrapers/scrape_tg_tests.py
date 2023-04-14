#!/usr/bin/env python3

import re
import scrape_common as sc

url = 'https://statistik.tg.ch/themen-und-daten/covid-19.html/10816'
content = sc.download(url, silent=True)

res = re.search(r".*name: '2020',\s+categories: \[\'(.*)\]\s+}", content)
assert res, f'failed to extract 2020 weeks, got {res}'
weeks_2020 = res[1].split(',')

res = re.search(r".*name: '2021',\s+categories: \[\'(.*)\]\s+}", content)
assert res, f'failed to extract 2021 weeks, got {res}'
weeks_2021 = res[1].split(',')

res = re.search(r".*name: '2022',\s+categories: \[\'(.*)\]\s+}", content)
assert res, f'failed to extract 2022 weeks, got {res}'
weeks_2022 = res[1].split(',')

res = re.search(r".*name: '2023',\s+categories: \[\'(.*)\]\s+}", content)
assert res, f'failed to extract 2023 weeks, got {res}'
weeks_2023 = res[1].split(',')

weeks = weeks_2020 + weeks_2021 + weeks_2022 + weeks_2023
years = ['2020'] * len(weeks_2020) + ['2021'] * len(weeks_2021) + ['2022'] * len(weeks_2022) + ['2023'] * len(weeks_2023)

res = re.search(r".*name: 'Anzahl negativer Tests.?',\s+color: '.*',\s+data: \[(.*)\],", content)
assert res, f'failed to extract negative tests, got {res}'
negative_tests = res[1].split(',')

res = re.search(r".*name: 'Anzahl positiver Tests.?',\s+color: '.*',\s+data: \[(.*)\],", content)
assert res, f'failed to extract positive tests, got {res}'
positive_tests = res[1].split(',')

res = re.search(r".*name: 'Positivitätsrate',\s+color: '.*',\s+data: \[(.*)\],", content)
assert res, f'failed to extract positivtiy rate, got {res}'
positivity_rate = res[1].split(',')

assert len(weeks) == len(negative_tests) == len(positive_tests) == len(positivity_rate), f'Expected same length for weeks {len(weeks)}, neg. tests {len(negative_tests)}, pos. tests {len(positive_tests)}, pos. rate {len(positivity_rate)}'

for week, year, neg, pos, rate in zip(weeks, years, negative_tests, positive_tests, positivity_rate):
    td = sc.TestData(canton='TG', url=url)
    td.week = sc.find(r'KW (\d+)', week)
    td.year = year
    td.positive_tests = int(pos)
    td.negative_tests = int(neg)
    td.positivity_rate = float(rate)
    print(td)
