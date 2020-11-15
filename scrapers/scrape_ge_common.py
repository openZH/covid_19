#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def get_latest_ge_weekly_pdf_url():
    return get_ge_weekly_pdf_urls()[0]


def get_ge_weekly_pdf_urls():
    d = sc.download('https://www.ge.ch/document/covid-19-bilan-epidemiologique-hebdomadaire', silent=True)
    soup = BeautifulSoup(d, 'html.parser')
    links = soup.find_all('a', title=re.compile(r"\.pdf$"))
    result = []
    for link in links:
        pdf_url = link.get('href')
        assert pdf_url, "pdf URL is empty"
        if not pdf_url.startswith('http'):
            pdf_url = f'https://www.ge.ch{pdf_url}'
        if pdf_url not in result:
            result.append(pdf_url)
    return result
