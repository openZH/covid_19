#!/usr/bin/env python3

import sys

# This file contains expectations of what data is provided by each scraper.
# It is used by the parser to verify no expected field is missing,
# which would indicate broken parser, or change to a website.
#
# It is to track and detect regressions.

# A per-canton list of extra fields that are expected to be present.
# Number of confirmed cases is always required to be present,
# and is not listed in this list.
matrix = {
    # Note: Please keep the order of cantons and entries.
    'AG': ['Confirmed', 'Deaths', 'Released', 'Hospitalized', 'ICU', 'Vent'],
    'AI': ['Confirmed'],
    'AR': ['Confirmed', 'Deaths'],
    'BE': ['Confirmed', 'Deaths', 'Hospitalized', 'ICU', 'Vent'],
    'BL': ['Confirmed', 'Deaths', 'Released', 'Hospitalized', 'ICU'],
    'BS': ['Confirmed', 'Deaths', 'Released', 'Hospitalized', 'ICU'],
    'FR': ['Confirmed', 'Deaths', 'Released', 'Hospitalized', 'ICU'],
    'GE': ['Confirmed', 'Deaths', 'Hospitalized', 'ICU'],
    'GL': ['Confirmed', 'Deaths', 'Hospitalized'],
    'GR': ['Confirmed', 'Deaths', 'Hospitalized'],
    'JU': ['Confirmed', 'Deaths', 'Hospitalized', 'ICU'],
    'LU': ['Confirmed', 'Deaths', 'Hospitalized', 'ICU'],
    'NE': ['Deaths', 'Hospitalized', 'ICU', 'Vent'],
    'NW': ['Confirmed', 'Deaths', 'Hospitalized', 'ICU'],
    'OW': ['Confirmed', 'Deaths', 'Hospitalized'],
    'SG': ['Confirmed', 'Deaths', 'Released', 'Hospitalized', 'ICU'],
    'SH': ['Confirmed', 'Deaths', 'Hospitalized', 'ICU'],
    'SO': ['Confirmed', 'Deaths', 'Hospitalized'],
    'SZ': ['Confirmed', 'Deaths', 'Released'],
    'TG': ['Confirmed', 'Deaths', 'Hospitalized', 'ICU'],
    'TI': ['Confirmed', 'Deaths', 'Released', 'Hospitalized', 'ICU', 'Vent'],
    'UR': ['Confirmed', 'Deaths', 'Released', 'Hospitalized'],
    'VD': ['Confirmed', 'Deaths', 'Hospitalized', 'ICU'],
    'VS': ['Confirmed', 'Deaths', 'Released', 'Hospitalized', 'ICU', 'Vent'],
    'ZG': ['Confirmed', 'Deaths', 'Released', 'Hospitalized', 'ICU'],
    'ZH': ['Confirmed', 'Deaths', 'Hospitalized', 'Vent'],
    # 'FL': [],  # No scraper.
}

allowed_extras = ['Confirmed', 'Deaths', 'Released', 'Hospitalized', 'ICU', 'Vent']

# List of cantons that are expected to have date AND time.
matrix_time = [
    'AG',
    'AI',
    'AR',
    'BE',
    # 'BL',  # Not available.
    'BS',
    # 'FR',  # Not available.
    'GE',
    'GL',
    # 'GR',  # Not available.
    'JU',
    'LU',
    'NW',
    # 'NE',  # Not easily available.
    'OW',
    # 'SG',  # Not available.
    'SH',
    'SO',
    'SZ',
    # 'TG',  # Not available.
    'TI',
    'UR',
    # 'VD',  # Not available.
    'VS',
    'ZG',
    'ZH',
    # 'FL',  # No scraper.
]


def check_expected(abbr, date, deaths, extras):
    """
    Verify that canton `abbr` has expected numbers presents.
    If not, return a non-empty list of expectation violations back to the caller.
    """
    expected_extras = matrix[abbr]

    for k in expected_extras:
        if k not in allowed_extras:
            print(f'WARNING: Unknown extra {k} present (typo?) in expectation matrix[{abbr}]', file=sys.stderr)

    violated_expectations = []

    cross = {
        'Deaths': deaths,
        'Confirmed': extras.get('ncumul_conf'),
        'Hospitalized': extras.get('ncumul_hosp'),
        'ICU': extras.get('ncumul_ICU'),
        'Vent': extras.get('ncumul_vent'),
        'Released': extras.get('ncumul_released'),
    }

    # Check for fields that should be there, but aren't
    for k, v in cross.items():
        if v is None and k in expected_extras:
            violated_expectations.append(f'Expected {k} to be present for {abbr}')

    # Check for new fields, that are there, but we didn't expect them
    for k, v in cross.items():
        if v is not None and k not in expected_extras:
            violated_expectations.append(f'Not expected {k} to be present for {abbr}. Update scrape_matrix.py file.')

    assert "T" in date
    date_time = date.split("T", 1)
    assert len(date_time[0]) == 10
    if abbr in matrix_time:
        if len(date_time[1]) != 5:
            violated_expectations.append(f'Expected time of a day to be present for {abbr}. Found none.')
    else:
        if len(date_time[1]) != 0:
            violated_expectations.append(
                f'Not expected time of a day to be present for {abbr}. Found "{date_time[1]}". Update scrape_matrix.py file?')

    return violated_expectations
