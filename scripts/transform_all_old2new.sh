#!/bin/sh

DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p $DIR/../fallzahlen_kanton_total_csv_v2

for f in $DIR/../fallzahlen_kanton_total_csv/*.csv;
do
    filename="$(basename "$f")"
    $DIR/old2newcsv.py $f > $DIR/../fallzahlen_kanton_total_csv_v2/$filename
done
