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
        match = re.search('^(\w+)\s+([\w\-\:]+)\s+([\w\-]+)\s+(\w+|-)\s+OK(.*)$', l)
        if not match:
            input_failures += 1
            print(f'Error: Not matched input line: {l}', file=sys.stderr)
            continue
        date_part = match.group(2).split('T')
        data = {
            'date': date_part[0],
            'time': '',
            'abbreviation_canton_and_fl': match.group(1),
            'ncumul_tested': '',
            'ncumul_conf': match.group(3),
            'new_hosp': '',
            'current_hosp': '',
            'current_icu': '',
            'current_vent': '',
            'ncumul_released': '',
            'ncumul_deceased': match.group(4),
            'source': '',
            'current_isolated': '',
            'current_quarantined': '',
        }

        if len(date_part) == 2:
            data['time'] = date_part[1]

        if data['ncumul_conf'] == '-':
            data['ncumul_conf'] = ''
        else:
            data['ncumul_conf'] = int(data['ncumul_conf'])

        if data['ncumul_deceased'] == '-':
            data['ncumul_deceased'] = ''
        else:
            data['ncumul_deceased'] = int(data['ncumul_deceased'])

        # Parse optional data.
        rest = match.group(5)
        extras_match = re.search('# Extras: ([^#]+)', rest)
        if extras_match:
            try:
                extras = extras_match.group(1).strip()
                extras = extras.split(',')
                extras = { kv.split('=', 2)[0]: int(kv.split('=', 2)[1]) for kv in extras }
                for key in extras:
                    data[key] = extras[key]
            except Exception as e:
                print(f'Error: Parsing optional data failed, ignoring: {extras_match.group(1)}', file=sys.stderr)

        # Parse URLs
        url_match = re.search('# URLs: ([^#]+)', rest)
        try:
            url_source = url_match.group(1).strip().split(', ')[-1]
        except (TypeError, IndexError):
            url_source = ''
        if url_source:
            data['source'] = url_source

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
                    new_hosp,
                    current_hosp,
                    current_icu,
                    current_vent,
                    ncumul_released,
                    ncumul_deceased,
                    source,
                    current_isolated,
                    current_quarantined
                )
                VALUES
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''',
                [
                    data['date'],
                    data['time'],
                    data['abbreviation_canton_and_fl'],
                    data['ncumul_tested'],
                    data['ncumul_conf'],
                    data['new_hosp'],
                    data['current_hosp'],
                    data['current_icu'],
                    data['current_vent'],
                    data['ncumul_released'],
                    data['ncumul_deceased'],
                    data['source'],
                    data['current_isolated'],
                    data['current_quarantined'],
                ]
            )
            print("Successfully added new entry.")
        except sqlite3.IntegrityError:
            if os.environ.get('SCRAPER_OVERWRITE') == 'no':
                print("Error: Data for this date has already been added", file=sys.stderr)
            else:
                try:
                    # keys that are updated
                    update_keys = [
                        'time',
                        'ncumul_tested',
                        'ncumul_conf',
                        'new_hosp',
                        'current_hosp',
                        'current_icu',
                        'current_vent',
                        'ncumul_released',
                        'ncumul_deceased',
                        'source',
                        'current_isolated',
                        'current_quarantined',
                        'ncumul_ICF', # GE only
                        'ncumul_confirmed_non_resident', # BS only
                        'hosp_non_resident', # BS only
                    ]
                    for key in update_keys:
                        # only update for non-empty values
                        # Note: `0` is a valid value
                        if key in data and data[key] is not None and data[key] != '':
                            c.execute(
                                f'UPDATE data SET {key} = ? WHERE date = ? AND abbreviation_canton_and_fl = ?;',
                                [data[key], data['date'], data['abbreviation_canton_and_fl']]
                            )
                            print(f"Successfully updated field '{key}' of {data['abbreviation_canton_and_fl']}: {data[key]} ({data['date']}).")
                except sqlite3.Error as e:
                    print("Error: an error occured in sqlite3: ", e.args[0], file=sys.stderr)
                    conn.rollback()
        finally:
            conn.commit()
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
finally:
    conn.close()

if input_failures:
    sys.exit(1)
