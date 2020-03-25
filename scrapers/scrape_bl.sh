#!/bin/sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"  # " # To make editor happy

echo BL

URL="https://www.statistik.bl.ch/files/sites/Grafiken/COVID19/Grafik_COVID19_BL_Linie.htm"
d=$("${DIR}/download.sh" "${URL}")

# <pre id="data" style="display:none;">Datum, Bestätigte Fälle, Verstorbene
# 28-02-2020,1,
# 29-02-2020,2,
# 01-03-2020,2,
# 02-03-2020,2,
# ...
# 21-03-2020,282,3
# 22-03-2020,289,3
# 23-03-2020,302,3
# 24-03-2020,306,4
# </pre>

echo "Scraped at: $(date --iso-8601=seconds)"
line=$(echo "$d" | sed -n '/<pre id\="data"/,$p' | grep "</pre>" -m1 -B1 | head -1)

echo -n "Date and time: "
echo "$line" | cut -d "," -f 1 | sed 's/\-/./g'

echo -n "Confirmed cases: "
echo "$line" | cut -d "," -f 2

echo -n "Deaths: "
echo "$line" | cut -d "," -f 3
