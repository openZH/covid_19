#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def strip_value(value):
    return value.replace('\'', '')


def get_latest_weekly_pdf_url():
    return get_all_weekly_pdf_urls()[0]


def get_all_weekly_pdf_urls():
    base_url = 'https://corona.so.ch'
    url = f'{base_url}/bevoelkerung/daten/woechentlicher-situationsbericht/'
    d = sc.download(url, silent=True)
    soup = BeautifulSoup(d, 'html.parser')
    links = soup.find_all(href=re.compile(r'\.pdf$'))
    result = []
    for link in links:
        file_ref = link.get('href')
        url = f'{base_url}{file_ref}'
        if url not in result:
            result.append(url)
    return result
