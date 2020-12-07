#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import scrape_common as sc
import scrape_ge_common as sgc


pdf_urls = sgc.get_ge_weekly_pdf_urls()
for pdf_url in pdf_urls:
    pdf = sc.download_content(pdf_url, silent=True)

    content = sc.pdftotext(pdf, page=1)
    week_number = sc.find(r'Situation semaine (\d+)', content)
    year = sc.find(r'au \d+(\w+)? \w+ (\d{4})', content, group=2)

    # data is on page 6 from W48 2020
    for page in [4, 6]:
        content = sc.pdftotext(pdf, page=page)
        # remove ' separator to simplify pattern matching
        content = re.sub(r'(\d)\'(\d)', r'\1\2', content)

        weekly_tests = sc.find(r'avec\s(\d+)\stests\s(effectués\s?)?(contre|\.)', content)
        res = re.match(r'.*taux\sde\spositivité.*\s\(?(\d+\.?\d?)%\)?\s(en|durant).*\d+\.?\d?%', content, re.MULTILINE | re.DOTALL)
        positivity_rate = None
        if res:
            positivity_rate = res[1]

        if weekly_tests and positivity_rate:
            td = sc.TestData(canton='GE', url=pdf_url)
            td.week = week_number
            td.year = year
            td.total_tests = weekly_tests
            td.positivity_rate = positivity_rate
            print(td)
