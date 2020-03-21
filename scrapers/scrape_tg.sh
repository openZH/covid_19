#!/bin/sh
set -e

echo TG
d=$(curl --silent "https://www.tg.ch/news/fachdossier-coronavirus.html/10552" | egrep "<li>Anzahl bestätigter|<em>Stand")
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | grep "Stand" | sed -E -e 's/^.*Stand ([^<]+)<.*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | grep 'Anzahl' | sed -E -e 's/.* ([0-9]+)<.*$/\1/'
