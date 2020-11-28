#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
import scrape_common as sc
import scrape_sh_common as shc

# last week and current weeks PDFs
urls = [
    'https://sh.ch/CMS/content.jsp?contentid=6840226&language=DE&_=1605991453278',
    'https://sh.ch/CMS/content.jsp?contentid=6894309&language=DE&_=1606572960487',
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

    content = sc.pdftotext(pdf, page=13)
    # remove ' separator to simplify pattern matching
    content = re.sub(r'(\d)\’(\d)', r'\1\2', content)
    td.total_tests = sc.find(r'In\s+der\s+letzten\s+Woche\s+wurden\s+(\d+)\s+(durchgef.hrte\s+)?Tests', content)
    td.positivity_rate = sc.find(r'Die Positivitätsrate[\w+\s+]+\(\d+\.?\d?%\)?[\w+\s+]+\s+(\d+\.?\d?)%', content, flags=re.MULTILINE | re.DOTALL)

    print(td)
