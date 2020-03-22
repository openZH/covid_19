#!/bin/sh
set -e

echo VS
d=$(curl --silent "https://www.vs.ch/de/web/coronavirus" | egrep "bestätigte Fälle")
echo "Scraped at: $(date --iso-8601=seconds)"

# <p>21.03.2020: Derzeit gibt es 359 bestätigte Fälle von Coronavirus-Infektionen im Kanton.&nbsp;Insgesamt hat das Virus bisher den Tod von 9&nbsp;Personen im Wallis verursacht.</p>

echo -n "Date and time: "
echo "$d" | egrep "<p>[0-9]+\.[0-9]+\.202[0-2]: Derzeit" | sed -E -e 's/^.*<p>([0-9]+\.[0-9]+\.202[0-2]): .*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | egrep "bestätigte" | sed -E -e 's/^.*es ([0-9]+) best.* Fälle .*$/\1/'

echo -n "Deaths: "
echo "$d" | egrep "Tod" | sed -E -e 's/^.*Tod von ([0-9])+( |&nbsp;)Person.*$/\1/i'
