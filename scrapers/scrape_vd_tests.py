#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import scrape_common as sc
import scrape_vd_common as svc


pdf_url = svc.get_weekly_pdf_url()
pdf = sc.pdfdownload(pdf_url, silent=True, page=1)
pdf = re.sub(r'(\d+)\'(\d+)', r'\1\2', pdf)

td = sc.TestData(canton='VD', url=pdf_url)

year = sc.find(r'Situation au \d+.*(20\d{2})', pdf)
res = re.search(r'Entre\s+le\s+(\d+\s+\w+)\s+et\s+le\s+(\d+\s+\w+),', pdf)
assert res, 'failed to extract start and end dates'
td.start_date = sc.date_from_text(f'{res[1]} {year}').isoformat()
td.end_date = sc.date_from_text(f'{res[2]} {year}').isoformat()

res = re.search(r'une\s+moyenne\s+de\s+(\d+)\s+frottis\s+SARS-CoV-2', pdf)
assert res, 'failed to extract total number of tests'
td.total_tests = 7 * int(res[1])

res = re.search(r'dont\s+(\d+\.?\d?)%\s+étaient\s+positifs', pdf)
assert res, 'failed to extract positivity rate'
td.positivity_rate = res[1]

print(td)
