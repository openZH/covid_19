#!/usr/bin/env python3

# Various small utilities used by scrapers.

import datetime
import os
import subprocess
import re
import requests
import xlrd
from scrape_dates import parse_date


class DayData(object):
    __isfrozen = False
    def __init__(self, canton, url):
        self.canton = canton
        self.url = url
        self.timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone().isoformat()
        self.datetime = None
        self.tested = None
        self.cases = None
        self.hospitalized = None
        self.new_hosp = None
        self.icu = None
        self.vent = None
        self.deaths = None
        self.recovered = None
        self.isolated = None
        self.quarantined = None
        # canton-specific fields
        self.icf = None
        self.confirmed_non_resident = None
        self.hosp_non_resident = None

        # freeze class, so that no new attributes can be created
        self.__isfrozen = True

    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError( "%r is a frozen class" % self )
        object.__setattr__(self, key, value)

    def __str__(self):
        str_rep = [
            self.canton,
            f'Scraped at: {self.timestamp}',
            f'Downloading: {self.url}'
        ]
        if self.datetime is not None and self.datetime != '':
            str_rep += [f'Date and time: {self.datetime}']
        if self.tested is not None and self.tested != '':
            str_rep += [f'Tested: {self.tested}']
        if self.cases is not None and self.cases != '':
            str_rep += [f'Confirmed cases: {self.cases}']
        if self.hospitalized is not None and self.hospitalized != '':
            str_rep += [f'Hospitalized: {self.hospitalized}']
        if self.new_hosp is not None and self.new_hosp != '':
            str_rep += [f'New Hospitalized: {self.new_hosp}']
        if self.icu is not None and self.icu != '':
            str_rep += [f'ICU: {self.icu}']
        if self.vent is not None and self.vent != '':
            str_rep += [f'Vent: {self.vent}']
        if self.deaths is not None and self.deaths != '':
            str_rep += [f'Deaths: {self.deaths}']
        if self.recovered is not None and self.recovered != '':
            str_rep += [f'Recovered: {self.recovered}']
        if self.isolated is not None and self.isolated != '':
            str_rep += [f'Isolated: {self.isolated}']
        if self.quarantined is not None and self.quarantined != '':
            str_rep += [f'Quarantined: {self.quarantined}']
        if self.icf is not None and self.icf != '':
            str_rep += [f'ICF: {self.icf}']
        if self.confirmed_non_resident is not None and self.confirmed_non_resident != '':
            str_rep += [f'Confirmed non-resident: {self.confirmed_non_resident}']
        if self.hosp_non_resident is not None and self.hosp_non_resident != '':
            str_rep += [f'Hospitalized non-resident: {self.hosp_non_resident}']
        return "\n".join(str_rep)


spelledOutNumbersMap = {
    'eins': 1,
    'einen': 1,
    'einem': 1,
    'ein': 1,
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

def parse_xls(book, header_row=1, sheet_index=0, sheet_name=None, skip_rows=1):
    rows = []
    if sheet_name:
        sheet = book.sheet_by_name(sheet_name)
    else:
        sheet = book.sheet_by_index(sheet_index)
    # if a header cell is empty, the name of the column (e.g. "A") is used instead
    headers = {c: sheet.cell_value(header_row, c) or xlrd.formula.colname(c) for c in range(sheet.ncols)} 
    for r in range(header_row + skip_rows, sheet.nrows):
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

def safeint(s):
    if not s:
        return s
    f = float(s)
    r = round(f)
    if f == r:
        return int(f)
    else:
        raise ValueError(f"Can't parse {s} as int without losing precision")

def int_or_word(x):
    if x in spelledOutNumbersMap:
        return spelledOutNumbersMap[x]
    elif represents_int(x):
        return int(x)
    return None


def date_from_text(date_str):
    new_date = parse_date(date_str)
    day = new_date.split("T", 1)[0].split('-', 2)
    day = datetime.date(int(day[0]), int(day[1]), int(day[2]))
    return day
