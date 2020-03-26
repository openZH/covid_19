#!/usr/bin/env python3

import scrape_common as sc

print('JU')
d = sc.download('https://www.jura.ch/fr/Autorites/Coronavirus/Accueil/Coronavirus-Informations-officielles-a-la-population-jurassienne.html')
sc.timestamp()
# d = sc.filter(r'Situation .*2020', d) # + 2 lines before.

print('Date and time:', sc.find(r'Situation (.+?)<\/em', d))
print('Confirmed cases:', sc.find(r'<p.*?<strong>([0-9]+)<', d))
