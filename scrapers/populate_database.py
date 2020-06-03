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
    # load the csv to sqlite db
    assert len(sys.argv) == 2, "Call script with CSV file as parameter"
    filename = sys.argv[1]
    columns = []
    with open(filename,'r') as f:
        dr = csv.DictReader(f) 
        if not columns:
            columns = dr.fieldnames
        to_db = []
        for r in dr:
            db_row = []
            for col in columns:
                db_row.append(r[col])
            to_db.append(db_row)

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
            new_hosp integer,
            current_hosp integer,
            current_icu integer,
            current_vent integer,
            ncumul_released integer,
            ncumul_deceased integer,
            source text,
            current_isolated integer,
            current_quarantined integer,
            UNIQUE(date, abbreviation_canton_and_fl)
        )
        '''
    )
    # check if there are extra columns
    for col in columns[14:]:
        c.execute(f'ALTER TABLE data ADD COLUMN {col} integer;')

    # add entries
    query = 'INSERT INTO data (\n'
    query += ",\n".join(columns)
    query += ') VALUES ('
    query += ",".join(['?'] * len(columns))
    query += ');'
    c.executemany(query, to_db)
    conn.commit()
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
finally:
    conn.close()
