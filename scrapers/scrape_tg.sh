#!/usr/bin/env python3

import scrape_common as sc

print('TG')
d = sc.download('https://www.tg.ch/news/fachdossier-coronavirus.html/10552')
sc.timestamp()
d = sc.filter(r'<li>Anzahl bestätigter|<em>Stand', d)

# 2020-03-25
"""
      <li>Anzahl bestätigter Fälle: 96</li> 
     <p><em>Stand 25.3.20</em></p> 
"""

print('Date and time:', sc.find(r'Stand ([^<]+)<', d))
print('Confirmed cases:', sc.find(r'Anzahl bestätigter Fälle: ([0-9]+)<', d))
