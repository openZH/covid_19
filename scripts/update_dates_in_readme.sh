#!/bin/bash

DIR="$(cd "$(dirname "$0")" && pwd)"

today=$(date +%s)

areas="FL AG AI AR BE BL BS FR GE GL GR JU LU NE NW OW SG SH SO SZ TG TI UR VD VS ZG ZH"
for area in $areas
do
    update_date_str=`grep $area $DIR/../COVID19_Fallzahlen_CH_total_v2.csv | tail -n 1 | awk -F, '{print $1}'`
    update_date=$(date --date="$update_date_str" +%s)
    diff=$(($today-$update_date))

    if [ $diff -lt 84000 ]; then
        color='4d9221'
    elif [ $diff -lt 144000 ]; then
        color='b8e186'
    else
        color='de77ae'
    fi
    sed -i -e "/\[$area\]/s#update on [^|]*|#update on $update_date_str](https://placehold.jp/$color/000000/200x50.png?text=$update_date_str 'Last update on $update_date_str')|#" $DIR/../README.md
    echo "Update README for ${area} (date: ${update_date_str}, color: ${color})"
done
