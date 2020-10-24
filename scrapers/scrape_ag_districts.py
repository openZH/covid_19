#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import datetime
import scrape_common as sc
import cv2
import pytesseract
import numpy as np
import io


img_url = 'https://www.ag.ch/media/kanton_aargau/themen_1/coronavirus_1/bilder_11/daten/Inzidenz_pro_100K_Einwohner.jpg'
sc.download_file(img_url, 'img.jpg')

img = cv2.imread('img.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
gray = cv2.bitwise_not(img_bin)

kernel = np.ones((2, 1), np.uint8)
img = cv2.erode(gray, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
text_in_img = pytesseract.image_to_string(img)

for line in text_in_img.split('\n'):
    print(line)

# district_ids = {
#     'Baden':
#     'Muri':
#     'Lenzburg':
#     'Zofingen':
#     'Aarau':
#     'Bremgarten':
#     'Brugg':
#     'Kulm':
#     'Laufenburg':
#     'Rheinfelden':
#     'Zurzach':
# }
# 
# for row in rows:
#     dd = sc.DistrictData(canton='AG', district=district)
#     dd.district_id = district_id
#     dd.population = population[district]
#     dd.url = main_url
#     dd.date = row['date']
#     dd.total_cases = row[district] + initial_cases[district]
#     dd.new_cases = dd.total_cases - last_total_cases_val
#     last_total_cases_val = dd.total_cases
#     print(dd)
