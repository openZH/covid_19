#!/usr/bin/env python3

import scrape_common as sc
import re


# get latest from list with all press releases
d = sc.download('https://www.regierung.li/coronavirus', silent=True)

pdf_url = sc.find(r'<a.*?href="([^"]+\.pdf[^"]*)".*?>.+Situationsbericht.+<\/a>', d)
assert pdf_url, "PDF URL not found"

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
print(dd)
