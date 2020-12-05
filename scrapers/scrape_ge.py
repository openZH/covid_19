#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import datetime
import sys
from bs4 import BeautifulSoup
import scrape_common as sc
import scrape_ge_common as sgc

is_first = True

# parse tested from PDF
pdf_url = sgc.get_latest_ge_weekly_pdf_url()
pdf = sc.pdfdownload(pdf_url, silent=True)

week_number = sc.find(r'Situation semaine (\d+)', pdf)
week_end_date = datetime.datetime.strptime('2020-W' + week_number + '-7', '%G-W%V-%u').date()
number_of_tests = sc.find(r'Au total, (\d+\'\d+) tests PCR ont', pdf)

if number_of_tests is not None:
    number_of_tests = number_of_tests.replace('\'', '')

    dd_test = sc.DayData(canton='GE', url=pdf_url)
    dd_test.datetime = week_end_date.isoformat()
    dd_test.tested = number_of_tests
    print(dd_test)
    is_first = False


# get hospitalized number
hosp_url = 'https://www.hug.ch/coronavirus-maladie-covid-19/situation-aux-hug'
d = sc.download(hosp_url, silent=True)
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')
content = soup.find(string=re.compile("Comparatif entre le nombre de patients.*")).find_previous('p').text

dd_hosp = sc.DayData(canton='GE', url=hosp_url)
hosp_date = sc.find(r'^Au (\d+\s*(:?\w+)?\s+\w+)\s+à\s+\d+h', content, flags=re.I|re.UNICODE)
dd_hosp.datetime = f'{hosp_date} 2020'
dd_hosp.hospitalized = sc.find(r'(\d+) malades Covid actif', content)
dd_hosp.icu = sc.find(r'(\d+) aux soins intensifs', content)
dd_hosp.icf = sc.find(r'(\d+) aux soins intermédiaires', content)
if dd_hosp:
    if not is_first:
        print('-' * 10)
    is_first = False
    print(dd_hosp)


# isolated / quarantined
iso_url = 'https://infocovid.smc.unige.ch/session/f44a42326896444ff5b80c63d65fca9c/download/download_table_cas?w='
xls = sc.xlsdownload(iso_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
for row in rows:
    dd_iso = sc.DayData(canton='GE', url=iso_url)
    dd_iso.datetime = row['date']
    dd_iso.isolated = row['isolement déjà en cours']
    dd_iso.quarantined = row['Quarantaines en cours suite\nà un contact étroit']
    dd_iso.quarantine_riskareatravel = row['Quarantaines en cours au retour de zone à risque']
    if not is_first:
        print('-' * 10)
    is_first = False
    print(dd_iso)


# xls
d = sc.download('https://www.ge.ch/document/covid-19-donnees-completes-debut-pandemie', silent=True)
soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find(title=re.compile("\.xlsx$")).get('href')
assert xls_url, "xls URL is empty"
if not xls_url.startswith('http'):
    xls_url = f'https://www.ge.ch{xls_url}'

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0, skip_rows=2)
for i, row in enumerate(rows):
    if not isinstance(row['Date'], datetime.datetime):
        print(f"WARNING: {row['Date']} is not a valid date, skipping.", file=sys.stderr)
        continue
    if not is_first:
        print('-' * 10)
    is_first = False
    
    # TODO: remove when source is fixed
    # handle wrong value on 2020-04-09, see issue #819
    if row['Date'].date().isoformat() == '2020-04-09':
        row['Cumul COVID-19 sorties d\'hospitalisation'] = ''

    dd = sc.DayData(canton='GE', url=xls_url)
    dd.datetime = row['Date'].date().isoformat()
    dd.cases = row['Cumul cas COVID-19']
    dd.hospitalized = row['Total hospitalisations COVID-19 actifs (en cours) canton (HUG-cliniques)']
    dd.icu = row['Patients COVID-19 actifs aux soins intensifs HUG']
    dd.icf = row['Patients COVID-19 actifs aux soins intermédiaires HUG']
    dd.deaths = row['Cumul décès COVID-19 ']

    # Since 2020-11-17 GE does no longer publish data about isolated and quarantined
    #dd.isolated = row['Nombre de personnes en isolement ce jour']
    #dd.quarantined = row['Nombre de personnes en quarantaine ce jour ']
    #dd.quarantine_riskareatravel = row['Nombre de personnes en quarantaine ce jour suite à un retour de voyage']

    # Since 2020-07-01 new_hosp is no longer provided
    #dd.new_hosp = row['Nb nouveaux patients COVID-19 hospitalisés']

    ## Since 2020-07-27 vent is no longer provided 
    #dd.vent = row['Patients COVID-19 aux soins intensifs intubés']

    # TODO: check if Nombre tests is added again
    # on 2020-06-09 GE removed the `Nombre tests` column
    #dd.tested = sum(r['Nombre tests'] for r in rows[:i+1])
    if dd:
        print(dd)

