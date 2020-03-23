#!/bin/sh
set -e

echo SH
d=$(./download.sh "https://sh.ch/CMS/content.jsp?contentid=3209198&language=DE&_=1584807070095" | grep data_post_content | sed -E -e 's/\\n/\n/g')
echo "Scraped at: $(date --iso-8601=seconds)"

echo -n "Date and time: "
echo "$d" | grep "Im Kanton Schaffhausen gibt es" | sed -E -e 's/^.*\(([0-9.]+)\).*$/\1/'

echo -n "Confirmed cases: "
echo "$d" | grep "best&auml;tige" | sed -E -e 's/^.*strong>([0-9]+)[^0-9]*$/\1/'
