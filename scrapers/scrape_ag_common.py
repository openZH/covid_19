#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import scrape_common as sc


def get_ag_xls_url():
    data_url = 'https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp'
    d = sc.download(data_url, silent=True)
    soup = BeautifulSoup(d, 'html.parser')
    xls_url = soup.find('a', href=re.compile(r'\.xlsx$'))['href']
    if not xls_url.startswith('http'):
        xls_url = f'https://www.ag.ch{xls_url}'
    return xls_url
