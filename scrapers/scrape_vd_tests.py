#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import scrape_common as sc
import scrape_vd_common as svc


pdf_urls = svc.get_all_weekly_pdf_urls()
for pdf_url in pdf_urls:
    pdf = sc.pdfdownload(pdf_url, silent=True, page=1)
    pdf = re.sub(r'(\d+)\'(\d+)', r'\1\2', pdf)
    pdf = re.sub(r'(\d+)’(\d+)', r'\1\2', pdf)

    td = sc.TestData(canton='VD', url=pdf_url)

    year = sc.find(r'Situation au \d+.*(20\d{2})', pdf)
    res = re.search(r'Entre\s+le\s+(?P<start>\d+\s+\w+)s+et\s+le\s+(?P<end>\d+\s+\w+),', pdf, flags=re.I|re.UNICODE) 
    res_with_year = re.search(r'Entre\s+le\s+(?P<start>\d+\s+\w+\s+\d{4})\s+et\s+le\s+(?P<end>\d+\s+\w+\s+\d{4}),', pdf, flags=re.I|re.UNICODE)
    res_no_month = re.search(r'Entre\s+le\s+(?P<start>\d+)\s+et\s+le\s+(?P<end>\d+\s+\w+),', pdf, flags=re.I|re.UNICODE)

    if res:
        start_date = sc.date_from_text(f"{res['start']} {year}")
        end_date = sc.date_from_text(f"{res['end']} {year}")
    elif res_with_year:
        start_date = sc.date_from_text(res_with_year['start'])
        end_date = sc.date_from_text(res_with_year['end'])
    elif res_no_month:
        end_date = sc.date_from_text(f"{res_no_month['end']} {year}")
        start_date = sc.date_from_text(f"{res_no_month['start']}.{end_date.month}.{year}")
    assert start_date and end_date, f'failed to extract start and end dates from {pdf_url}'
    td.start_date = start_date
    td.end_date = end_date

    res = re.search(r'une\s+moyenne\s+de\s+(\d+)\s+frottis\s+SARS-CoV(-)?2', pdf)
    if res:
        days = (end_date - start_date).days
        td.total_tests = days * int(res[1])

    res = re.search(r'dont\s+(\d+\.?\d?)%\s+étaient\s+positifs', pdf)
    if res:
        td.positivity_rate = res[1]

    if td:
        print(td)
