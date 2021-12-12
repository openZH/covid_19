#!/usr/bin/env python3

import datetime
import re
from bs4 import BeautifulSoup
import scrape_common as sc


is_first = True

url = 'https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/info/Seiten/Start.aspx'
data = sc.download(url, silent=True)
data = re.sub(r'(\d+)&#39;(\d+)', r'\1\2', data)
soup = BeautifulSoup(data, 'html.parser')
elem = soup.find('h2', text=re.compile(r'Fallzahlen\s+Kanton.*'))
if elem is not None:
    table = elem.find_next('table')
    body = table.find('tbody')
    for row in body.find_all('tr'):
        tds = row.find_all('td')

        if not is_first:
            print('-' * 10)
        is_first = False

        dd = sc.DayData(canton='GR', url=url)
        dd.datetime = tds[0].text
        dd.cases = tds[1].text
        dd.isolated = tds[3].text
        dd.quarantined = tds[4].text
        dd.deaths = tds[6].text
        dd.hospitalized = tds[8].text
        dd.icu = tds[10].text
        dd.vent = tds[11].text
        print(dd)


json_url = 'https://services1.arcgis.com/YAuo6vcW85VPu7OE/arcgis/rest/services/Fallzahlen_Total_Kanton/FeatureServer/0/query?where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnHiddenFields=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=Eingangs_Datum&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=standard&f=pjson'
data = sc.jsondownload(json_url, silent=True)

# 2020-04-02
"""
features: [
{
    attributes: {
            Eingangs_Datum: 1582675200000,
            Anzahl_Fälle_total__kumuliert_: 2,
            Neue_Faelle: 2,
            Neue_aktive_Fälle: 2,
            Anzahl_aktive_Fälle_total: 2,
            Anzahl_Personen_in_Isolation: 0,
            Anzahl_Personen_in_Quarantäne: 0,
            Verstorbene: 0,
            Verstorbene__kumuliert_: 0,
            Neue_Hospitalisierungen: 0,
            Hospitalisiert_Total: 0,
            Neu_Pflege: 0,
            Hospitalisiert_Pflege: 0,
            Neu_IPS: 0,
            Hospialisiert_IPS: 0,
            Neu_IPS_beatmet: 0,
            Hospitalisiert_IPS_beatmet: 0,
            FID: 1
    }
},
{
    attributes: {
            Eingangs_Datum: 1582761600000,
            Anzahl_Fälle_total__kumuliert_: 2,
            Neue_Faelle: 0,
            Neue_aktive_Fälle: 0,
            Anzahl_aktive_Fälle_total: 2,
            Anzahl_Personen_in_Isolation: 0,
            Anzahl_Personen_in_Quarantäne: 0,
            Verstorbene: 0,
            Verstorbene__kumuliert_: 0,
            Neue_Hospitalisierungen: 0,
            Hospitalisiert_Total: 0,
            Neu_Pflege: 0,
            Hospitalisiert_Pflege: 0,
            Neu_IPS: 0,
            Hospialisiert_IPS: 0,
            Neu_IPS_beatmet: 0,
            Hospitalisiert_IPS_beatmet: 0,
            FID: 2
    }
},
"""

assert 'features' in data, "JSON did not contain `features` key"

for feature in data['features']:
    row = feature['attributes']
    if not is_first:
        print('-' * 10)
    is_first = False

    dd = sc.DayData(canton='GR', url=json_url)
    dd.datetime = datetime.datetime.fromtimestamp(row['Eingangs_Datum'] / 1000).date().isoformat()
    dd.cases = row['Anzahl_Fälle_total__kumuliert_']
    dd.hospitalized = row['Hospitalisiert_Total']
    dd.icu = row['Hospialisiert_IPS']
    dd.vent = row['Hospitalisiert_IPS_beatmet']
    # Neue_Hospotalisierungen does currently not match our definition of new_hosp
    # GR provides this calculated field as the difference between
    # hospitalized from yesterday and today
    #dd.new_hosp = row['Neue_Hospitalisierungen']
    dd.deaths = row['Verstorbene__kumuliert_']
    dd.isolated = row['Anzahl_Personen_in_Isolation']
    dd.quarantined = row['Anzahl_Personen_in_Quarantäne']
    print(dd)
