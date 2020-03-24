#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo SG
d=$("${DIR}/download.sh" "https://www.sg.ch/tools/informationen-coronavirus.html" | grep "Bestätigte Fälle:")
echo "Scraped at: $(date --iso-8601=seconds)"

# 									<div class="col-xs-12"><p>20.03.2020:<br/>Bestätigte Fälle: 98<br/><br/></p></div>

echo -n "Date and time: "
echo "$d" | sed -E -e 's/^.*<p>([0-9]+\.[0-9]+\.[0-9]+):<br.*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | sed -E -e 's/^.*>Bestätigte Fälle: ([0-9]+)<.*$/\1/'
