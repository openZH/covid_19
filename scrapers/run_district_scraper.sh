#!/bin/bash

# Script to run a single district scraper

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
echo "Populating database from CSV fallzahlen_kanton_${SCRAPER_KEY}_bezirk..."
$DIR/populate_district_database.py $DIR/../fallzahlen_bezirke/fallzahlen_kanton_${SCRAPER_KEY}_bezirk.csv

# 2. run the scraper, update the db
echo "Run the district scraper..."
scrape_script="${DIR}/scrape_${SCRAPER_KEY,,}_districts.py"
$scrape_script | $DIR/add_district_db_entry.py

# 3. Export the database as csv
echo "Export database to CSV..."
sqlite3 -header -csv $DIR/data.sqlite "select * from data order by DistrictId, District, Canton, Date, Year, Week+0 asc;" > $DIR/../fallzahlen_bezirke/fallzahlen_kanton_${SCRAPER_KEY}_bezirk.csv
sed -i 's/""//g' $DIR/../fallzahlen_bezirke/fallzahlen_kanton_${SCRAPER_KEY}_bezirk.csv
