#!/bin/sh

echo "| Canton | Confirmed cases | Deceased | Last update            |"
echo "|:------:| ---------------:| --------:|:---------------------- |"
#     |   BL   |             282 |        0 | 2020-03-21             |

# PER CANTON / FL

# 1    2    3                          4             5           6           7          8           9               10
# date,time,abbreviation_canton_and_fl,ncumul_tested,ncumul_conf,ncumul_hosp,ncumul_ICU,ncumul_vent,ncumul_released,ncumul_deceased,source

for f in *.csv; do
  # Output latest row with non-zero commulative number of cases (and deaths). Then sort by number of cases, and print the date.
  awk -F , '{if ($5) { printf("|   %2s   | %15d | %8d | %-21s  |\n", $3, $5, $10, $2 != "\"\"" ? $1 "T" $2 : $1); }}' "$f" | tail -1
done |  sort -r -n -k 4

# TOTAL

DATE=$(TZ="Europe/Zurich" date --iso-8601=minutes)

for f in *.csv; do
  # Output last row with non-zero commulative number of cases (and deaths)
  awk -F , '{if ($5) { print $1, $3, $5, $10; }}' "$f" | tail -1
  # The do sums.
done | awk "BEGIN { sum_cases = 0; sum_deceased = 0; } { sum_cases += \$3; sum_deceased += \$4; } END { printf(\"|  TOTAL | %15d | %8d | %-22s |\n\", sum_cases, sum_deceased, \"${DATE}\"); }"
