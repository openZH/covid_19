#!/usr/bin/env python3

import scrape_common as sc
import sys
import re


# download latest PDF
pdf_url = 'https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/covid-19-woechentlicher-lagebericht.pdf.download.pdf/BAG_COVID-19_Woechentliche_Lage.pdf'
d = sc.pdfdownload(pdf_url, raw=True, silent=True)

"""
Coronavirus-Krankheit-2019 (COVID-19)
Eidgen<C3><B6>ssisches Departement des Innern EDI
Bundesamt f<C3><BC>r Gesundheit BAG
Direktionsbereich <C3><96>ffentliche Gesundheit
Situationsbericht zur epidemiologischen Lage in der Schweiz
und im F<C3><BC>rstentum Liechtenstein - Woche 28 (06.-12.07.2020)
"""

datetime = sc.find(r'Liechtenstein - Woche .*(\d{2}\.\d{2}\.\d{4})\)', d)

"""
Canton, tests of previous-week then current-week

AG 5478 3588 808 529 1.3 1.8
AI 96 55 595 341 0.0 0.0
AR 391 249 708 451 0.5 1.2
BE 6924 4652 669 449 0.4 0.9
...
"""
start = d.find('Anzahl PCR-Tests in der Schweiz')
if start > 0:
    start = d.find('\nAG ', start)
else:
    start = 0
end = d.find('Tabelle 4. Durchgeführte Tests nach Kalenderwoche', start)
if start > 0 and end > start:
    tests_table = d[start:end]
    for line in tests_table.splitlines():
        canton = sc.find(r'^([A-Z][A-Z]) ', line)
        if canton is not None:
            dd = sc.DayData(canton=canton, url=pdf_url)
            dd.datetime = datetime
            dd.tested = sc.find(r'^[A-Z][A-Z] \d+ (\d+)', line)
            print('-' * 10)
            print(dd)

