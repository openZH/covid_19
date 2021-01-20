#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import scrape_common as sc
import scrape_vs_common as svc


pdf_urls = svc.get_vs_all_daily_pdf_url()
for pdf_url in pdf_urls:
    content = sc.pdfdownload(pdf_url, silent=True, layout=True, page=1)

    date = sc.find(r'(\d{2}/\d{2}/20\d{2})', content)
    date = sc.date_from_text(date.replace('/', '.'))
    if date.year == 2020:
        # no data available in 2020
        break

    vd = sc.VaccinationData(canton='VS', url=pdf_url)
    vd.start_date = date.isoformat()
    vd.end_date = date.isoformat()
    vd.total_vaccinations = svc.strip_value(sc.find(r'.*Anzahl\s+der\s+verteilten\s+Impfdosen.*\s+(\d+.\d+)\s+', content))
    if vd:
        print(vd)
