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
        vd = sc.VaccinationData()
        if vd.parse(line.strip()):
            c = conn.cursor()
            try:
                print(vd)

                c.execute(
                    '''
                    INSERT INTO data (
                      canton,
                      start_date,
                      end_date,
                      week,
                      year,
                      doses_delivered,
                      first_doses,
                      second_doses,
                      total_vaccinations,
                      source
                    )
                    VALUES
                    (?,?,?,?,?,?,?,?,?,?)
                      ;

                    ''',
                    [
                        vd.canton,
                        vd.start_date or '',
                        vd.end_date or '',
                        vd.week or '',
                        vd.year or '',
                        vd.doses_delivered,
                        vd.first_doses,
                        vd.second_doses,
                        vd.total_vaccinations,
                        vd.url,
                    ]
                )

                print("Successfully added new entry.")
            except sqlite3.IntegrityError as e:
                # try UPDATE if INSERT didn't work (i.e. constraint violation)
                try:
                    c.execute(
                        '''
                        UPDATE data SET
                          doses_delivered = ?,
                          first_doses = ?,
                          second_doses = ?,
                          total_vaccinations = ?,
                          source = ?
                        WHERE canton = ?
                        AND   start_date = ?
                        AND   end_date = ?
                        AND   week = ?
                        AND   year = ?
                        ;
                        ''',
                        [
                            vd.doses_delivered,
                            vd.first_doses,
                            vd.second_doses,
                            vd.total_vaccinations,
                            vd.url,

                            vd.canton,
                            vd.start_date or '',
                            vd.end_date or '',
                            vd.week or '',
                            vd.year or '',
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
