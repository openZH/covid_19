#!/bin/bash

# Script to run a single scraper

set -e
set -o pipefail

function cleanup {
  exit $?
}
trap "cleanup" EXIT

DIR="$(cd "$(dirname "$0")" && pwd)"


echo "Run all scrapers..."
scrape_script="${DIR}/scrape_*.py"
$scrape_script | $DIR/parse_scrape_output.py 

for scrape_script in $DIR/scrape_??.py
do
    if [ -f $scrape_script -a -x $scrape_script ]
    then
        name=`basename $scrape_script`
        echo "Running $name..."
        $scrape_script
        echo "=========================================="
        echo ""
    fi
done
