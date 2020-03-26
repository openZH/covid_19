#!/usr/bin/env python3

import scrape_common as sc

print('GE')
d = sc.pdfdownload('https://www.ge.ch/document/point-coronavirus-maladie-covid-19/telecharger')
sc.timestamp()

#d = sc.filter(r'Dans le canton de Genève|Actuellement.*cas ont|décédées|hospitalisés', d) # + 1 line.

# 2020-03-23
"""
Cette fiche destinée à la population générale
dresse un état des lieux de la situation au 23
mars 2020.

Chiffres clés au 22 mars 2020 (OMS, OFSP
et DGS pour la Suisse et Genève)
Chine

81'498 cas

3'267 décès

Europe

151'293 cas

7'426 décès

Italie

53'578 cas

4'827 décès

Suisse

8'060 cas

66 décès

Genève

1'203 cas

9 décès

Dans le canton de Genève (23.03 à 12h)
Actuellement, 1'231 cas ont été confirmés. Le nombre de
cas continue de progresser.
Actuellement, au total 214 patients sont hospitalisés,
dont 43 aux soins intensifs. A l’heure actuelle, 9
personnes sont décédées dans le canton des suites de
la maladie.
"""


# 2020-03-24
"""
Dans le canton de Genève (24.03 à 12h)
Actuellement, 1510 cas ont été confirmés. Le nombre de
cas continue de progresser.
Actuellement, au total 238 patients sont hospitalisés,
dont 41 aux soins intensifs. A l’heure actuelle, 12
personnes sont décédées dans le canton des suites de
la maladie.

"""

# Use non-greedy matching.
print('Date and time:', sc.find(r'Dans le.*\((.*?h)\)', d))

# To handle: 1'231 as 1231
d = d.replace("'", '')

print('Confirmed cases:', sc.find(r', ([0-9]+) cas ont', d))

print('Hospitalized:', sc.find(r'total ([0-9]+) patients?.*hospitalis', d))

print('ICU:', sc.find(r'dont ([0-9]+) aux soins? intensifs?', d))

# Due to pdf line wrapping, merge new lines into one line for easier matching.
d = d.replace('\n', ' ')
# Use non-greedy matching.
print('Deaths:', sc.find(r'\b([0-9]+) [^,\.]*? décédées', d))
