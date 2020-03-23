#!/bin/sh
set -e

echo BS
URL=$(./download.sh "https://www.gd.bs.ch/" | egrep 'Tagesbulletin.*Corona' | grep href | head -1 | awk -F '"' '{print $2;}')
d=$(./download.sh "https://www.gd.bs.ch/${URL}" | grep "positive Fälle")
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | sed -E -e 's/^.*Stand [A-Za-z]*,? (.+), insgesamt.*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | sed -E -e 's/^.*insgesamt ([0-9]+) positive.*$/\1/'
