#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def get_fr_xls():
    d = sc.download('https://www.fr.ch/de/gesundheit/covid-19/coronavirus-statistik-ueber-die-entwicklung-im-kanton', silent=True)

    soup = BeautifulSoup(d, 'html.parser')
    xls_url = soup.find(href=re.compile(r"\.xlsx$")).get('href')
    assert xls_url, "URL is empty"
    if not xls_url.startswith('http'):
        xls_url = f'https://www.fr.ch{xls_url}'

    xls = sc.xlsdownload(xls_url, silent=True)
    return xls_url, xls
