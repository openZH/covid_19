#!/usr/bin/env python3

# Various small utilities used by scrapers.

import datetime
import os
import subprocess
import re
import requests
import xlrd

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


def download(url, encoding='utf-8'):
    """curl like"""
    print("Downloading:", url)
    downloader = os.path.join(os.path.dirname(__file__), 'download.sh')
    return subprocess.run([downloader, url], capture_output=True, check=True).stdout.decode(encoding)

def xlsdownload(url):
    print("Downloading:", url)
    r = requests.get(url) 
    xls = xlrd.open_workbook(file_contents=r.content)
    return xls

def xldate_as_datetime(sheet, date):
    return xlrd.xldate.xldate_as_datetime(date, sheet.book.datemode)

def pdfdownload(url, encoding='utf-8', raw=False):
    """Download a PDF and convert it to text"""
    print("Downloading:", url)
    downloader = os.path.join(os.path.dirname(__file__), 'download.sh')
    with subprocess.Popen([downloader, url], stdout=subprocess.PIPE) as pdf:
        pdf_command = ['pdftotext', '-', '-']
        if raw:
            pdf_command = ['pdftotext', '-raw', '-', '-']
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
    except ValueError:
        return False


def int_or_word(x):
    if x in spelledOutNumbersMap:
        return spelledOutNumbersMap[x]
    elif represents_int(x):
        return int(x)
    return None
