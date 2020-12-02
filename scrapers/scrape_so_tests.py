#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import scrape_common as sc
import scrape_so_common as soc


pdf_urls = soc.get_all_weekly_pdf_urls()
for pdf_url in pdf_urls:
    content = sc.pdfdownload(pdf_url, layout=True, silent=True, page=1)
    # remove ' separator to simplify pattern matching
    content = re.sub(r'(\d)\'(\d)', r'\1\2', content)

    year = sc.find(r'S\s?tand: \d+\.\d+\.(20\d{2})', content)
    res = re.match(r'.*Woche (\d+)\s+Woche (\d+)', content, re.DOTALL)
    assert res, 'Weeks could not be extracted'
    week1 = res[1]
    week2 = res[2]

    res = re.match(r'.*PCR-Tes\s?ts\sTotal\s+\d+\s+\d+\s+(\d+)\s+\d+\.?\d?\s+(\d+)\s', content, re.DOTALL)
    assert res, f'PCR tests for week {week1} or {week2} could not be extracted!'
    total_tests1 = res[1]
    total_tests2 = res[2]

    #res = re.match(r'.*Positivit.tsrate\s+\*?\s+\d.*%\s+(\d.*)%\s+(\d.*)%', content, re.DOTALL)
    res = re.match(r'.*Positivit.tsrate\s+\*+?\s+\d+\.?\d?%\s+(\d+\.?\d?)%\s+(\d+\.?\d?)%', content, re.DOTALL)
    assert res, f'Positivity rate for week {week1} or {week2} could not be extracted!'
    pos_rate1 = res[1]
    pos_rate2 = res[2]

    data = sc.TestData(canton='SO', url=pdf_url)
    data.week = week1
    data.year = year
    data.total_tests = total_tests1
    data.positivity_rate = pos_rate1
    print(data)

    data = sc.TestData(canton='SO', url=pdf_url)
    data.week = week2
    data.year = year
    data.total_tests = total_tests2
    data.positivity_rate = pos_rate2
    print(data)
