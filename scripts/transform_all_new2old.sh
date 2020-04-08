#!/bin/sh

DIR="$(cd "$(dirname "$0")" && pwd)"

for f in $DIR/../fallzahlen_kanton_total_csv_v2/*.csv;
do
    filename="$(basename "$f")"
    $DIR/new2oldcsv.py $f > $DIR/../fallzahlen_kanton_total_csv/$filename
done
