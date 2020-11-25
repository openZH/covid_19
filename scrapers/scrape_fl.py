#!/usr/bin/env python3

import scrape_common as sc
import sys
import re


# get latest from list with all press releases
d = sc.download('https://www.regierung.li/coronavirus', silent=True)

is_first = True
pdf_url = sc.find(r'<a.*?href="([^"]+\.pdf)[^"]*"[^>]*?>[^<]+?Situationsbericht[^<]+?<\/a>', d)
if pdf_url:
    # download latest PDF
    d = sc.pdfdownload(pdf_url, raw=True, silent=True)
    # extract case numbers reported for previous days
    d = d.replace(u'\xa0', u' ')
    d = d.replace("'", "")
    d = d.replace("’", "")

    # data from the most recent press release
    dd = sc.DayData(canton='FL', url=pdf_url)
    dd.datetime = sc.find(r'Situationsbericht vom (.*? 20\d{2})', d)

    dd.cases = sc.find(r"insgesamt\s+([0-9]+)\s+laborbestätigte\s+Fälle", d)
    m = re.search(r'(?:Bisher|Bislang)\s+trat(en)?\s+(\S+)\s+(Todesfall|Todesfälle)', d, flags=re.I)
    if m:
        dd.deaths = sc.int_or_word(m[2])

    if re.search('Alle\s+weiteren\s+Erkrankten\s+sind\s+in\s+der\s+Zwischenzeit\s+genesen', d):
        dd.recovered = int(dd.cases) - int(dd.deaths)

    m = re.search(r'(\S+)\s+Erkrankte\s+sind\s+derzeit\s+hospitalisiert', d)
    if m:
        dd.hospitalized = sc.int_or_word(m[1].lower())

    m = re.search(r'Gegenwärtig\s+befinden\s+sich\s+(\d+)\s+enge\s+Kontaktpersonen\s+in\s+Quarantäne.', d)
    if m:
        dd.quarantined = m[1]

    if dd:
        print(dd)
        is_first = False
else:
    print("WARNING: PDF URL not found (Situationsbericht)", file=sys.stderr)

# get the data from PDF file containing full history
history_url = 'https://www.llv.li/files/ag/aktuelle-fallzahlen.pdf'
d = sc.pdfdownload(history_url, layout=True, silent=True)
assert d, f"No content in history PDF found ({history_url})"
data_in_history_found = False
rows = d.splitlines()
header = rows[2]
assert re.search(r'^Situationsbericht\s+vom\s+Datenstand\s+Anzahl\s+pos\.\s+Fälle\s+genesen\s+hospitalisiert\s+Todesfälle$', header), f"Header in PDF changed: {header}"
for row in rows:
    row = row.replace("'", "")
    m = re.search(r'^(?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag),\s+(?P<report_date>.+?\d{4})\s+(?P<date>.+?\s+Uhr)\s+(?P<cases>\d+)\s+(?P<recovered>\d+)\s+(?P<hosp>\d+)?\s+(?P<deaths>\d+)$', row)
    if m:
        data_in_history_found = True
        dd_full_list = sc.DayData(canton='FL', url=history_url)
        dd_full_list.datetime = m['report_date']
        dd_full_list.cases = m['cases']
        dd_full_list.recovered = m['recovered']
        dd_full_list.hospitalized = m['hosp']
        dd_full_list.deaths = m['deaths']
        if dd_full_list:
            if not is_first:
                print('-' * 10)
            is_first = False
            print(dd_full_list)

assert data_in_history_found, f"Unable to retrieve data from {history_url}"
