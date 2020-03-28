#!/usr/bin/env python3

import json
import scrape_common as sc

print('GR')
d = sc.download('https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/info/Seiten/Start.aspx')
sc.timestamp()
d = sc.filter(r'>Fallzahlen|Best(ä|&auml;)tigte F(ä|&auml;)lle|Personen in Spitalpflege|Verstorbene Personen', d)
d = d.replace('&nbsp;', ' ')
d = d.replace('&#58;', ':')

# 2020-03-27
"""
                                <tr class="normalRow">
                                        <td class="Note"><div class="ExternalClassB7916028EFDA4BF8993C3858B0A09812"><div class="corona-header"><p><strong>Fallzahlen  27.03.2020</strong></p></div></div></td>
                                </tr><tr class="alternatingRow">
                                        <td class="Note"><div class="ExternalClass822792B8A5974741842E201D29A827FC"><div class="corona-message">Bestätigte Fälle&#58; 409<br>Personen in Spitalpflege&#58; 52<br>Verstorbene Personen&#58; 9<br></div></div></td>
                                </tr>
"""

print('Date and time:', sc.find(r'Fallzahlen *([^<]+)<', d).strip())
print('Confirmed cases:', sc.find('Best(ä|&auml;)tigte F(ä|&auml;)lle:? ([0-9]+)[^0-9]', d, group=3))
print('Deaths:', sc.find(r'Verstorbene Person(en)?: ([0-9]+)[^0-9]', d, group=2))


# Note the FORMAT can also be changed to export data in XML.
data = sc.download('https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/_layouts/15/GenericDataFeed/feed.aspx?PageID=26&ID=g_1175d522_e609_4287_93af_d14c9efd5218&FORMAT=JSONRAW')
if data:
  sc.timestamp()

  data = json.loads(data)

  # Sort by date, just in case. ISO 8601 is used, so we can just sort using strings.
  data.sort(key=lambda x: x['date'])

  last_row = data[-1]

  # {'date': '2020-03-27', 'time': '', 'abbreviation_canton_and_fl': 'GR', 'ncumul_tested': '', 'ncumul_conf': '409', 'ncumul_hosp': '52', 'ncumul_ICU': '', 'ncumul_vent': '', 'ncumul_released': '', 'ncumul_deceased': '9', 'source': 'https://www.gr.ch/coronavirus'}
  if last_row['time']:
    print('Date and time:', '{}T{}'.format(last_row['date'], last_row['time']))
  else:
    print('Date and time:', last_row['date'])
  if last_row['ncumul_tested']:
    print('Tested:', last_row['ncumul_tested'])
  print('Confirmed cases:', last_row['ncumul_conf'])
  if last_row['ncumul_hosp']:
    print('Hospitalized:', last_row['ncumul_hosp'])
  if last_row['ncumul_ICU']:
    print('ICU:', last_row['ncumul_ICU'])
  if last_row['ncumul_vent']:
    print('Vent:', last_row['ncumul_vent'])
  if last_row['ncumul_released']:
    print('Recovered:', last_row['ncumul_released'])
  if last_row['ncumul_deceased']:
    print('Deaths:', last_row['ncumul_deceased'])
