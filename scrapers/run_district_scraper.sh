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

# run the scraper
echo "Run the district scraper..."
scrape_script="${DIR}/scrape_${SCRAPER_KEY,,}_districts.py"
$scrape_script > $DIR/../fallzahlen_bezirke/fallzahlen_kanton_${SCRAPER_KEY}_bezirk.csv
