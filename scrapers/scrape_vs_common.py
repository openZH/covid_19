#!/usr/bin/env python

import re
import datetime

from bs4 import BeautifulSoup

import scrape_common as sc


def get_vs_latest_weekly_pdf_url():
    pdfs = get_vs_weekly_pdf_urls()
    assert pdfs, "Could not find weekly PDFs"
    return pdfs[0]


def get_vs_weekly_pdf_urls():
    base_url = 'https://www.vs.ch'
    url = base_url + '/de/web/coronavirus/statistiques-hebdomadaires'
    content = sc.download(url, silent=True)
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all(href=re.compile(r'Synthese.*Woche'))
    result = []
    for link in links:
        url = base_url + link['href'].replace(' ', '%20')
        result.append(url)
    return result


def get_vs_weekly_general_data(pdf):
    content = sc.pdftotext(pdf, page=1)
    week = int(sc.find(r'Epidemiologische Situation Woche (\d+)', content))
    end_date = sc.find(r'bis\s+(\d+\.\d+\.\d{4})', content)
    end_date = sc.date_from_text(end_date)
    start_date = end_date - datetime.timedelta(days=7)
    year = start_date.year
    return week, year
