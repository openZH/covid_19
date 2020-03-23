#!/bin/sh
set -e

echo SO
d=$(./download.sh "https://corona.so.ch/" | egrep "Situation Kanton Solothurn.*Stand|Anzahl positiv getesteter Erkrankungsfälle|Verstorben:")
echo "Scraped at: $(date --iso-8601=seconds)"

# <p class="bodytext"><strong>Situation Kanton Solothurn (Stand 23.03.2020, 12:00)</strong></p><ul><li>Anzahl positiv getesteter Erkrankungsfälle: 95 Personen</li> 	<li>Verstorben:<strong> </strong>1 Person</li></ul><p class="bodytext"> </p></div></div>



echo -n "Date and time: "
echo "$d" | egrep "Situation Kanton Solothurn.*Stand" | head -1 | sed -E -e 's/^.*\(Stand (.+)\)<.+$/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep "Anzahl positiv getesteter Erkrankungsfälle: [0-9]+ " | head -1 | sed -E -e 's/^.*Anzahl positiv getesteter Erkrankungsfälle: ([0-9]+) .*$/\1/'

echo -n "Deaths: "
echo "$d" | egrep "Verstorben:.*[0-9]+" | head -1 | sed -E -e 's/^.*Verstorben:(<strong> <\/strong>)?([0-9]+) .*$/\2/'
