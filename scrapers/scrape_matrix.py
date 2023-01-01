#!/usr/bin/env python3

import sys

# This file contains expectations of what data is provided by each scraper.
# It is used by the parser to verify no expected field is missing,
# which would indicate broken parser, or change to a website.
#
# It is to track and detect regressions.

# A per-canton list of extra fields that are expected to be present.
matrix = {
    # Note: Please keep the order of cantons and entries.
    'AG': [], # AG does not always provide the same numbers
    'AI': ['Confirmed cases', 'Deaths'],
    'AR': [], # TODO: AR removed the cases data on 2021-01-23
    'BE': [], # BE does not always provide the same numbers
    'BL': [], # BL does not always provide the same numbers
    'BS': ['Confirmed cases', 'Deaths', 'Released'],
    'FR': ['Confirmed cases', 'Deaths'],
    'GE': [], # GE does not always provide the same numbers
    'GL': ['Confirmed cases', 'Deaths', 'Hospitalized'],
    'GR': ['Confirmed cases', 'Deaths', 'Hospitalized'],
    'JU': ['Deaths', 'Hospitalized'],
    'LU': [], # LU does not always provide the same numbers 
    'NE': [], # NE does not always provide the same numbers
    'NW': ['Confirmed cases', 'Deaths', 'Hospitalized', 'ICU'],
    'OW': [], # TODO: on 2020-12-22 OW did only provide hospitalisations, check again later
    'SG': ['Confirmed cases', 'Deaths'],
    'SH': ['Confirmed cases', 'Deaths'],
    'SO': ['Confirmed cases'],
    'SZ': ['Confirmed cases', 'Deaths', 'Released'],
    'TG': ['Confirmed cases', 'Deaths', 'Released', 'Hospitalized', 'ICU'],
    'TI': ['Confirmed cases', 'Deaths', 'Hospitalized', 'ICU'],
    'UR': ['Confirmed cases', 'Deaths', 'Hospitalized'],
    'VD': ['Confirmed cases', 'Deaths', 'Hospitalized', 'ICU',],
    'VS': ['Confirmed cases', 'Deaths'],
    'ZG': ['Confirmed cases'],
    'ZH': ['Confirmed cases', 'Deaths', 'Hospitalized'],
    'FL': ['Confirmed cases'],
}

allowed_extras = ['Confirmed cases', 'Deaths', 'Released', 'Hospitalized', 'ICU', 'Vent', 'Isolated', 'Quarantined']

# List of cantons that are expected to have date AND time.
matrix_time = [
    'AI',
    'AG',
    # 'AR',  # Not available anymore.
    # 'BE',  # Not available.
    # 'BL',  # Not available.
    'BS',
    # 'FR',  # Not available.
    # 'GE',  # Not available.
    # 'GL',  # Not available.
    # 'GR',  # Not available.
    # 'JU',  # Not available in xls
    # 'LU',  # Available, but different values are reported at differnt times
    # 'NW',  # Not available in xls
    # 'NE',  # Not easily available.
    'OW',
    # 'SG',  # Not available.
    # 'SH',  # Sometimes available
    # 'SO',
    'SZ',
    'TG',
    # 'TI',  # Not available
    'UR',
    # 'VD',  # Not available.
    # 'VS',  # Not available
    'ZG',
    'ZH',
    # 'FL',  # Not available
]


def check_expected(abbr, date, data):
    """
    Verify that canton `abbr` has expected numbers presents.
    If not, return a non-empty list of expectation violations back to the caller.
    """
    expected_extras = matrix[abbr]
    violated_expectations = []
    warnings = []

    for k in expected_extras:
        if k not in allowed_extras:
            text = f'Unknown extra {k} present (typo?) in expectation matrix[{abbr}]'
            print(f'WARNING: {text}', file=sys.stderr)
            warnings.append(text)

    cross = {
        'Confirmed cases': data.get('ncumul_conf'),
        'Deaths': data.get('ncumul_deceased'),
        'Hospitalized': data.get('current_hosp'),
        'ICU': data.get('current_icu'),
        'Vent': data.get('current_vent'),
        'Released': data.get('ncumul_released'),
        'Isolated': data.get('current_isolated'),
        'Quarantined': data.get('current_quarantined'),
    }

    # Check for fields that should be there, but aren't
    for k, v in cross.items():
        if v is None and k in expected_extras:
            violated_expectations.append(f'Expected {k} to be present for {abbr}')

    # Check for new fields, that are there, but we didn't expect them
    # for k, v in cross.items():
    #     if v is not None and k not in expected_extras:
    #         text = f'Not expected {k} to be present for {abbr}. Update scrape_matrix.py file.'
    #         print(f'WARNING: {text}', file=sys.stderr)
    #         warnings.append(text)

    assert date and "T" in date, f'Date is invalid: {date}'
    date_time = date.split("T", 1)
    assert len(date_time[0]) == 10
    if abbr in matrix_time:
        if len(date_time[1]) != 5:
            violated_expectations.append(f'Expected time of a day to be present for {abbr}. Found none.')
    else:
        if len(date_time[1]) != 0:
            text = f'Not expected time of a day to be present for {abbr}. Found "{date_time[1]}". Update scrape_matrix.py file?'
            print(f'WARNING: {text}', file=sys.stderr)
            warnings.append(text)

    return (violated_expectations, warnings)
