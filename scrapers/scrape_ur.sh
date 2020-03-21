#!/bin/sh
set -e

echo UR
d=$(curl --silent "https://www.ur.ch/themen/2920" | grep "Personen gestiegen")
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | sed -E -e 's/^.*\(Stand[A-Za-z ]*, ([^\)]+)\).*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | sed -E -e 's/^.* ([0-9]+) Personen gestiegen.*$/\1/'
