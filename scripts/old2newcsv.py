#!/usr/bin/env python3

# This script convert CSV files from the old strucutre to the new structure

import sqlite3
import csv
import traceback
import os
import sys

assert len(sys.argv) == 2, "Call script with CSV file as parameter"

field_names = [
    'date',
    'time',
    'abbreviation_canton_and_fl',
    'ncumul_tested',
    'ncumul_conf',
    'new_hosp',
    'current_hosp',
    'current_icu',
    'current_vent',
    'ncumul_released',
    'ncumul_deceased',
    'source',
]

try:
    writer = csv.DictWriter(
        sys.stdout,
        field_names,
        delimiter=',',
        quotechar='"',
        lineterminator='\n',
        quoting=csv.QUOTE_MINIMAL
    )
    writer.writeheader()

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        dr = csv.DictReader(f) 
        for r in dr:
            # map old to new structure
            data = {
              'date': r['date'],
              'time': r['time'],
              'abbreviation_canton_and_fl': r['abbreviation_canton_and_fl'],
              'ncumul_tested': r['ncumul_tested'],
              'ncumul_conf': r['ncumul_conf'],
              'new_hosp': '',
              'current_hosp': r['ncumul_hosp'],
              'current_icu': r['ncumul_ICU'],
              'current_vent': r['ncumul_vent'],
              'ncumul_released': r['ncumul_released'],
              'ncumul_deceased': r['ncumul_deceased'],
              'source': r['source'],
            }
            # re-add extra columns
            for col in dr.fieldnames[11:]:
                data[col] = r[col]
            writer.writerow(data)
except Exception as e:
    print("Error: %s" % e)
    print(traceback.format_exc())
    sys.exit(1)
finally:
    sys.stdout.flush()
