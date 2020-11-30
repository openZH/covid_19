#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def get_weekly_pdf_url():
    base_url = 'https://www.infosan.vd.ch'
    d = sc.download(base_url, silent=True)
    soup = BeautifulSoup(d, 'html.parser')
    html_url = base_url + soup.find(href=re.compile("/publications/covid-19-point-epidemiologique")).get('href')
    d = sc.download(html_url, silent=True)
    soup = BeautifulSoup(d, 'html.parser')
    pdf_url = base_url + soup.find(href=re.compile(r"\.pdf$")).get('href')
    return pdf_url
