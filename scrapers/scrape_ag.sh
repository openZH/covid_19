#!/bin/sh
set -e

echo AG
URL=$(curl --silent "https://www.ag.ch/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp" | sed -E -e 's/<li>/\n<li>/g' | grep Bulletin | grep pdf | grep href | awk -F '"' '{print $6;}' | head -1)
d=$(curl --silent "https://www.ag.ch/${URL}" | pdftotext - - | egrep -A 2 "(Aarau, .+Uhr|Stand [A-Za-z]*, [0-9]+)")  # " # To make my editor happy.
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | grep "Aarau," | sed -E -e 's/.*, (.+)/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep '^[0-9]+$'
