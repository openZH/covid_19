#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import matplotlib.pyplot as plt

# only values above this MIN_VALUE are considered outliers
# this is to prevent a failing scraper run if the absolute value is not very high
# this outlier detection is mostly to prevent human error (wrong data added)
MIN_VALUE = 20


# to use different styles, make sure to reload the default to always get clean results
# plt.style.available
def use_style(style):
    plt.style.use('default')
    plt.style.use(style)

assert len(sys.argv) == 2, "Error: Call this script with the path to a CSV file"

csv_file = sys.argv[1]

# load canton file from covid_19 repo
df = pd.read_csv(csv_file, parse_dates=[0])

# create new column for current cases
df_conf = df[['date', 'ncumul_conf']].reset_index(drop=True)
df_conf['current_conf'] = df['ncumul_conf'] - df['ncumul_conf'].shift(1)

# only use the last 30 rows
df_conf = df_conf.tail(30).reset_index(drop=True)

# generate boxplot
use_style('ggplot')
df_conf.boxplot(column='current_conf')
plt.savefig('boxplot.png')


# caculate iqr for confirmed cases
q1 = df_conf['current_conf'].quantile(0.25)
q3 = df_conf['current_conf'].quantile(0.75)
iqr = q3 - q1
factor = 1.5

print(f"IQR * {factor} = {iqr * factor}")

lower_limit = q1 - (iqr * factor)
upper_limit = q3 + (iqr * factor)

upper_limit = max(upper_limit, MIN_VALUE)
lower_limit = max(lower_limit, 0)

# use IQR*factor to get outliers
outliers = df_conf.query('(current_conf < @lower_limit) or (current_conf > @upper_limit)')
if outliers.empty:
    print('No outliers found.')
else:
    print("Outliers:")
    print(outliers)

if not df_conf.tail(1).query('(current_conf < @lower_limit) or (current_conf > @upper_limit)').empty:
    print("Last entry is an outlier, please check if this is an error")
    sys.exit(1)
