#!/usr/bin/env python3

import scrape_common as sc

print('NE')

d = sc.pdfdownload('https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Documents/Covid-19-Statistiques/COVID19_PublicationInternet.pdf', layout=True)
sc.timestamp()

# Heavily inspired by code by https://github.com/maekke97

import re

# Magic column fix (don't know if this is stable).
d = re.sub(r'avr\n? *i\n? *l', 'avril', d, flags=re.I)

# Find the start of the table on page 5.
d = d[d.find('1mars2020'):]

# d  # Example rows.
"""
18mars2020                       32                146                15                     3                                                           18                     3                                                                                       3              1                      2
19mars2020                       29                175                16                     3                                                           19                     3                                                                                       3              1                      3
20mars2020                       13                188                17                     4                                                           21                     4                                                              2                        6                                     3
21mars2020                       12                200                15                     5                                                           20                     5                                                              1                        6              1                      4
22mars2020                       16                216                22                     6                                                           28                     6                                                              1                        7                                     4
23mars2020                       31                247                22                                            5                   6                33                                          5                     6                   0                       11              1                      5
24mars2020                       18                265                24                                            2                   6                32                                          2                     6                   3                       11              1                      6
25mars2020                       15                280                31                                            3                   7                41                                          3                     7                   2                       12              3                      9
26mars2020                       19                299                33                                            2                   7                42                                          2                     7                   1                       10              2                     11
1avril2020                        18                420                52                                            6                   8                66                                          6                     8                   4                       18              2                     23
2avril2020                        10                430                49                                            2                  10                61                                          2                    10                   4                       16              3                     26
3avril2020                        14                444                50                                            2                   9                61                                          2                     9                   3                       14                                    26
4avril2020                         7                451                49                                            1                   9                59                                          1                     9                   4                       14              1                     27
5avril2020                        11                462                46                                            4                   8                58                                          4                     8                   5                       17                                    27
6avril2020                         4                466                49                                            2                   8                59                                          2                     8                   4                       14              1                     28
7avril2020                                                             56                                            5                   5                66                                          5                     5                   7                       17                                    28
"""

# Replace strategic spans of spaces by colon to indicate columns.
d = d.replace('2020                      ', '2020:')
d = d.replace('                    ', ':')
d = d.replace('              ', ':')

# d  # Example rows.
"""
18mars2020: 32:  146:  15: 3:::     18: 3::::       3:1:  2
19mars2020: 29:  175:  16: 3:::     19: 3::::       3:1:  3
20mars2020: 13:  188:  17: 4:::     21: 4:::  2:    6::   3
21mars2020: 12:  200:  15: 5:::     20: 5:::  1:    6:1:  4
22mars2020: 16:  216:  22: 6:::     28: 6:::  1:    7::   4
23mars2020: 31:  247:  22::    5:     6:  33::  5: 6:     0:   11:1:  5
24mars2020: 18:  265:  24::    2:     6:  32::  2: 6:     3:   11:1:  6
25mars2020: 15:  280:  31::    3:     7:  41::  3: 7:     2:   12:3:  9
26mars2020: 19:  299:  33::    2:     7:  42::  2: 7:     1:   10:2: 11
1avril2020:  18:  420:  52::    6:     8:  66::  6: 8:     4:   18:2: 23
2avril2020:  10:  430:  49::    2:    10:  61::  2:10:     4:   16:3: 26
3avril2020:  14:  444:  50::    2:     9:  61::  2: 9:     3:   14::  26
4avril2020:   7:  451:  49::    1:     9:  59::  1: 9:     4:   14:1: 27
5avril2020:  11:  462:  46::    4:     8:  58::  4: 8:     5:   17::  27
6avril2020:   4:  466:  49::    2:     8:  59::  2: 8:     4:   14:1: 28
7avril2020:::     56::    5:     5:  66::  5: 5:     7:   17::  28
"""

# Split all lines into rows (by new line) and columns (by colon), and
# strip any adjacent spaces.

data = [[dat.strip() for dat in line.split(':')] for line in d.split('\n')]

COLUMNS = [
    'date',
    'ncases_per_day',
    'ncumul_cases',
    'n_hospital_non_icu',
    'n_hospital_icu',
    'n_hospital_icu_non_tube',
    'n_hospital_icu_tube',
    'n_hospital_total',
    'n_icu_covid',
    'n_icu_non_tube',
    'n_icu_tube',
    'n_icu_non_covid',
    'n_icu_total',
    'n_deceased',
    'ncumul_deceased'
]

# Take last non-empty row with non-empty confirmed cases values.
last_row = []
while len(data):
  last_row = data[-1]
  data = data[:-1]  # Chop the last row off.
  if (len(last_row) >= COLUMNS.index('ncumul_cases') + 1) \
     and last_row[COLUMNS.index('ncumul_cases')]:
    break

def get_column(name):
  if COLUMNS.index(name) < len(last_row):
    return last_row[COLUMNS.index(name)] or 'None'
  return None

def get_column_int(name):
  if COLUMNS.index(name) < len(last_row):
    return int(last_row[COLUMNS.index(name)] or '0')
  return 0

print('Date and time:', get_column('date'))

print('Confirmed cases:', get_column('ncumul_cases'))

# These are hospitalized positive cases.
print('Hospitalized:', get_column('n_hospital_total'))

# Not that this includes also non-COVID related patients.
# print('ICU:', last_row[COLUMNS.index('n_icu_total')] or 'None')
# To just get COVID related intubations use `max(n_icu_covid, n_icu_non_tube + n_icu_tube)`,
# or `n_icu_total - n_icu_non_covid`.
print('ICU:', max(get_column_int('n_icu_covid'),
                  get_column_int('n_icu_non_tube') + get_column_int('n_icu_tube')))

# Intubated.
print('Vent:', get_column('n_hospital_icu_tube'))

print('Deaths:', get_column('ncumul_deceased'))
