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

for scrape_script in $DIR/scrape_??.py
do
    if [ -f $scrape_script -a -x $scrape_script ]
    then
        name=`basename $scrape_script`
        echo ""
        echo "Running $name..."
        echo "=========================================="
        $scrape_script | $DIR/parse_scrape_output.py
        echo "=========================================="
        echo ""
    fi
done
