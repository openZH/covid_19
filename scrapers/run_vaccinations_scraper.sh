#!/bin/bash

# Script to run a single tests scraper

set -e
set -o pipefail

function cleanup {
  exit $?
}
trap "cleanup" EXIT

DIR="$(cd "$(dirname "$0")" && pwd)"


# SCRAPER_KEY must be set
if [ -z $SCRAPER_KEY ] ; then
  echo "SCRAPER_KEY env variable must be set"; 
  exit 1
fi

area="kanton_${SCRAPER_KEY}"
if [ "$SCRAPER_KEY" = "FL" ] ; then
   area="${SCRAPER_KEY}"
fi

# 1. populate the database with the current CSV
echo "Populating database from CSV fallzahlen_${area}_vaccinations..."
$DIR/populate_vaccinations_database.py $DIR/../fallzahlen_impfungen/fallzahlen_${area}_impfungen.csv

# 2. run the scraper, update the db
echo "Run the vaccinations scraper..."
scrape_script="${DIR}/scrape_${SCRAPER_KEY,,}_vaccinations.py"
$scrape_script | $DIR/add_vaccinations_db_entry.py

# 3. Export the database as csv
echo "Export database to CSV..."
sqlite3 -header -csv $DIR/data.sqlite "select * from data order by canton, start_date, end_date, year, week+0 asc;" > $DIR/../fallzahlen_impfungen/fallzahlen_${area}_impfungen.csv
sed -i 's/""//g' $DIR/../fallzahlen_impfungen/fallzahlen_${area}_impfungen.csv
