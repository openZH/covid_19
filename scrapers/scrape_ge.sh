#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo GE
d=$("${DIR}/download.sh" "https://www.ge.ch/document/point-coronavirus-maladie-covid-19/telecharger" | pdftotext - - | egrep -B 1 "Dans le canton de Genève|Actuellement.*cas ont|décédées|hospitalisés")
echo "Scraped at: $(date --iso-8601=seconds)"

cat >/dev/null <<EOF
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
EOF


echo -n "Date and time: "
echo "$d" | grep "Dans le" | sed -E -e 's/.*\((.*)\).*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | grep "cas ont" | sed -E -e 's/( |<)/\n/g' | sed "s/'//g" | egrep '[0-9]+' | head -1


echo -n "Hospitalized: "
echo "$d" | grep "hospitalisés" | sed -E -e "s/'//g" | sed -E -e 's/^.*total ([0-9]+) patients?.*hospitalis.*$/\1/' | head -1

# Due to pdf line wrapping. Also match previous line and merge it into single line.
D=$(echo "$d" | grep -B 2 "décédées" | tr '\n' ' ' | sed "s/'//g" | sed -E -e 's/^.*([0-9]+) [^,]* décédées.*$/\1/')  # ' # Make my editor happy.
echo "Deaths: ${D}"
