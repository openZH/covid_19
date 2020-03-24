#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo OW
d=$("${DIR}/download.sh" "https://www.ow.ch/de/verwaltung/dienstleistungen/?dienst_id=5962" | egrep '>Stand |ist bei [0-9]+ Personen')
echo "Scraped at: $(date --iso-8601=seconds)"

#<p class="object-pages-img"><img src="../../images/5e73948a8f49f.jpg"  alt="Kampagne BAG" style="width:600;height:293;border:0;" /></p><br /><div class="object-pages-description"><p class="icmsPContent icms-wysiwyg-first"><em>Stand 23.03.2020</em></p>
#...
#...
# <h3 class="icmsH3Content"><strong>Anzahl Infizierte</strong></h3>
# 
# <p class="icmsPContent">Bisher ist bei 25 Personen im Kanton Obwalden das Coronavirus nachgewiesen worden.</p>


echo -n "Date and time: "
echo "$d" | egrep "Stand" | head -1 | sed -E -e 's/^.*Stand ([^<]+)<.*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep "ist bei [0-9]+ Personen" | sed -E -e 's/^.*ist bei ([0-9]+) Personen.*$/\1/'
