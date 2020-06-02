#!/usr/bin/env python3

# This script convert CSV files from the old to the new structure

import csv
import sys
import traceback

assert len(sys.argv) == 2, "Call script with CSV file as parameter"

try:
    filename = sys.argv[1]
    rows = []
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
              'current_isolated': '',
              'current_quarantined': '',
            }
            # re-add extra columns
            for col in dr.fieldnames[11:]:
                data[col] = r[col]
            rows.append(data)

    writer = csv.DictWriter(
        sys.stdout,
        rows[0].keys(),
        delimiter=',',
        quotechar='"',
        lineterminator='\n',
        quoting=csv.QUOTE_MINIMAL
    )
    writer.writeheader()
    writer.writerows(rows)
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
finally:
    sys.stdout.flush()
