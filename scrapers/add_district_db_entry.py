#!/usr/bin/env python3

import sys
import sqlite3
import traceback
import os

import scrape_common as sc

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
        dd = sc.DistrictData()
        if dd.parse(line.strip()):
            c = conn.cursor()
            try:
                print(dd)

                c.execute(
                    '''
                    INSERT INTO data (
                      DistrictId,
                      District,
                      Canton,
                      Date,
                      Week,
                      Year,
                      Population,
                      TotalConfCases,
                      NewConfCases,
                      TotalDeaths,
                      NewDeaths,
                      SourceUrl
                    )
                    VALUES
                    (?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT (DistrictId, District, Canton, Date, Week, Year)
                    DO UPDATE SET
                      Population = ?,
                      TotalConfCases = ?,
                      NewConfCases = ?,
                      TotalDeaths = ?,
                      NewDeaths = ?,
                      SourceUrl = ?
                      ;

                    ''',
                    [
                        # insert
                        dd.district_id,
                        dd.district,
                        dd.canton,
                        dd.date or '',
                        dd.week or '',
                        dd.year or '',
                        dd.population,
                        dd.total_cases,
                        dd.new_cases,
                        dd.total_deceased,
                        dd.new_deceased,
                        dd.url,

                        # update
                        dd.population,
                        dd.total_cases,
                        dd.new_cases,
                        dd.total_deceased,
                        dd.new_deceased,
                        dd.url
                    ]
                )

                print("Successfully added/updated entry.")
            except sqlite3.IntegrityError as e:
                print("Error: an error occured in sqlite3: ", e.args[0], file=sys.stderr)
                conn.rollback()
                input_failures += 1
            finally:
                conn.commit()
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
finally:
    conn.close()

if input_failures:
    print(f'input_failures: {input_failures}')
    sys.exit(1)
