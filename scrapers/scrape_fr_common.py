#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def get_fr_xls():
    main_url = 'https://www.fr.ch/de/gesundheit/covid-19/coronavirus-statistik-ueber-die-entwicklung-im-kanton'
    d = sc.download(main_url, silent=True)

    soup = BeautifulSoup(d, 'html.parser')
    item = soup.find('span', text=re.compile(r"Statistik .ber die Entwicklungen im Kanton.*"))
    item = item.find_parent('a')
    xls_url = item.get('href')
    assert xls_url, "URL is empty"
    if not xls_url.startswith('http'):
        xls_url = f'https://www.fr.ch{xls_url}'

    xls = sc.xlsdownload(xls_url, silent=True)
    return xls_url, xls, main_url
