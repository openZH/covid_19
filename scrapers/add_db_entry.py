#!/usr/bin/env python3

import re
import sys
import sqlite3
import traceback
import os

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)

input_failures = 0

try:
    DATABASE_NAME = os.path.join(__location__, 'data.sqlite')
    conn = sqlite3.connect(DATABASE_NAME)

    i = 0
    for line in sys.stdin:
        l = line.strip()
        # Groups:            1       2             3       4           5
        match = re.search('^(\w+)\s+([\w\-\:]+)\s+(\w+)\s+(\w+|-)\s+OK(.*)$', l)
        if not match:
          input_failures += 1
          print(f'Error: Not matched input line: {l}')
          continue
        date_part = match.group(2).split('T')
        data = {
            'date': date_part[0],
            'time': '',
            'area': os.environ['SCRAPER_KEY'],
            'tested': '',
            'confirmed': int(match.group(3)),
            'hospitalized': '',
            'icu': '',
            'vent': '',
            'released': '',
            'deceased': match.group(4),
            'source': os.environ['SCRAPER_SOURCE']
        }

        if len(date_part) == 2:
            data['time'] = date_part[1]

        if (data['deceased'] == '-'):
            data['deceased'] = ''
        else:
            data['deceased'] = int(data['deceased'])

        # Parse optional data.
        rest = match.group(5)
        extras_match = re.search('# Extras: ([^#]+)', rest)
        if extras_match:
          try:
            extras = extras_match.group(1).strip()
            extras = extras.split(',')
            extras = { kv.split('=', 2)[0]: int(kv.split('=', 2)[1]) for kv in extras }
            if 'ncumul_hosp' in extras:
              data['hospitalized'] = extras['ncumul_hosp']
            if 'ncumul_ICU' in extras:
              data['icu'] = extras['ncumul_ICU']
            # if 'ninst_ICU_intub' in extras:
            #   data['intubated'] = extras['ninst_ICU_intub']
            if 'ncumul_vent' in extras:
              data['vent'] = extras['ncumul_vent']
            if 'ncumul_released' in extras:
              data['released'] = extras['ncumul_released']
          except Exception as e:
            print(f'Error: Parsing optional data failed, ignoring: {extras_match.group(1)}')

        c = conn.cursor()
        try:
            print(data)
            c.execute(
                '''
                INSERT INTO data (
                    date,
                    time,
                    abbreviation_canton_and_fl,
                    ncumul_tested,
                    ncumul_conf,
                    ncumul_hosp,
                    ncumul_ICU,
                    ncumul_vent,
                    ncumul_released,
                    ncumul_deceased,
                    source
                )
                VALUES
                (?,?,?,?,?,?,?,?,?,?,?)
                ''',
                [
                    data['date'],
                    data['time'],
                    data['area'],
                    data['tested'],
                    data['confirmed'],
                    data['hospitalized'],
                    data['icu'],
                    data['vent'],
                    data['released'],
                    data['deceased'],
                    data['source'],
                ]
            )
        except sqlite3.IntegrityError:
            print("Error: Data for this date has already been added")
        finally:
            conn.commit()
except Exception as e:
    print("Error: %s" % e)
    print(traceback.format_exc())
    sys.exit(1)
finally:
    conn.close()

if input_failures:
  sys.exit(1)
