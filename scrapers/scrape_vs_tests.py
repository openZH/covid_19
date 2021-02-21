#!/usr/bin/env python

import re

import scrape_common as sc
import scrape_vs_common as svc


# get all PDFs
for url in svc.get_vs_weekly_pdf_urls():
    td = sc.TestData(canton='VS', url=url)

    pdf = sc.download_content(url, silent=True)
    td.week, td.year = svc.get_vs_weekly_general_data(pdf)

    for page in range(4, 5):
        content = sc.pdftotext(pdf, page=page, raw=True)
        content = re.sub(r'(\d)\‘(\d)', r'\1\2', content)
        content = re.sub(r'(\d)\’(\d)', r'\1\2', content)

        td.total_tests = sc.find(r'Alle\s+Arten\s+von\s+Tests\s+(\d+)', content)
        td.positivity_rate = sc.find(r'Alle\s+Arten\s+von\s+Tests\s+\d+\s+(\d+\.\d+)%', content)
        td.pcr_total_tests = sc.find(r'PCR\s+(\d+)', content)
        td.pcr_positivity_rate = sc.find(r'PCR\s+\d+\s+(\d+\.\d+)%', content)
        td.ag_total_tests = sc.find(r'Antigentests\s+(\d+)', content)
        td.ag_positivity_rate = sc.find(r'Antigentests\s+\d+\s+(\d+\.\d+)%', content)

        if not td.total_tests:
            continue

        print(td)
