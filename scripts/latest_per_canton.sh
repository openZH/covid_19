#!/bin/sh

echo "| Canton | Confirmed cases | Last update             |"
echo "|:------:| ---------------:|:----------------------- |"
#     |   BL   |             282 | 2020-03-21              |

# PER CANTON / FL

for f in *.csv; do
  # Output latest row with non-zero commulative number of cases. Then sort by number of cases, and print the date.
  awk -F , '{if ($5) { printf("|   %2s   | %15d | %-22s  |\n", $3, $5, $1); }}' "$f" | tail -1
done |  sort -r -n -k 4

# TOTAL

DATE=$(TZ="Europe/Zurich" date --iso-8601=minutes)

for f in *.csv; do
  # Output last row with non-zero commulative number of cases
  awk -F , '{if ($5) { print $1, $3, $5; }}' "$f" | tail -1
done | awk "BEGIN { sum = 0; } { sum += \$3; } END { printf(\"|  TOTAL | %15d | %10s  |\n\", sum, \"${DATE}\"); }"
