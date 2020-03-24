#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo GL
d=$("${DIR}/download.sh" "https://www.gl.ch/verwaltung/finanzen-und-gesundheit/gesundheit/coronavirus.html/4817" | egrep "Fallzahlen Kanton Glarus.+Update|Bestätigte Fälle|Wahrscheinliche Fälle")
echo "Scraped at: $(date --iso-8601=seconds)"

#      <li><strong><a href="#Fallzahlen">Fallzahlen Kanton Glarus</a> (Update 22.03.2020, 13.30 Uhr)</strong></li> 
#...
#      <h2><strong><a id="Fallzahlen" name="Fallzahlen"></a>Coronavirus: Update Kanton Glarus</strong></h2> 
#      <h2>Bestätigte Fälle:&nbsp;<strong>31</strong>&nbsp;</h2> 
#      <h2>Wahrscheinliche Fälle:&nbsp;<strong>--</strong></h2> 
#      <h2>Hospitalisierungen:&nbsp;<strong>3</strong>&nbsp;</h2> 


echo -n "Date and time: "
echo "$d" | egrep "Fallzahlen Kanton" | sed -E -e 's/^.*Update (.+ Uhr)\)<.*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep "Best(ä|&auml;)tigte F(ä|&auml;)lle" | sed -E -e 's/^.*strong>([0-9]+)<.*$/\1/' | head -1
