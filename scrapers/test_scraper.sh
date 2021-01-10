#!/bin/bash

# Script to run a single scraper

set -e
set -o pipefail

function cleanup {
  exit $?
}
trap "cleanup" EXIT

DIR="$(cd "$(dirname "$0")" && pwd)"
NEWLINE=$'\n'

echo "Run all scrapers..."

exit_code=0
errors=''
for scrape_script in $DIR/scrape_??.py
do
    if [ -f $scrape_script -a -x $scrape_script ]
    then
        name=`basename $scrape_script`
        canton=${name:7:2}
        export SCRAPER_KEY=${canton^^}
        echo ""
        echo "Running ${SCRAPER_KEY} scraper..."
        echo "=========================================="

        set +e
        $DIR/run_scraper.sh
        ret=$?
        if [ $ret -ne 0 ]
        then
            echo "ERROR: ${scrape_script} failed with exit code $ret. continue." >&2
            errors=$"${errors}${NEWLINE}ERROR: ${scrape_script} failed with exit code $ret"
            exit_code=1
        fi
        $DIR/validate_scraper_output.sh
        ret=$?
        if [ $ret -ne 0 ]
        then
            echo "ERROR: Validation for ${SCRAPER_KEY} failed with exit code $ret. continue." >&2
            errors=$"${errors}${NEWLINE}ERROR: Validation for ${SCRAPER_KEY} failed with exit code $ret"
            exit_code=1
        fi
        set -e

        echo "=========================================="
        echo ""
    fi
done

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

for scrape_script in $DIR/scrape_??_tests.py
do
    if [ -f $scrape_script -a -x $scrape_script ]
    then
        name=`basename $scrape_script`
        canton=${name:7:2}
        export SCRAPER_KEY=${canton^^}
        echo ""
        echo "Running ${SCRAPER_KEY} tests scraper..."
        echo "=========================================="

        set +e
        $DIR/run_tests_scraper.sh
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

for scrape_script in $DIR/scrape_??_vaccinations.py
do
    if [ -f $scrape_script -a -x $scrape_script ]
    then
        name=`basename $scrape_script`
        canton=${name:7:2}
        export SCRAPER_KEY=${canton^^}
        echo ""
        echo "Running ${SCRAPER_KEY} vaccinations scraper..."
        echo "=========================================="

        set +e
        $DIR/run_vaccinations_scraper.sh
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
