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
                      pcr_positive_tests,
                      pcr_negative_tests,
                      pcr_total_tests,
                      pcr_positivity_rate,
                      ag_positive_tests,
                      ag_negative_tests,
                      ag_total_tests,
                      ag_positivity_rate,
                      positive_tests,
                      negative_tests,
                      total_tests,
                      positivity_rate,
                      source
                    )
                    VALUES
                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                      ;

                    ''',
                    [
                        td.canton,
                        td.start_date or '',
                        td.end_date or '',
                        td.week or '',
                        td.year or '',
                        td.pcr_positive_tests,
                        td.pcr_negative_tests,
                        td.pcr_total_tests,
                        td.pcr_positivity_rate,
                        td.ag_positive_tests,
                        td.ag_negative_tests,
                        td.ag_total_tests,
                        td.ag_positivity_rate,
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
                          pcr_positive_tests = ?,
                          pcr_negative_tests = ?,
                          pcr_total_tests = ?,
                          pcr_positivity_rate = ?,
                          ag_positive_tests = ?,
                          ag_negative_tests = ?,
                          ag_total_tests = ?,
                          ag_positivity_rate = ?,
                          positive_tests = ?,
                          negative_tests = ?,
                          total_tests = ?,
                          positivity_rate = ?,
                          source = ?
                        WHERE canton = ?
                        AND   start_date = ?
                        AND   end_date = ?
                        AND   week = ?
                        AND   year = ?
                        ;
                        ''',
                        [
                            td.pcr_positive_tests,
                            td.pcr_negative_tests,
                            td.pcr_total_tests,
                            td.pcr_positivity_rate,
                            td.ag_positive_tests,
                            td.ag_negative_tests,
                            td.ag_total_tests,
                            td.ag_positivity_rate,
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
