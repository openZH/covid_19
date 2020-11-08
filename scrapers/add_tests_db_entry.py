#!/usr/bin/env python3

import sys
import sqlite3
import traceback
import os

import db_common as dc
import scrape_common as sc

__location__ = dc.get_location()

input_failures = 0

try:
    DATABASE_NAME = os.path.join(__location__, 'data.sqlite')
    conn = sqlite3.connect(DATABASE_NAME)

    i = 0
    for line in sys.stdin:
        td = sc.TestData()
        if td.parse(line.strip()):
            c = conn.cursor()
            try:
                print(td)

                c.execute(
                    '''
                    INSERT INTO data (
                      canton,
                      start_date,
                      end_date,
                      week,
                      year,
                      positive_tests,
                      negative_tests,
                      total_tests,
                      positivity_rate,
                      url
                    )
                    VALUES
                    (?,?,?,?,?,?,?,?,?,?)
                      ;

                    ''',
                    [
                        td.canton,
                        td.start_date or '',
                        td.end_date or '',
                        td.week or '',
                        td.year or '',
                        td.positive_tests,
                        td.negative_tests,
                        td.total_tests,
                        td.positivity_rate,
                        td.url,
                    ]
                )

                print("Successfully added new entry.")
            except sqlite3.IntegrityError as e:
                # try UPDATE if INSERT didn't work (i.e. constraint violation)
                try:
                    c.execute(
                        '''
                        UPDATE data SET
                          positive_tests = ?,
                          negative_tests = ?,
                          total_tests = ?,
                          positivity_rate = ?,
                          url = ?
                        WHERE canton = ?
                        AND   start_date = ?
                        AND   end_date = ?
                        AND   week = ?
                        AND   year = ?
                        ;
                        ''',
                        [
                            td.positive_tests,
                            td.negative_tests,
                            td.total_tests,
                            td.positivity_rate,
                            td.url,

                            td.canton,
                            td.start_date or '',
                            td.end_date or '',
                            td.week or '',
                            td.year or '',
                        ]
                    )
                    print("Successfully updated entry.")
                except sqlite3.Error as e:
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
