#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
import scrape_common as sc
import scrape_so_common as soc


pdf_urls = soc.get_all_weekly_pdf_urls()
# start with the oldest PDF to have the most recent ones last
pdf_urls.reverse()
for pdf_url in pdf_urls:
    content = sc.pdfdownload(pdf_url, layout=True, silent=True, page=1)
    # remove ' separator to simplify pattern matching
    content = re.sub(r'(\d)\'(\d)', r'\1\2', content)

    date = sc.find(r'S\s?tand: (\d+\.\d+\.20\d{2})', content)
    date = sc.date_from_text(date)
    year1 = (date - datetime.timedelta(weeks=2)).year
    year2 = (date - datetime.timedelta(weeks=1)).year
    res = re.match(r'.*Woche (?P<w1>\d+)(\s+\(\d+\.\d+-\d+\.\d+\))?\s+Woche (?P<w2>\d+)\s+', content, re.DOTALL)
    assert res, 'Weeks could not be extracted'
    week1 = res['w1']
    week2 = res['w2']

    res = re.match(r'.*PCR-Tes\s?ts\s+(\d.*\n)?Total\s+\d+\s+\d+\s+(\d+)\s+\d+\.?\d?\s+(\d+)\s', content, re.DOTALL)
    if not res:
        res = re.match(r'.*Labortes\s?ts\s\(PCR\s-\sund\sS\s?chnelltes\s?ts\s?\)\s+(\d.*\n)?Total\s+\d+\s+\d+\.?\d?\s+(\d+)\s+\d+\.?\d?\s+(\d+)\s', content, re.DOTALL)
    if not res:
        res = re.match(r'.*Labortes\s?ts\s\(PCR\s-\sund\sS\s?chnelltes\s?ts\s?\)\s+(\d.*\n)?Total\s+\d+\s+(\d+)\s+\d+\.?\d?\s+(\d+)\s', content, re.DOTALL)
    if res:
        total_tests1 = res[2]
        total_tests2 = res[3]

    if not res:
        res = re.match(r'.*\s+PCR\s+\d+\s+(\d+)\s+(\d+)\s', content, re.DOTALL)
        assert res, f'PCR tests for week {week1} or {week2} could not be extracted!'
        if res:
            total_tests1 = int(res[1])
            total_tests2 = int(res[2])

        res = re.match(r'.*\s+Antigen-Schnelltests\s+\d+\s+(\d+)\s+(\d+)', content, re.DOTALL)
        assert res, f'Antigen tests for week {week1} or {week2} could not be extracted!'
        if res:
            total_tests1 += int(res[1])
            total_tests2 += int(res[2])

    assert res, f'PCR tests for week {week1} or {week2} could not be extracted!'

    #res = re.match(r'.*Positivit.tsrate\s+\*?\s+\d.*%\s+(\d.*)%\s+(\d.*)%', content, re.DOTALL)
    res = re.match(r'.*Positivit.tsrate\s+\*+?\s+\d+\.?\d?%?\s+(\d+\.?\d?)%?\s+(\d+\.?\d?)%?', content, re.DOTALL)
    pos_rate1 = None
    pos_rate2 = None
    if res:
        pos_rate1 = res[1]
        pos_rate2 = res[2]

    data = sc.TestData(canton='SO', url=pdf_url)
    data.week = week1
    data.year = year1
    data.total_tests = total_tests1
    data.positivity_rate = pos_rate1
    print(data)

    data = sc.TestData(canton='SO', url=pdf_url)
    data.week = week2
    data.year = year2
    data.total_tests = total_tests2
    data.positivity_rate = pos_rate2
    print(data)
