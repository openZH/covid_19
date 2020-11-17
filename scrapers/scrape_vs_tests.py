#!/usr/bin/env python

import re

import scrape_common as sc
import scrape_vs_common as svc


# get the latest weekly PDF
url = svc.get_vs_latest_weekly_pdf_url()
td = sc.TestData(canton='VS', url=url)

# fetch the PDF
pdf = sc.download_content(url, silent=True)
td.week, td.year = svc.get_vs_weekly_general_data(pdf)

content = sc.pdftotext(pdf, page=2, raw=True)
content = re.sub(r'(\d)\‘(\d)', r'\1\2', content)

td.total_tests = sc.find(r'Anzahl durchgef.hrter Tests.*[\s|\(](\d+)[\s|\.]', content)
td.positivity_rate = sc.find(r'Die Positivit.tsrate .* (\d+\.?\d?)%', content)

print(td)
