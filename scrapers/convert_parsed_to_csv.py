#!/usr/bin/env python3

# Reads data in a format produced by ./parse_scrape_output.py
# from standard input, and converts into CSV file on a standard output.
#
# Example usage:
#   ./meta_scrape.sh | ./convert_parsed_to_csv.py > latest.csv
#   ./scrape_vd.sh | ./parse_scrape_output.py | ./convert_parsed_to_csv.py > vd.csv
#   cat *0.txt | ./convert_parsed_to_csv.py > full_history.csv
#
# See README.md for details about columns defined in CSV format.

import csv
import re
import sys

# See README.md for more details about these fields.
field_names = [
    'date',
    'time',
    'abbreviation_canton_and_fl',
    'ncumul_tested',
    'ncumul_conf',
    'ncumul_hosp',  # Actually not cumulative.
    'ncumul_ICU',   # Actually not cumulative.
    'ncumul_vent',  # Actually not cumulative.
    'ncumul_released',
    'ncumul_deceased',
    'source',
]

writer = csv.DictWriter(sys.stdout, field_names,
                        delimiter=',',
                        quotechar='"',
                        lineterminator='\n',
                        quoting=csv.QUOTE_MINIMAL)

writer.writeheader()

input_failures = 0
for line in sys.stdin:
    l = line.strip()

    # AR 2020-03-23T10:00      30       1 OK 2020-03-23T19:12:09+01:00 https://www.ai.ch/themen/gesundheit-alter-und-soziales/gesundheitsfoerderung-und-praevention/uebertragbare-krankheiten/coronavirus
    # GE 2020-03-27T         1924      23 OK 2020-03-28T18:57:34+01:00 # Extras: ncumul_hosp=313,ncumul_ICU=54 # URLs: https://www.ge.ch/document/point-coronavirus-maladie-covid-19/telecharger

    # Groups:             1              2                                         3       4              5                               6                            7             8
    match = re.search(r'^([A-Z][A-Z])\s+((?:\d\d\d\d-\d\d-\d\d)T(?:\d\d:\d\d)?)\s+(\d+)\s+(\d+|-)\s+OK\s+([0-9:\+\-\.T]+)(?:\s+# Extras: ([^#]+))?(?:\s+(?:(# URLs: )?(h.+)))?(?:\s+(http.+))?$', l)
    if not match:
        input_failures += 1
        print(f"Failed to parse line: {l}", file=sys.stderr)
        continue

    abbr = match.group(1)

    date_part = match.group(2).split('T', 2)

    data = {
        'date': date_part[0],
        'time': None,
        'abbreviation_canton_and_fl': abbr,
        'ncumul_tested': None,
        'ncumul_conf': int(match.group(3)),
        'ncumul_hosp': None,
        'ncumul_ICU': None,
        'ncumul_vent': None,
        'ncumul_released': None,
        'ncumul_deceased': None,
        'source': '',
    }

    if len(date_part) == 2:
        data['time'] = date_part[1]

    if match.group(4) != '-':
        data['ncumul_deceased'] = int(match.group(4))

    scrape_time = match.group(5)

    url_sources = match.group(7)
    if match.group(8):
        url_sources = match.group(8)
    if url_sources:
        data['source'] = f'Scraper for {abbr} at {scrape_time} using {url_sources}'
    else:
        data['source'] = f'Scraper for {abbr} at {scrape_time}'

    # Parse optional data.
    extras_list = match.group(6)
    if extras_list:
        try:
            extras = extras_list.strip()
            extras = extras.split(',')
            extras = { kv.split('=', 2)[0]: int(kv.split('=', 2)[1]) for kv in extras }
            # data.update(extras)
            for k in ['ncumul_hosp', 'ncumul_ICU', 'ncumul_vent', 'ncumul_released', 'new_hosp', 'current_hosp']:
                if k in extras:
                    data[k] = extras[k]
        except Exception as e:
            input_failures += 1
            print(f'Error: Parsing optional data failed, ignoring: {extras_list}', file=sys.stderr)

    # print(data)
    writer.writerow(data)

sys.stdout.flush()

if input_failures:
    sys.exit(1)
