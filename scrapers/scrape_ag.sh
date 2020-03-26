#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo AG

# From the new website:
d=$("${DIR}/download.sh" "https://www.ag.ch/de/themen_1/coronavirus_2/alle_ereignisse/alle_ereignisse_1.jsp" | egrep 'Neues Lagebulletin')
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | sed -E -e 's/Neues Lagebulletin/\n/g' | egrep 'class="timeline__time" datetime="00.*00"' | sed -E -e 's/^.*class="timeline__time" datetime="00(.*00)".*$/\1/' | head -1

echo -n "Confirmed cases: "
echo "$d" | sed -E -e 's/Neues Lagebulletin/\n/g' | egrep "zurzeit [0-9]+ best(ä|&auml;)tigte F(ä|&auml;)lle" | sed -E -e 's/^.*zurzeit ([0-9]+) best(ä|&auml;)tigte F(ä|&auml;)lle.*$/\1/' | head -1

echo -n "Hospitalized: "
echo "$d" | sed -E -e 's/Neues Lagebulletin/\n/g' | egrep "[0-9]+ Person(en)? sind zurzeit hospitalisiert" | sed -E -e 's/^.* ([0-9]+) Person(en)? sind zurzeit hospitalisiert.*$/\1/' | head -1

echo -n "ICU: "
echo "$d" | sed -E -e 's/Neues Lagebulletin/\n/g' | egrep "[0-9]+ Person(en)? werden auf Intensivstationen behandelt" | sed -E -e 's/^.* ([0-9]+) Person(en)? werden auf Intensivstationen behandelt.*$/\1/' | head -1

echo -n "Vent: "
echo "$d" | sed -E -e 's/Neues Lagebulletin/\n/g' | egrep "[0-9]+ Person(en)? k(ü|&uuml;)nstlich beatmet werden" | sed -E -e 's/^.* ([0-9]+) Person(en)? k(ü|&uuml;)nstlich beatmet werden.*$/\1/' | head -1

echo -n "Deaths: "
echo "$d" | sed -E -e 's/Neues Lagebulletin/\n/g' | sed -E -e 's/zwei/2/g' | egrep "[0-9]+ Person(en)? an den Folgen des Coronavirus verstorben" | sed -E -e 's/^.* ([0-9]+) Person(en)? an den Folgen des Coronavirus verstorben.*$/\1/' | head -1
