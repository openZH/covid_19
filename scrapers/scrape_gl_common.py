#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def get_gl_pdf_url():
    d = sc.download('https://www.gl.ch/verwaltung/finanzen-und-gesundheit/gesundheit/coronavirus.html/4817', silent=True)
    soup = BeautifulSoup(d, 'html.parser')

    # weekly pdf
    pdf_url = soup.find(href=re.compile(r'Sentinella.*\.pdf')).get('href')
    return pdf_url
