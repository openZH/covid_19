#!/usr/bin/env python3

# This script creates a new sqlite database based on the CSV is reiceives as an argument
# The sqlite database is used as an intermediate step to merge new data in existing CSVs

import sqlite3
import csv
import traceback
import os
import sys


__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)

try:
    # create db
    DATABASE_NAME = os.path.join(__location__, 'data.sqlite')
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS data')
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS data (
            date text,
            time text,
            abbreviation_canton_and_fl text,
            ncumul_tested  integer,
            ncumul_conf integer,
            ncumul_hosp integer,
            ncumul_ICU integer,
            ncumul_vent integer,
            ncumul_released integer,
            ncumul_deceased integer,
            source text,
            UNIQUE(date, abbreviation_canton_and_fl)
        )
        '''
    )

    # load the csv to sqlite db
    assert len(sys.argv) == 2, "Call script with CSV file as parameter"
    filename = sys.argv[1]
    with open(filename,'r') as f:
            dr = csv.DictReader(f) 
            to_db = []
            for r in dr:
                db_row = [
                    r['date'],
                    r['time'],
                    r['abbreviation_canton_and_fl'],
                    r['ncumul_tested'],
                    r['ncumul_conf'],
                    r['ncumul_hosp'],
                    r['ncumul_ICU'],
                    r['ncumul_vent'],
                    r['ncumul_released'],
                    r['ncumul_deceased'],
                    r['source']
                ]
                to_db.append(db_row)
    c.executemany(
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
        to_db
    )
    conn.commit()
except Exception as e:
    print("Error: %s" % e)
    print(traceback.format_exc())
    sys.exit(1)
finally:
    conn.close()
