#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def get_nw_page():
    url = 'https://www.nw.ch/gesundheitsamtdienste/6044'
    content = sc.download(url, silent=True)
    content = content.replace("&nbsp;", " ")
    content = re.sub(r'(\d+)\'(\d+)', r'\1\2', content)
    soup = BeautifulSoup(content, 'html.parser')
    return url, soup
