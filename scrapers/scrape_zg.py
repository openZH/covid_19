#!/usr/bin/env python3

import re
from io import StringIO
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
import scrape_common as sc

print('ZG')
d = sc.download('https://www.zg.ch/behoerden/gesundheitsdirektion/amt-fuer-gesundheit/corona')
sc.timestamp()
soup = BeautifulSoup(d, 'html.parser')
d = sc.filter(r'Infizierte Personen|Genesene Personen|Verstorbene Personen|Stand:', d)
print('Date and time:', sc.find(r'Stand:? ([^<]+ Uhr)<', d))

detailed_stats = soup.find("a", text=re.compile("Detaillierte Statistik"))
if detailed_stats:
    d_detailed_stats = sc.download(detailed_stats['href'])
    d_detailed_stats_comps = urlparse(detailed_stats['href'])
    csv_path = sc.find(r'csv_path:"([^"]+)"', d_detailed_stats)
    csv_url = f"{d_detailed_stats_comps.scheme}://{d_detailed_stats_comps.netloc}{csv_path}"
    d_csv = sc.download(csv_url)
    """
"Typ","Datum","Anzahl","Meta","Type","Content"
"Fallzahl","01.03.2020","0",NA,NA,NA
"Fallzahl","02.03.2020","0",NA,NA,NA
"Fallzahl","03.03.2020","1",NA,NA,NA
"Fallzahl","04.03.2020","1",NA,NA,NA
"Fallzahl","05.03.2020","2",NA,NA,NA
"Fallzahl","06.03.2020","3",NA,NA,NA
"Fallzahl","07.03.2020","3",NA,NA,NA
"""
    df = pd.read_csv(StringIO(d_csv), sep=",", parse_dates=['Datum'], dayfirst=True)
    df_cases = df[df['Typ'] == 'Fallzahl'].sort_values(by='Datum', ascending=False)
    print('Confirmed cases:', int(df_cases.iloc[0]['Anzahl']))
    df_hospitalized = df[df['Typ'] == 'Hospitalisierte'].sort_values(by='Datum', ascending=False)
    print('Hospitalized:', int(df_hospitalized.iloc[0]['Anzahl']))
    df_icu = df[df['Typ'] == 'Hospitalisierte in Intensivpflege'].sort_values(by='Datum', ascending=False)
    print('ICU:', int(df_icu.iloc[0]['Anzahl']))
    df_recovered = df[df['Typ'] == 'Genesene'].sort_values(by='Datum', ascending=False)
    print('Recovered:', int(df_recovered.iloc[0]['Anzahl']))
    df_deaths = df[df['Typ'] == 'Todesfälle'].sort_values(by='Datum', ascending=False)
    print('Deaths:', int(df_deaths.iloc[0]['Anzahl']))

else:
    # 2020-03-23
    """
      <p>Infizierte Personen: 62</p>
<p>Genesene Personen: 10</p>
<p>Verstorbene Personen: 0</p>
<p>Stand: 23.3.2020, 8.00 Uhr</p>
"""
    print('Confirmed cases:', sc.find(r'Infizierte Personen:? ([0-9]+)<', d))
    print('Deaths:', sc.find(r'Verstorbene Personen:? ([0-9]+)<', d))
    print('Recovered:', sc.find(r'Genesene Personen:? ([0-9]+)<', d))
