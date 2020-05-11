#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import matplotlib.pyplot as plt


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
#df_conf = df_conf.tail(30).reset_index(drop=True)
print(df_conf)

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

# use IQR*factor to get outliers
outliers = df_conf.query('(current_conf < (@q1 - @factor * @iqr)) or  (current_conf > (@q3 + @factor * @iqr))')
if outliers.empty:
    print('No outliers found.')
    sys.exit(0)
else:
    print("Outliers:")
    print(outliers)

if not df_conf.tail(1).query('(current_conf < (@q1 - @factor * @iqr)) or  (current_conf > (@q3 + @factor * @iqr))').empty:
    print("Last entry is an outlier, please check if this is an error")
    sys.exit(1)
