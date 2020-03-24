#!/bin/sh
set -e

# https://www.vd.ch/toutes-les-actualites/hotline-et-informations-sur-le-coronavirus/
# includes a content from datawrapper, which provides actual data and table rendering.

echo VD
B="https://datawrapper.dwcdn.net"
N="tr5bJ"
V=14
m=10 # max redirects
until [ -z $V ] ; do
    [[ $((m--)) -gt 0 ]] || exit 1
    R=$(curl --silent "$B/$N/$V/")
    V=$(echo $R | grep 'http-equiv=.REFRESH' | sed -E -e 's,^.*url=\.\./\.\./'$N'/([0-9]+)/.*$,\1,')
    # <html><head><meta http-equiv="REFRESH" content="0; url=../../tr5bJ/16/"></head></html>
done
d=$(echo $R | grep -A 4 render | grep -oE 'chartData:\s+"[^"]+"' | awk -F '"' '{print $2;}' | sed -E -e 's/\\n/\n/g' | sed -E -e 's/\\t/\t/g')
echo "Scraped at: $(date --iso-8601=seconds)"


# render({
#            visJSON: {"id":"tables","title":"Table","order":70,"dimensions":2,"namespace":"table","caption":"table","locale":{"show-more":"Afficher\u00a0$0 de plus","show-less":"Afficher moi
#            chartJSON: {"id":"tr5bJ","title":"Evolution des cas positifs au COVID-19","theme":"datawrapper-data","createdAt":"2020-03-20 11:14:49","lastModifiedAt":"2020-03-21 17:35:00","typ
#            chartData: "Date\tHospitalisations\tSortis de l'h\u00f4pital\tD\u00e9c\u00e8s\tTotal cas confirm\u00e9s\n10.03.2020\t26\t5\t1\t130\n11.03.2020\t39\t5\t2\t200\n12.03.2020\t43\t5\t3\t292\n13.03.2020\t39\t5\t2\t204\n14.03.2020\t43\t5\t3\t350\n15.03.2020\t62\t5\t4\t406\n16.03.2020\t66\t5\t5\t508\n17.03.2020\t95\t9\t5\t608\n18.03.2020\t117\t16\t5\t796\n19.03.2020\t140\t52\t7\t1210\n20.03.2020\t152\t62\t12\t1432",

# Date	Hospitalisations	Sortis de l'h\u00f4pital	D\u00e9c\u00e8s	Total cas confirm\u00e9s
# 10.03.2020	26	5	1	130
# 11.03.2020	39	5	2	200
# ...
# 18.03.2020	117	16	5	796
# 19.03.2020	140	52	7	1210
# 20.03.2020	152	62	12	1432


echo -n "Date and time: "
echo "$d" | tail -1 | awk '{print $1;}'

echo -n "Confirmed cases: "
echo "$d" | tail -1 | awk '{print $5;}'

echo -n "Deaths: "
echo "$d" | tail -1 | awk '{print $4;}'
