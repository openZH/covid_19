#!/bin/sh
set -e

echo GE
d=$(curl --silent "https://www.ge.ch/document/point-coronavirus-maladie-covid-19/telecharger" | pdftotext - - | egrep "Dans le canton de Genève|Actuellement.*cas ont|décédées")
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | grep "Dans le" | sed -E -e 's/.*\((.*)\).*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | grep "cas ont" | sed -E -e 's/( |<)/\n/g' | egrep '[0-9]+' | head -1

echo -n "Deaths: "
echo "$d" | grep "décédées" | sed -E -e 's/^.*([0-9]+) [^,]* décédées.*$/\1/'
