#!/usr/bin/env python3

import scrape_common as sc
import requests
from bs4 import BeautifulSoup
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def find_key(row):
    return sc.find(r'<t.\sheight="17".*>([a-zA-Z][^(]+)\(', row).strip()


def find_value(row):
    return sc.find(r'<t.*>([0-9]+)<', row).strip()


def to_statistics(rows):
    return {find_key(str(row.contents)): find_value(str(row.contents)) for row in rows}


print('SG')
d = str(requests.get("https://www.sg.ch/tools/informationen-coronavirus.html", verify=False).content)

sc.timestamp()

soup = BeautifulSoup(d, 'html.parser')
statsBlock = soup.find(string=re.compile(r'Update\s*ganzer\s*Kanton\s*St\.Gallen')).find_parent("div").find_parent(
    "div").find_parent("div")
table = statsBlock.find('table')
assert table, "Table not found"

rows = table.find_all('tr')
statistics = to_statistics(rows)
print('Date and time:', statsBlock.find("h4").text)
print('Confirmed cases:', statistics["laborbest\\xc3\\xa4tigte F\\xc3\\xa4lle"])
print('Hospitalized:', statistics["Hospitalisationen Isolation"])
print('Deaths:', statistics["Verstorbene"])
print('ICU:', statistics["Hospitalisationen Intensiv"])
print('Recovered:', statistics["aus Spital entlassene"])
