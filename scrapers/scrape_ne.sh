#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo NE
d=$("${DIR}/download.sh" "https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Pages/Coronavirus.aspx" | grep 'Nombre de cas confirmés')
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | sed -E -e 's/^.*>Neuchâtel(&#160;)* +([^<]+)<\/span>.*$/\2/'

echo -n "Confirmed cases: "
echo "$d" | sed -E -e 's/<br>/\n/g' | grep -A 3 ">Neuchâtel" | egrep "Nombre de .* confirmés" | sed -E -e 's/^.*[^0-9]+([0-9]+) pers.*$/\1/'

echo -n "Deaths: "
echo "$d" | sed -E -e 's/<br>/\n/g' | grep -A 3 ">Neuchâtel" | egrep "Nombre.* décès" | head -1 | sed -E -e 's/^.*[^0-9]+ ([0-9]+)( pers.*|<\/strong).*$/\1/'
