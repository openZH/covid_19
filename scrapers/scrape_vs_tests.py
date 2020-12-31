#!/usr/bin/env python

import re

import scrape_common as sc
import scrape_vs_common as svc


# get all PDFs
for url in svc.get_vs_weekly_pdf_urls():
    td = sc.TestData(canton='VS', url=url)

    pdf = sc.download_content(url, silent=True)
    td.week, td.year = svc.get_vs_weekly_general_data(pdf)

    content = sc.pdftotext(pdf, page=2, raw=True)
    content = re.sub(r'(\d)\‘(\d)', r'\1\2', content)

    td.total_tests = sc.find(r'Anzahl durchgef.hrter Tests.*[\s|\(](\d+)[\s|\.]', content)
    td.positivity_rate = sc.find(r'Die\s+Positivitätsrate.*\n?.*\s(\d+\.?\d?)%\s.*gegen.ber\s\d+\.?\d?%', content)
    if not td.positivity_rate:
        td.positivity_rate = sc.find(r'Die\s+Positivitätsrate.*\n?.*\s(\d+\.?\d?)%', content)

    # ignore PDFs not providing total count
    if not td.total_tests:
        continue

    print(td)
