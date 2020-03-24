#!/bin/sh
set -e

echo BL
URL=$(curl --silent https://www.baselland.ch/politik-und-behorden/direktionen/volkswirtschafts-und-gesundheitsdirektion/amt-fur-gesundheit/medizinische-dienste/kantonsarztlicher-dienst/aktuelles/medienmitteilungen-1 | grep "href=.*update-.*-bestaetigte-faelle" | sed -E -e 's/^.*href="([^"]+)".*$/\1/' | head -1)  # " # To make my editor happy.
d=$(curl --silent "${URL}")

#  <p><span>Der Kantonale Krisenstab gibt Stand Dienstag, 17. März 2020, 14.00 Uhr, 13 neue positive Fälle von Personen mit Wohnsitz im Kanton Basel-Landschaft bekannt. Es sind jetzt insgesamt 89 bestätigte Fälle im Kanton Basel-Landschaft zu verzeichnen. </span></p>
#  <p>Der Kantonale Krisenstab gibt Stand Sonntag, 22. März 2020, 14.00 Uhr,� sieben neue positive Fälle von Personen mit Wohnsitz im Kanton Basel-Landschaft bekannt. Es sind jetzt insgesamt 289 bestätigte Fälle im Kanton Basel-Landschaft zu verzeichnen. Die Anzahl im Kanton Basel-Landschaft am Coronavirus verstorbener Personen beläuft sich auf insgesamt drei.</p>

# Weird character after Uhr,: chr(0xc2), 'Â'  (302 octal)

# Es sind jetzt insgesamt 89 bestätigte Fälle
# Es sind jetzt insgesamt 282 bestätigte Fälle
# Note: There are some non-breaking spaces (ASCII 160 decimal, 240 octal) in between some words / numbers.

echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | tr '\302' ' ' | egrep --text "Stand" | head -1 | tr '\240' ' ' | sed -E -e 's/^.*Stand +[[:alpha:]]+, +(.+ Uhr),.*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | tr '\302' ' ' | egrep --text "Es sind jetzt insgesamt" | head -1 | tr '\240' ' ' | sed -E -e 's/^.*Es sind jetzt insgesamt +([0-9]+) +bestätigte Fälle.*$/\1/'
