#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc
import scrape_gl_common as sgc

pdf_url = sgc.get_gl_pdf_url()
if pdf_url is not None:
    pdf = sc.download_content(pdf_url, silent=True)
    content = sc.pdftotext(pdf, page=1, layout=True)
    # remove 1k separators
    content = re.sub(r'(\d)\'(\d)', r'\1\2', content)

    year = sc.find(r'Stand: \d{2}\.\d{2}.(\d{4})', content)
    week = sc.find(r'KW(\d+)\.pdf', pdf_url)

    # Insgesamt Anzahl, 100k, 14 Tage Anzahl, 100k, 7 Tage Anzahl, 100k
    number_of_tests = sc.find(r'PCR-Tests/Schnelltests\sKanton Glarus\s+\d+\s+\d+\.?\d+?\s+\d+\s+\d+\.?\d+?\s+(\d+)\s+\d+', content)
    # Insgesamt, 14 Tage, 7 Tage
    positivity_rate = sc.find(r'Positivit.tsrate GL\s?\*+?\s+\d+\.\d%\s+\d+\.\d%\s+(\d+\.\d)%\s+', content)

    td = sc.TestData(canton='GL', url=pdf_url)
    td.week = week
    td.year = year
    td.total_tests = number_of_tests
    td.positivity_rate = positivity_rate
    print(td)
