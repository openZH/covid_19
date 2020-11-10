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

# 1. populate the database with the current CSV
echo "Populating database from CSV fallzahlen_kanton_${SCRAPER_KEY}_tests..."
$DIR/populate_tests_database.py $DIR/../fallzahlen_tests/fallzahlen_kanton_${SCRAPER_KEY}_tests.csv

# 2. run the scraper, update the db
echo "Run the tests scraper..."
scrape_script="${DIR}/scrape_${SCRAPER_KEY,,}_tests.py"
$scrape_script | $DIR/add_tests_db_entry.py

# 3. Export the database as csv
echo "Export database to CSV..."
sqlite3 -header -csv $DIR/data.sqlite "select * from data order by canton, start_date, end_date, week, year asc;" > $DIR/../fallzahlen_tests/fallzahlen_kanton_${SCRAPER_KEY}_tests.csv
sed -i 's/""//g' $DIR/../fallzahlen_tests/fallzahlen_kanton_${SCRAPER_KEY}_tests.csv
