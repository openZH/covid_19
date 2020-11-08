#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def get_fr_xls():
    d = sc.download('https://www.fr.ch/sante/covid-19/coronavirus-statistiques-evolution-de-la-situation-dans-le-canton', silent=True)

    soup = BeautifulSoup(d, 'html.parser')
    xls_url = soup.find(href=re.compile("\.xlsx$")).get('href')
    assert xls_url, "URL is empty"
    if not xls_url.startswith('http'):
        xls_url = f'https://www.fr.ch{xls_url}'

    xls = sc.xlsdownload(xls_url, silent=True)
    return xls_url, xls
