#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo UR
d=$("${DIR}/download.sh" "https://www.ur.ch/themen/2920" | egrep "Personen gestiegen|Anstieg auf [0-9]+ Person")
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
#echo "$d" | sed -E -e 's/^.*\(Stand[A-Za-z ]*, ([^\)]+)\).*$/\1/'
echo "$(date --iso-8601=date)"  # Current website doesn't provide information about day or hour. :/ Fake it.

echo -n "Confirmed cases: "
echo "$d" | sed -E -e 's/^.* ([0-9]+) Personen gestiegen.*$/\1/' -e 's/^.*Anstieg auf ([0-9]+) Person.*$/\1/' | head -1
