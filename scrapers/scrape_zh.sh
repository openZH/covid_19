#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo ZH
d=$("${DIR}/download.sh" "https://gd.zh.ch/internet/gesundheitsdirektion/de/themen/coronavirus.html" | egrep "Im Kanton Zürich sind zurzeit|\\(Stand")
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | grep "Stand" | sed -E -e 's/.*Stand (.+) Uhr.*/\1/'

echo -n "Confirmed cases: "
echo "$d" | grep "posit" | sed -e 's/ /\n/g' | egrep '[0-9]+' | head -1
