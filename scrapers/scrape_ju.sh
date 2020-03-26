#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo JU
d=$("${DIR}/download.sh" "https://www.jura.ch/fr/Autorites/Coronavirus/Accueil/Coronavirus-Informations-officielles-a-la-population-jurassienne.html" | egrep -B 2 'Situation .*2020')
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | grep Situation | sed -E -e 's/^.*Situation (.+)<\/em.*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep "<p.*<strong>[0-9]+" | sed -E -e 's/^.*>([0-9]+)<.*$/\1/'
