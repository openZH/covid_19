#!/bin/sh

for f in *.csv; do
  # Output last row with non-zero commulative number of cases
  awk -F , '{if ($5) { print $1, $3, $5; }}' "$f" | tail -1
done | awk 'BEGIN { sum = 0; } { sum += $3; } END { print sum; }'
