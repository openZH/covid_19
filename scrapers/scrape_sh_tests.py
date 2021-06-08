#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
from bs4 import BeautifulSoup
import scrape_common as sc
import scrape_sh_common as shc

# extract content_id of main page
url = 'https://sh.ch/CMS/Webseite/Kanton-Schaffhausen/Beh-rde/Verwaltung/Departement-des-Innern/Gesundheitsamt-3209198-DE.html'
d = sc.download(url, silent=True)
content_id = sc.find(r"var contentid = '(\d+)';", d)
assert content_id

# get main page contents with the content id
url = f'https://sh.ch/CMS/content.jsp?contentid={content_id}&language=DE'
d = sc.jsondownload(url, silent=True)

# and extract the Lagebericht content ids
soup = BeautifulSoup(d['data_post_content'], 'html.parser')
links = soup.find_all('a', text=re.compile(r'Lagebericht'))
content_ids = []
for link in links:
    content_ids.append(link.get('contentid'))

# fetch the PDFs and parse
found_data = False
for content_id in content_ids:
    url = f'https://sh.ch/CMS/content.jsp?contentid={content_id}&language=DE'
    pdf_url = shc.get_sh_url_from_json(url)
    pdf = sc.download_content(pdf_url, silent=True)

    td = sc.TestData(canton='SH', url=pdf_url)

    content = sc.pdftotext(pdf, page=1)
    date = sc.find(r'(\d+\..*\d{4})', content)
    date = sc.date_from_text(date)
    # not explicitly stated
    start_date = date - datetime.timedelta(days=7)
    td.start_date = start_date.isoformat()
    td.end_date = date.isoformat()

    #content = sc.pdftotext(pdf, page=14)
    for page in range(9, 16):
        content = sc.pdftotext(pdf, page=page)
        # remove ' separator to simplify pattern matching
        content = re.sub(r'(\d)\’(\d)', r'\1\2', content)
        td.total_tests = sc.find(r'in\s+der\s+letzten\s+Woche\s+wurden(\s+nur)?\s+(\d+)\s+(durchgef.hrte\s+)?Tests', content, group=2)
        if not td.total_tests:
            td.total_tests = sc.find(r'Es\s+wurden\s+in\s+der\s+letzten\s+Woche\s+(\d+)\s+Tests', content)
        if not td.total_tests:
            td.total_tests = sc.find(r'in\s+der\s+letzten\s+Woche[\s|\w]+\s+(\d+)[\s|\w]+\s+Tests', content)
        if not td.total_tests:
            td.total_tests = sc.find(r'insgesamt\s+(\d+)\s+Tests', content)
        td.positivity_rate = sc.find(r'Die\sPositivitätsrate\sbetrug\s+(\d+\.?\d?)%\s', content)
        if not td.positivity_rate:
            td.positivity_rate = sc.find(r'Die\sPositivitätsrate.*Vorwoche\s\(\d+\.?\d?%\)\s[\w+\s+]+\s(\d+\.?\d?)%\s.*\.', content, flags=re.MULTILINE | re.DOTALL)
        if not td.positivity_rate:
            td.positivity_rate = sc.find(r'Positivitätsrate\s+[\w\s]+\s+(\d+\.?\d?)%[\w\s]+?\(Vorwoche', content)
        if not td.positivity_rate:
            td.positivity_rate = sc.find(r'Positivitätsrate\s+[\w\s\,\d%]+\s+\((\d+\.?\d?)%\s+(gegen.ber|gg.\.)', content)

        td.ag_total_tests = sc.find(r'Der\s+Anteil\s+der\s+Antigen-Schnelltests\s+betrug\s+letzte\s+Woche\s+\d+%\s\((\d+)\s+Tests\)', content)
        if not td.ag_total_tests:
            td.ag_total_tests = sc.find(r'Der\s+Anteil\s+der\s+Antigen-Schnelltests\s+betrug\s+letzte\s+Woche\s+\d+%\s+mit\s+(\d+)\s+Tests', content)

        if td:
            found_data = True
            print(td)

assert found_data, 'Did not find any tests data for SH'
