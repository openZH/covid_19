#!/bin/sh

# Scrapers are expected to output data on standard output in the following
# format:
#
# GR
# Scraped at: 2020-03-21T19:22:10+01:00
# Date and time: 20.03.2020
# Confirmed cases: 213
# Deaths: 3
#
# Abbreviation of the canton first.
#
# Then scraped timestamp. Current time in ISO-8601 format. Implicitly in Swiss
# timezone (TZ=Europe/Zurich), CET, or CEST.
#
# The information about time of when the data was published / gathered.
# The data and time, or just time, can be omitted if not available.
# Any date / time format is ok. More accurate the better. It is advised to strip
# the name of the weekday. Add time parser to the parse_scrape_output.py script
# if needed.
#
# Number of cases.
#
# Number of deaths can be omitted, if not available.

export WEBARCHIVE_SNAPSHOT=1

for s in ./scrape_*.sh;
do
  if ! ./$s | ./parse_scrape_output.py 2>/dev/null; then
    a=$(echo "$s" | sed -E -e 's/^.*scrape_(..)\..*$/\1/' | tr a-z A-Z) # ' # To make my editor happy.
    echo "$a" - - - FAILED
  fi
done
