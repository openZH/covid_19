#!/usr/bin/env python3

import csv
import re
from io import StringIO
from bs4 import BeautifulSoup
import scrape_common as sc

url = "https://www.zh.ch/de/gesundheit/coronavirus.html#-1310230111"

# get quarantined and isolated from website
dd_iso_q = sc.DayData(canton='ZH', url=url)
d = sc.download(url, silent=True)

# 2020-07-08
"""
<div class="mdl-richtext ">
<h2 class="atm-heading" id="-1310230111" tabindex="-1">Gesundheitliche Lage</h2>
<p class="atm-paragraph">Personen mit Wohnsitz im Kanton Zürich<br> </p>
<h4 class="atm-heading" id="-718243468">23</h4>
<p class="atm-paragraph">neue positive Fälle in den letzten 24 Stunden</p>
<h4 class="atm-heading" id="-718243501">11</h4>
<p class="atm-paragraph">in Spitalbehandlung</p>
<h4 class="atm-heading" id="808114848">3</h4>
<p class="atm-paragraph">davon mit künstlicher Beatmung</p>
<h4 class="atm-heading" id="-790711940">131</h4>
<p class="atm-paragraph">Total Verstorbene seit Pandemiebeginn (78 in Alters- und Pflegeheimen, 51 im Spital, 2 Zuhause)</p>
<h4 class="atm-heading" id="-790711785">181</h4>
<p class="atm-paragraph">in Isolation</p>
<h4 class="atm-heading" id="-790704311">914</h4>
<p class="atm-paragraph">in Quarantäne &nbsp;</p>
<h4 class="atm-heading" id="1798737408">16'362</h4>
<p class="atm-paragraph">liessen sich vom 29. Juni bis 5. Juli 2020 testen, davon waren 196 positiv</p>
<p class="atm-paragraph">Diese Zahlen wurden publiziert am 8. Juli 2020 um 14:30 Uhr. Die Zahlen zu Isolation und Quarantäne werden jeweils dienstags und donnerstags aktualisiert.</p>
</div>
"""

soup = BeautifulSoup(d, 'html.parser')
date_time_info = sc.find('publiziert am (.+Uhr)', d)
dd_iso_q.datetime = date_time_info
dd_iso_q.isolated = soup.find(string=re.compile(r'in Isolation')).find_previous('h4').text
dd_iso_q.quarantined = soup.find(string=re.compile(r'in Quarantäne')).find_previous('h4').text

print(dd_iso_q)

csv_url = 'https://raw.githubusercontent.com/openzh/covid_19/master/fallzahlen_kanton_zh/COVID19_Fallzahlen_Kanton_ZH_total.csv'
d_csv = sc.download(csv_url, silent=True)
reader = csv.DictReader(StringIO(d_csv), delimiter=',')

for row in reader:
    print('-' * 10)
    dd = sc.DayData(canton='ZH', url=url)
    dd.datetime = f"{row['date']} {row['time']}"
    dd.cases = row['ncumul_conf']
    dd.deaths = row['ncumul_deceased']
    dd.hospitalized = row['current_hosp']
    dd.vent = row['current_vent']
    print(dd)
    



