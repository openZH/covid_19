#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import datetime
import scrape_common as sc
from scrape_dates import parse_date
import cv2
import pytesseract
import numpy as np
import tempfile
import os


districts = {
    'Baden': {
        'pattern': r'^Baden.*',
        'district_id': '1902',
        'population': 145696,
    },
    'Muri': {
        'pattern': r'^Muri.*',
        'district_id': '1908',
        'population': 37170,
    },
    'Lenzburg': {
        'pattern': r'^Lenzburg.*',
        'district_id': '1907',
        'population': 64792,
    },
    'Zofingen': {
        'pattern': r'^Zo.+ngen.*',
        'district_id': '1910',
        'population': 73136,
    },
    'Aarau': {
        'pattern': r'^Aarau.*',
        'district_id': '1901',
        'population': 79702,
    },
    'Bremgarten': {
        'pattern': r'^Bremga.+en.*',
        'district_id': '1903',
        'population': 78745,
    },
    'Brugg': {
        'pattern': r'^Brugg.*',
        'district_id': '1904',
        'population': 51814,
    },
    'Kulm': {
        'pattern': r'^Kulm.*',
        'district_id': '1905',
        'population': 42412,
    },
    'Laufenburg': {
        'pattern': r'^Laufen.*burg.*',
        'district_id': '1906',
        'population': 33035,
    },
    'Rheinfelden': {
        'pattern': r'^Rheinfelden.*',
        'district_id': '1909',
        'population': 47926,
    },
    'Zurzach': {
        'pattern': r'^Z.+zach.*',
        'district_id': '1911',
        'population': 34650,
    },
}

data_url = 'https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp'
d = sc.download(data_url, silent=True)
soup = BeautifulSoup(d, 'html.parser')
img_caption = soup.find(string=re.compile(r".*Inzidenz pro 100'000 Einwohner nach Bezirke.*"))
img_date = sc.find(r'\(Stand:?\s+(.*\d{4})', img_caption.string)
img_date = datetime.datetime.fromisoformat(parse_date(img_date).split('T', 1)[0])
img_url = img_caption.find_previous('img')['src']
img_url = 'https://www.ag.ch/media/kanton_aargau/themen_1/coronavirus_1/bilder_11/daten/Inzidenz_pro_100K_Einwohner_content_large.jpg'
if not img_url.startswith('http'):
    img_url = f'https://www.ag.ch{img_url}'

# download the image to a temporary file
_, path = tempfile.mkstemp(suffix='.jpg')
sc.download_file(img_url, path)

# convert to binary image
img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray, img_bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
gray = cv2.bitwise_not(img_bin)

# improve image and extract text
kernel = np.ones((2, 1), np.uint8)
img = cv2.erode(gray, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
#cv2.imshow('img', img)
#cv2.waitKey(0)
custom_config = '--oem 3 --psm 6'
text_in_img = pytesseract.image_to_string(img, config=custom_config)

# delete the temp img file
os.remove(path)

def parse_line(line):
    in_str = "OBFT"
    out_str = "0877"
    tab = str.maketrans(in_str, out_str)
    match = re.match(r'^(.*)\s+(?:[_-]\s+)?(\S+)\s+(\S+)\s+(\S+)$', line)
    if match:
        return (int(match[3].replace("'", "").translate(tab)), int(match[4].replace("'", "").translate(tab)))
    return (None, None)

for name, config in districts.items():
    for line in text_in_img.split('\n'):
        dd = sc.DistrictData(canton='AG', district=name)
        dd.district_id = config['district_id']
        dd.url = data_url
        if re.search(config['pattern'], line, flags=re.I):
            population, total_cases = parse_line(line)
            assert population == config['population'], f"Population number for {name} does not match, {population} != {config['population']}"
            dd.date = img_date.date().isoformat()
            dd.population = population
            dd.total_cases = total_cases
            break
    assert dd, f"No data found for district {name}, Text: {text_in_img}"
    print(dd)
