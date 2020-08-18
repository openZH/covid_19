#!/usr/bin/env python3

import scrape_common as sc
import sys
import re


# get latest from list with all press releases
d = sc.download('https://www.regierung.li/coronavirus', silent=True)

pdf_url = sc.find(r'<a.*?href="([^"]+\.pdf)[^"]*"[^>]*?>[^<]+?Situationsbericht[^<]+?<\/a>', d)
if pdf_url:
    # download latest PDF
    d = sc.pdfdownload(pdf_url, raw=True, silent=True)
    # extract case numbers reported for previous days
    d = d.replace(u'\xa0', u' ')

    # data from the most recent press release
    dd = sc.DayData(canton='FL', url=pdf_url)
    dd.datetime = sc.find(r'Situationsbericht vom (.*? 20\d{2})', d)

    dd.cases = sc.find(r'insgesamt\s+([0-9]+)\s+laborbestätigte\s+Fälle', d)
    m = re.search(r'Bisher\s+trat(en)?\s+(\S+)\s+(Todesfall|Todesfälle)', d, flags=re.I)
    if m:
        dd.deaths = sc.int_or_word(m[2])

    if re.search('Alle\s+weiteren\s+Erkrankten\s+sind\s+in\s+der\s+Zwischenzeit\s+genesen', d):
        dd.recovered = int(dd.cases) - int(dd.deaths)

    print(dd)
else:
    print("WARNING: PDF URL not found (Situationsbericht)", file=sys.stderr)

# get the data from PDF file containing full history
history_url = 'https://www.llv.li/files/ag/aktuelle-fallzahlen.pdf'
d = sc.pdfdownload(history_url, layout=True, silent=True)
assert d, f"No content in history PDF found ({history_url})"
data_in_history_found = False
for row in d.splitlines():
    m = re.search(r'^(?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag),\s+(.+\d{4})\s+(\d+)\s+(\d+)\s+(\d+)$', row)
    if m:
        data_in_history_found = True
        dd_full_list = sc.DayData(canton='FL', url=history_url)
        dd_full_list.datetime = m[1]
        dd_full_list.cases = m[2]
        dd_full_list.recovered = m[3]
        dd_full_list.deaths = m[4]
        print('-' * 10)
        print(dd_full_list)

assert data_in_history_found, f"Unable to retrieve data from {history_url}"
