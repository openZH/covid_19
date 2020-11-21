#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
import scrape_common as sc
import scrape_sh_common as shc

# last week and current weeks PDFs
urls = [
    'https://sh.ch/CMS/content.jsp?contentid=6782097&language=DE&_=1605991453285',
    'https://sh.ch/CMS/content.jsp?contentid=6840226&language=DE&_=1605991453278',
]
for url in urls:
    pdf_url = shc.get_sh_url_from_json(url)
    pdf = sc.download_content(pdf_url, silent=True)

    td = sc.TestData(canton='SH', url=pdf_url)

    content = sc.pdftotext(pdf, page=1)
    date = sc.find(r'(\d+\..*\d{4})', content)
    date = sc.date_from_text(date)
    # not explicitly stated
    start_date = date - datetime.timedelta(days=7)
    td.start_date = start_date.isoformat()
    td.end_date = date.isoformat()

    content = sc.pdftotext(pdf, page=3)
    # remove ' separator to simplify pattern matching
    content = re.sub(r'(\d)\’(\d)', r'\1\2', content)
    td.total_tests = sc.find(r'(\d+) durchgeführten Tests', content)
    td.positivity_rate = sc.find(r'Positivitätsrate.*\s(\d+\.?\d?)%', content, flags=re.MULTILINE | re.DOTALL)

    print(td)
