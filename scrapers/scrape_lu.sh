#!/bin/sh
set -e

echo LU
d=$(curl --silent "https://gesundheit.lu.ch/themen/Humanmedizin/Infektionskrankheiten/Coronavirus" | grep "Im Kanton Luzern gibt es" | awk -F '>' '{print $3;}')
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | sed -E -e 's/^.*Stand: (.+)(Uhr)?\).+$/\1/'

echo -n "Confirmed cases: "
echo "$d" | sed -e 's/ /\n/g' | egrep '[0-9]+' | head -1
