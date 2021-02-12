#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import scrape_common as sc


def get_latest_ge_weekly_pdf_url():
    return get_ge_weekly_pdf_urls()[0]


def get_ge_weekly_pdf_urls():
    d = sc.download('https://www.ge.ch/document/covid-19-bilan-epidemiologique-hebdomadaire', silent=True)
    soup = BeautifulSoup(d, 'html.parser')
    links = soup.find_all('a', title=re.compile(r"\.pdf$"))
    result = []
    for link in links:
        pdf_url = link.get('href')
        assert pdf_url, "pdf URL is empty"
        if not pdf_url.startswith('http'):
            pdf_url = f'https://www.ge.ch{pdf_url}'
        if pdf_url not in result:
            result.append(pdf_url)
    return result


class element_has_link(object):
  def __init__(self, locator):
    self.locator = locator

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if element.get_attribute('href'):
        return element
    else:
        return False


def get_link_from_element(driver, element_id):
    # the xls download links do not appear immediately for some reason
    # add some delay to get it.
    wait = WebDriverWait(driver, 20)
    elem = wait.until(element_has_link((By.ID, element_id)))
    url = elem.get_attribute('href')

    return url
