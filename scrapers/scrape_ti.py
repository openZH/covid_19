#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import scrape_common as sc

# get xlsx URL from covid19 page of TI
main_url = 'https://www4.ti.ch/dss/dsp/covid19/home/'
d = sc.download(main_url, silent=True)
soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find(href=re.compile("\.xlsx$")).get('href')
assert xls_url, "URL is empty"

#xls_url = 'https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/dati/COVID19_Dati_TI_per_github.xlsx'
xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0)
is_first = True
for row in rows:
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='TI', url=xls_url)
    dd.datetime = f"{row['date'].date().isoformat()}"
    if row['time']:
        dd.datetime += f"T{row['time'].time().isoformat()}"
    dd.cases = row['ncumul_conf']
    dd.hospitalized = row['current_hosp']
    dd.icu = row['current_icu']
    dd.vent = row['current_vent']
    dd.recovered = row['ncumul_released']
    dd.deaths = row['ncumul_deceased']
    print(dd)
