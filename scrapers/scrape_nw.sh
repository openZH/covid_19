#!/bin/sh
set -e

echo NW
d=$(./download.sh "https://www.nw.ch/gesundheitsamtdienste/6044" | egrep "Stand:|Bisher ist bei")
echo "Scraped at: $(date --iso-8601=seconds)"

# <p class="icmsPContent icms-wysiwyg-first"><em>Stand: 21.&nbsp;März 2020, 18.15&nbsp; Uhr</em></p>
# <p class="icmsPContent">Bisher ist bei 33&nbsp;Personen&nbsp;im Kanton Nidwalden das Coronavirus nachgewiesen worden.&nbsp;<a id="Veranstaltungen" name="Veranstaltungen"></a></p>

echo -n "Date and time: "
echo "$d" | grep "Stand:" | sed -E -e 's/^.*em>Stand: *([^<]+)<\/em>.*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | grep "Bisher ist" | sed -E -e 's/^.*ist bei ([0-9]+)(&nbsp;| )Pers.*$/\1/'
