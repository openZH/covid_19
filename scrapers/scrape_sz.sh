#!/bin/sh
set -e

echo SZ

#       <h2>Medienmitteilungen des kantonalen Führungsstabs</h2> 
#       <ul> 
#        <li><a href="https://www.sz.ch/public/upload/assets/45637/MM_KFS_Corona_17_3_2020.pdf">Medienmitteilung vom 17. März 2020</a></li> 

URL=$(./download.sh 'https://www.sz.ch/behoerden/information-medien/medienmitteilungen/coronavirus.html/72-416-412-1379-6948' | grep -A 3 "Medienmitteilungen des kantonalen Führungsstabs" | grep "<li>" | head -1 | awk -F '"' '{print $2;}')
d=$(./download.sh "${URL}" | pdftotext - - | grep "bestätigte Fälle|Schwyz, .+ 202")
echo "Scraped at: $(date --iso-8601=seconds)"

# Schwyz, 17. März 2020
# Im Kanton Schwyz sind aktuell 13 bestätigte Fälle registriert.

echo -n "Date and time: "
echo "$d" | egrep "Schwyz, .* 202" | sed -E -e 's/^.*Schwyz, (.+ 202[2-9]).*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep "aktuell" | sed -E -e 's/^.*aktuell ([0-9]+) bestätigte Fälle.*$/\1/'

# The latest PDF from 2020-03-17 doesn't mention numbers. Some previous did tho.
