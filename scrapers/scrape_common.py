#!/usr/bin/env python3

# Various small utilities used by scrapers.

import datetime
import os
import subprocess
import re
import requests
import xlrd


class DayData:
    def __init__(self, canton, url):
        self.canton = canton
        self.url = url
        self.timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone().isoformat()
        self.datetime = None
        self.cases = None
        self.hospitalized = None
        self.icu = None
        self.vent = None
        self.deaths = None
        self.recovered = None

    def __str__(self):
        str_rep = [self.canton, self.timestamp, f'Downloading: {self.url}']
        if self.cases is not None:
            str_rep += [f'Confirmed cases: {self.canton}']
        if self.hospitalized is not None:
            str_rep += [f'Hospitalized: {self.hospitalized}']
        if self.icu is not None:
            str_rep += [f'ICU: {self.icu}']
        if self.vent is not None:
            str_rep += [f'Vent: {self.vent}']
        if self.deaths is not None:
            str_rep += [f'Deaths: {self.deaths}']
        if self.recovered is not None:
            str_rep += [f'Recovered: {self.recovered}']
        return "\n".join(str_rep)


spelledOutNumbersMap = {
    'eins': 1,
    'einen': 1,
    'zwei': 2,
    'drei': 3,
    'vier': 4,
    'fünf': 5,
    'f&uuml;nf': 5,
    'sechs': 6,
    'sieben': 7,
    'acht': 8,
    'neun': 9,
    'zehn': 10,
    'elf': 11,
    'zwölf': 12,
    'zw&ouml;lf': 12
}


def download(url, encoding='utf-8', silent=False):
    """curl like"""
    if not silent:
        print("Downloading:", url)
    downloader = os.path.join(os.path.dirname(__file__), 'download.sh')
    return subprocess.run([downloader, url], capture_output=True, check=True).stdout.decode(encoding)

def jsondownload(url, silent=False):
    if not silent:
        print("Downloading:", url)
    r = requests.get(url)
    return r.json()

def xlsdownload(url, silent=False):
    if not silent:
        print("Downloading:", url)
    r = requests.get(url) 
    xls = xlrd.open_workbook(file_contents=r.content)
    return xls

def parse_xls(book, header_row=1, sheet_index=0, sheet_name=None):
    rows = []
    if sheet_name:
        sheet = book.sheet_by_name(sheet_name)
    else:
        sheet = book.sheet_by_index(sheet_index)
    # if a header cell is empty, the name of the column (e.g. "A") is used instead
    headers = {c: sheet.cell_value(header_row, c) or xlrd.formula.colname(c) for c in range(sheet.ncols)} 
    for r in range(header_row + 1, sheet.nrows):
        entry = {}
        for c, h in headers.items():
            cell_type = sheet.cell_type(r, c)
            value = sheet.cell_value(r, c)
            if cell_type == xlrd.XL_CELL_DATE:
                entry[h] = xlrd.xldate.xldate_as_datetime(value, book.datemode)
            elif cell_type == xlrd.XL_CELL_EMPTY:
                entry[h] = None
            elif represents_int(value):
                entry[h] = int(value)
            else:
                entry[h] = value

        rows.append(entry)
    return rows

def pdfdownload(url, encoding='utf-8', raw=False, layout=False, silent=False):
    """Download a PDF and convert it to text"""
    if not silent:
        print("Downloading:", url)
    downloader = os.path.join(os.path.dirname(__file__), 'download.sh')
    with subprocess.Popen([downloader, url], stdout=subprocess.PIPE) as pdf:
        pdf_command = ['pdftotext']
        if raw:
            pdf_command += ['-raw']
        if layout:
            pdf_command += ['-layout']
        pdf_command += ['-', '-']
        with subprocess.Popen(pdf_command, stdin=pdf.stdout, stdout=subprocess.PIPE) as text:
            t = text.stdout.read()
            text.wait()
            return t.decode(encoding)


def filter(pattern, d, flags=re.I):
    """grep like"""
    return "\n".join(l for l in d.split('\n') if re.search(pattern, l, flags=flags))


def find(pattern, d, group=1, flags=re.I):
    """sed like. Ignore character case by default"""
    m = re.search(pattern, d, flags=flags)
    if m:
        return m[group]
    return None


def timestamp():
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone()
    print("Scraped at:", now.isoformat())


def represents_int(s):
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False


def int_or_word(x):
    if x in spelledOutNumbersMap:
        return spelledOutNumbersMap[x]
    elif represents_int(x):
        return int(x)
    return None
