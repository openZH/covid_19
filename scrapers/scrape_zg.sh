#!/bin/sh
set -e

echo ZG
d=$(curl --silent "https://www.zg.ch/behoerden/gesundheitsdirektion/amt-fuer-gesundheit/corona" | egrep 'Infizierte Personen|Genesene Personen|Verstorbene Personen|Stand:')
echo "Scraped at: $(date --iso-8601=seconds)"


#      <p>Infizierte Personen: 62</p>
#<p>Genesene Personen: 10</p>
#<p>Verstorbene Personen: 0</p>
#<p>Stand: 23.3.2020, 8.00 Uhr</p>


echo -n "Date and time: "
echo "$d" | egrep "Stand" | head -1 | sed -E -e 's/^.*Stand:? ([^<]+ Uhr)<.*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep "Infizierte Personen" | head -1 | sed -E -e 's/^.*Infizierte Personen:? ([0-9]+)<.*$/\1/'

echo -n "Deaths: "
echo "$d" | egrep "Verstorbene Personen" | head -1 | sed -E -e 's/^.*Verstorbene Personen:? ([0-9]+)<.*$/\1/'

echo -n "Recovered: "
echo "$d" | egrep "Genesene Personen" | head -1 | sed -E -e 's/^.*Genesene Personen:? ([0-9]+)<.*$/\1/'
