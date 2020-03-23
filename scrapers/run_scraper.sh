#!/bin/bash

# Script to run a single scraper

set -e

function cleanup {
  exit $?
}
trap "cleanup" EXIT


# SCRAPER_KEY must be set
if [ -z $SCRAPER_KEY ] || [ -z $SCRAPER_SOURCE ] ; then
  echo "SCRAPER_KEY and SCRAPER_SOURCE env variables must be set"; 
  exit 1
fi

# 1. populate the database with the current CSV
echo "Populating database from CSV COVID19_Fallzahlen_Kanton_${SCRAPER_KEY}_total.csv..."
./populate_database.py ../fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_${SCRAPER_KEY}_total.csv

# 2. run the scraper, update the db
echo "Run the scraper..."
scrape_script="./scrape_${SCRAPER_KEY,,}.sh"
$scrape_script | ./parse_scrape_output.py | ./add_db_entry.py

# 3. Export the database as csv
echo "Export database to CSV..."
sqlite3 -header -csv ./data.sqlite "select * from data;" > ../fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_${SCRAPER_KEY}_total.csv
