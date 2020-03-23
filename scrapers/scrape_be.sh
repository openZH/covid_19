#!/bin/sh
set -e

echo BE
d=$(./download.sh "https://www.besondere-lage.sites.be.ch/besondere-lage_sites/de/index/corona/index.html" | grep -A 20 'table cellspacing="0" summary="Laufend aktualisierte Zahlen')
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | grep "Stand:" | sed -E -e 's/^.*Stand: (.+)\).*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep '<td .*<strong>[0-9]+<' | sed -E -e 's/.*>([0-9]+)<.*/\1/'

echo -n "Deaths: "
echo "$d" | egrep '<td[^<>]*>[0-9]+</td>' | sed -E -e 's/.*>([0-9]+)<.*/\1/'
