#!/usr/bin/env python3

# This script removes (=sets to empty string) older entries from a CSV
# in this example remove current_hosp prior to 2020-05-19

import csv
import sys
import traceback
import datetime

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
              'new_hosp': r['new_hosp'],
              'current_hosp': r['current_hosp'],
              'current_icu': r['current_icu'],
              'current_vent': r['current_vent'],
              'ncumul_released': r['ncumul_released'],
              'ncumul_deceased': r['ncumul_deceased'],
              'source': r['source'],
              'current_isolated': r.get('current_isolated', ''),
              'current_quarantined': r.get('current_quarantined', ''),
              'current_quarantined_riskareatravel': r.get('current_quarantined_riskareatravel', ''),  # new field
              'current_quarantined_total': r.get('current_quarantined_total', ''),  # new field
            }
            if datetime.datetime.strptime(data['date'], '%Y-%m-%d') < datetime.datetime(2020, 5, 19):
                data['current_hosp'] = ''
            # re-add extra columns
            for col in dr.fieldnames[12:]:
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
