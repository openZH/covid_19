#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def get_latest_ge_weekly_pdf_url():
    d = sc.download('https://www.ge.ch/document/covid-19-bilan-epidemiologique-hebdomadaire', silent=True)
    soup = BeautifulSoup(d, 'html.parser')
    pdf_url = soup.find(title=re.compile("\.pdf$")).get('href')
    assert pdf_url, "pdf URL is empty"
    if not pdf_url.startswith('http'):
        pdf_url = f'https://www.ge.ch{pdf_url}'
    return pdf_url
