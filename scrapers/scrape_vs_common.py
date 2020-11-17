#!/usr/bin/env python

import re

from bs4 import BeautifulSoup

import scrape_common as sc


def get_vs_latest_weekly_pdf_url():
    base_url = 'https://www.vs.ch'
    url = base_url + '/de/web/coronavirus/statistiques'
    content = sc.download(url, silent=True)
    soup = BeautifulSoup(content, 'html.parser')
    link = soup.find(href=re.compile(r'Synthese.*Woche'))
    url = base_url + link['href'].replace(' ', '%20')
    return url


def get_vs_weekly_general_data(pdf):
    content = sc.pdftotext(pdf, page=1)
    week = sc.find(r'Epidemiologische Situation Woche (\d+)', content)
    year = sc.find(r'\d+\.\d+\.(\d{4})', content)
    return week, year
