#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo GR
d=$("${DIR}/download.sh" "https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/info/Seiten/Start.aspx" | egrep ">Fallzahlen|Best(ä|&auml;)tigte F(ä|&auml;)lle|Personen in Spitalpflege|Verstorbene Personen")  # " # - to make my editor happy
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | grep Fallzahlen | sed -E -e 's/.*Fallzahlen ([^<]+)<.*/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep "Best(ä|&auml;)tigte F(ä|&auml;)lle" | sed -E -e 's/( |<)/\n/g' | egrep '[0-9]+' | head -1

echo -n "Deaths: "
echo "$d" | grep "Verstorbene" | sed -E -e 's/( |<)/\n/g' | sed -E -e 's/&nbsp;//g' | egrep '^[0-9]+' | head -1
