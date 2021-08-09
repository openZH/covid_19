#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import scrape_common as sc


def load_with_selenium(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "columnHeaders")))
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'date-slicer-input')]")))
    
    # select the complete date range by setting 2020-02-24 as start date
    begin = driver.find_element(By.XPATH, "//input[contains(@class, 'date-slicer-input')]")
    begin.click()
    begin.send_keys(Keys.CONTROL + "a")
    begin.send_keys(Keys.DELETE)
    begin.clear()
    begin.send_keys("2/24/2020") # 2020-02-24 is the date of the earliest data from JU
    begin.send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, "//div[contains(@class, 'slicer-header')]").click()
    time.sleep(5)
    return driver

def scrape_page_part(html):
    table = BeautifulSoup(html, 'html.parser')

    headers = [" ".join(cell.stripped_strings) for cell in table.find(class_='columnHeaders').find_all('div', class_='pivotTableCellWrap')]
    assert len(headers) == 6, f"Number of headers changed: {len(headers)} != 6"
    assert headers[0] == 'Date', f"Header changed to {headers[0]}"
    assert headers[1] == 'Nouveaux cas', f"Header changed to {headers[1]}"
    assert headers[2] == 'Cumul des cas confirmés', f"Header changed to {headers[2]}"
    assert headers[3] == 'Cas actuellement hospitalisés', f"Header changed to {headers[3]}"
    assert headers[4] == 'Cas actuellement en soins intensifs', f"Header changed to {headers[4]}"
    assert headers[5] == 'Nouveaux décès', f"Header changed to {headers[5]}"
    
    columns = table.find(class_='bodyCells').find('div', recursive=False).find('div', recursive=False).findChildren('div', recursive=False)
    assert len(columns) == 6, f"Number of columns changed: {len(columns)} != 6"

    cols = {}
    for i, col in enumerate(columns):
        values = []
        for cell in col.find_all('div'):
            values.append(" ".join(cell.stripped_strings).strip())
        cols[headers[i]] = values

    rows = pd.DataFrame.from_dict(cols).to_dict('records')
    return rows


url = 'https://www.jura.ch/fr/Autorites/Coronavirus/Infos-Actualite/Statistiques-COVID/Evolution-des-cas-COVID-19-dans-le-Jura.html'
d = sc.download(url, silent=True)
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')

is_first = True
iframe = soup.find(string=re.compile(r'Evolution du nombre de cas.*Jura')).find_next('iframe')
if iframe and iframe['src']:
    rows = []
    last_rows = {}
    
    # scroll through Power BI table
    # each time the table is scrolled, a new slice of data is loaded in the table
    i = 0
    while True:
        try:
            driver = load_with_selenium(iframe['src'])
            scroll = driver.find_elements(By.XPATH, "//div[contains(@class, 'scroll-bar-part-bar')]")[1]
            action = ActionChains(driver)
            action.drag_and_drop_by_offset(scroll, 0, i * 20).perform()

            current_rows = scrape_page_part(driver.page_source)
            driver.quit()
            # if we don't get new data after scrolling, we are at the end
            if current_rows == last_rows:
                break
            rows.extend(current_rows)
            last_rows = current_rows
            time.sleep(2)
        except Exception as e:
            print("Error: %s" % e, file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            break
        i += 1

    if rows:
        for i, row in enumerate(rows):
            if not is_first:
                print('-' * 10)
            is_first = False

            dd = sc.DayData(canton='JU', url=url)
            dd.datetime = row.get('Date', '')
            dd.cases = row.get('Cumul des cas confirmés')
            dd.hospitalized = row.get('Cas actuellement hospitalisés')
            dd.icu = row.get('Cas actuellement en soins intensifs')
            dd.deaths = 0
            for r in rows[i:]:
                dd.deaths += int(r.get('Nouveaux décès'))
            print(dd)
