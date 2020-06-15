#!/bin/bash

# Script to run a single scraper

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

area="Kanton_${SCRAPER_KEY}"
if [ "$SCRAPER_KEY" = "FL" ] ; then
   area="${SCRAPER_KEY}"
fi

# 1. Validate the result
node $DIR/../scripts/validate-csv.js $DIR/../fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_${area}_total.csv

# 2. Check for outliers
python $DIR/../scripts/check_for_outliers.py $DIR/../fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_${area}_total.csv
