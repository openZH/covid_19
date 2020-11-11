#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def strip_value(value):
    return value.replace('\'', '')


def get_latest_weekly_pdf_url():
    base_url = 'https://corona.so.ch'
    url = f'{base_url}/bevoelkerung/daten/woechentlicher-situationsbericht/'
    d = sc.download(url, silent=True)
    soup = BeautifulSoup(d, 'html.parser')
    pdf_url = soup.find(href=re.compile(r'\.pdf$')).get('href')
    pdf_url = f'{base_url}{pdf_url}'
    return pdf_url
