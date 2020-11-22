#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import scrape_common as sc


def get_latest_bl_bulletin_url():
    news_url = 'https://www.baselland.ch/politik-und-behorden/direktionen/volkswirtschafts-und-gesundheitsdirektion/amt-fur-gesundheit/medizinische-dienste/kantonsarztlicher-dienst/aktuelles/medienmitteilungen-1'
    news_content = sc.download(news_url, silent=True)
    soup = BeautifulSoup(news_content, 'html.parser')

    bulletin_url = soup.find('td', string=re.compile(r'Coronavirus: Wochenbulletin.*')).find_previous('a').get('href')
    return bulletin_url
