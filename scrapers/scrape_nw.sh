#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo NW
d=$("${DIR}/download.sh" "https://www.nw.ch/gesundheitsamtdienste/6044" | egrep "Stand:|Bisher (ist bei|sind)")  # " # To make my editor happy.
echo "Scraped at: $(date --iso-8601=seconds)"

# <p class="icmsPContent icms-wysiwyg-first"><em>Stand: 21.&nbsp;März 2020, 18.15&nbsp; Uhr</em></p>
# <p class="icmsPContent">Bisher ist bei 33&nbsp;Personen&nbsp;im Kanton Nidwalden das Coronavirus nachgewiesen worden.&nbsp;<a id="Veranstaltungen" name="Veranstaltungen"></a></p>

# <p class="icmsPContent icms-wysiwyg-first"><em>Stand: 24.&nbsp;März 2020, 15.15&nbsp;Uhr</em></p>
# <p class="icmsPContent">Bisher sind 42&nbsp;Personen&nbsp;im Kanton Nidwalden positiv auf das Coronavirus getestet worden.&nbsp;<a id="Veranstaltungen" name="Veranstaltungen"></a></p>


echo -n "Date and time: "
echo "$d" | grep "Stand:" | sed -E -e 's/^.*em>Stand: *([^<]+)<\/em>.*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep "Bisher (ist|sind)" | sed -E -e 's/^.*(ist bei|sind) ([0-9]+)(&nbsp;| )Pers.*$/\2/'
