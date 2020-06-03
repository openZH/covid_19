#!/bin/sh

DIR="$(cd "$(dirname "$0")" && pwd)"

for f in $DIR/../fallzahlen_kanton_total_csv_v2/*.csv;
do
    filename="$(basename "$f")"
    $DIR/add_new_columns.py $f > /tmp/columnfile 
    cat /tmp/columnfile > $DIR/../fallzahlen_kanton_total_csv_v2/$filename
done
