#!/usr/bin/env python3

# This script creates a new sqlite database based on the CSV is reiceives as an argument
# The sqlite database is used as an intermediate step to merge new data in existing CSVs

import sqlite3
import traceback
import os
import sys
import db_common as dc


__location__ = dc.get_location()

try:
    # load the csv to sqlite db
    assert len(sys.argv) == 2, "Call script with CSV file as parameter"
    columns, to_db = dc.load_csv(sys.argv[1])

    # create db
    DATABASE_NAME = os.path.join(__location__, 'data.sqlite')
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS data')
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS data (
            DistrictId integer NOT NULL,
            District text NOT NULL,
            Canton text NOT NULL,
            Date text NOT NULL,
            Week text NOT NULL,
            Year text NOT NULL,
            Population integer,
            TotalConfCases integer,
            NewConfCases integer,
            TotalDeaths integer,
            NewDeaths integer,
            SourceUrl text,
            UNIQUE(DistrictId, District, Canton, Date, Week, Year)
        )
        '''
    )

    # add entries
    query = dc.insert_db_query(columns)
    c.executemany(query, to_db)
    conn.commit()
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
finally:
    conn.close()
