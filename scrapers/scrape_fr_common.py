#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def get_fr_csv():
    main_url = 'https://www.fr.ch/de/gesundheit/covid-19/coronavirus-statistik-ueber-die-entwicklung-im-kanton'
    d = sc.download(main_url, silent=True)

    soup = BeautifulSoup(d, 'html.parser')
    item = soup.find('a', title=re.compile(r"Statistik .ber die Entwicklungen im Kanton.*"))
    csv_url = item.get('href')
    assert csv_url, "URL is empty"
    if not csv_url.startswith('http'):
        csv_url = f'https://www.fr.ch{csv_url}'

    csv = sc.download(csv_url, silent=True)
    return csv_url, csv, main_url
