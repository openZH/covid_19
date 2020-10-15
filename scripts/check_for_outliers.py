#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import pandas as pd

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)

# only values above this MIN_VALUE are considered outliers
# this is to prevent a failing scraper run if the absolute value is not very high
# this outlier detection is mostly to prevent human error (wrong data added)
MIN_VALUE = 20

# only check the last x days
LAG_PERIODS = 10

# periods considered "recent"
RECENT_PERIODS = 5

# IQR factor, determines how many times the IQR is the limit for an outlier
FACTOR = 2.0

assert len(sys.argv) >= 2, "Error: Call this script with the path(s) to CSV file(s)"

fail = False

args = sys.argv[1:]
for csv_file in args:

    # load canton file from covid_19 repo
    df = pd.read_csv(csv_file, parse_dates=[0])
    df_ignore = pd.read_csv(os.path.join(__location__, '..', 'outlier_status.csv'), parse_dates=[0])
    df = pd.merge(df, df_ignore, left_on=['date', 'abbreviation_canton_and_fl'], right_on=['date', 'abbreviation_canton_and_fl'], how='left')

    # create new column for current cases
    df_conf = df[['date', 'ncumul_conf', 'ncumul_conf_outlier']].reset_index(drop=True)
    df_conf['current_conf'] = df['ncumul_conf'] - df['ncumul_conf'].shift(1)

    # only use the last 30 rows
    df_conf = df_conf.tail(LAG_PERIODS).reset_index(drop=True)

    # caculate iqr for confirmed cases
    q1 = df_conf['current_conf'].quantile(0.25)
    q3 = df_conf['current_conf'].quantile(0.75)
    iqr = q3 - q1

    lower_limit = q1 - (iqr * FACTOR)
    upper_limit = q3 + (iqr * FACTOR)

    upper_limit = max(upper_limit, MIN_VALUE)
    lower_limit = 0 # always use 0 as lower limit
    df_conf['q1'] = q1
    df_conf['q3'] = q3
    df_conf['iqr'] = iqr
    df_conf['factor'] = FACTOR
    df_conf['upper_limit'] = upper_limit
    df_conf['lower_limit'] = lower_limit

    # use IQR*factor to get outliers
    outliers = df_conf.query('(current_conf < @lower_limit) or (current_conf > @upper_limit)')
    recent_outliers = df_conf.tail(RECENT_PERIODS).query("((current_conf < @lower_limit) or (current_conf > @upper_limit)) and (ncumul_conf_outlier != 'ignore')")
    if outliers.empty:
        print(f"✅ {csv_file} has no outliers.");
    else:
        if not recent_outliers.empty:
            fail = True
            print(f"❌ {csv_file} has recent outliers, please check if this is an error.");
        else:
            print(f"⚠️ {csv_file} has older or ignored outliers.");
        print(outliers[['date', 'ncumul_conf', 'current_conf', 'iqr', 'factor', 'upper_limit']])
        print('')

if fail:
    sys.exit(1)

