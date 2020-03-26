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

try:
    DATABASE_NAME = os.path.join(__location__, 'data.sqlite')
    conn = sqlite3.connect(DATABASE_NAME)

    i = 0
    for line in sys.stdin:
        l = line.strip()
        match = re.search('^(\w+)\s+([\w\-\:]+)\s+(\w+)\s+((\w+|-))', l)
        date_part = match.group(2).split('T')
        data = {
            'date': date_part[0],
            'time': '',
            'area': os.environ['SCRAPER_KEY'],
            'tested': None,
            'confirmed': int(match.group(3)),
            'hospitalized': None,
            'icu': None,
            'vent': None,
            'released': None,
            'deceased': match.group(4),
            'source': os.environ['SCRAPER_SOURCE']
        }

        if len(date_part) == 2:
            data['time'] = date_part[1]

        if (data['deceased'] == '-'):
            data['deceased'] = None
        else:
            data['deceased'] = int(data['deceased'])


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
