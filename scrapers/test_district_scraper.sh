#!/bin/bash

# Script to test run all district scraper

set -e
set -o pipefail

function cleanup {
  exit $?
}
trap "cleanup" EXIT

DIR="$(cd "$(dirname "$0")" && pwd)"
NEWLINE=$'\n'

echo "Run all district scrapers..."

exit_code=0
errors=''
for scrape_script in $DIR/scrape_??_districts.py
do
    if [ -f $scrape_script -a -x $scrape_script ]
    then
        name=`basename $scrape_script`
        canton=${name:7:2}
        export SCRAPER_KEY=${canton^^}
        echo ""
        echo "Running ${SCRAPER_KEY} district scraper..."
        echo "=========================================="

        set +e
        $DIR/run_district_scraper.sh
        ret=$?
        if [ $ret -ne 0 ]
        then
            echo "ERROR: ${scrape_script} failed with exit code $ret. continue." >&2
            errors=$"${errors}${NEWLINE}ERROR: ${scrape_script} failed with exit code $ret"
            exit_code=1
        fi
        set -e

        echo "=========================================="
        echo ""
    fi
done

echo "$errors"
exit $exit_code
