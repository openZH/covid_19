#!/bin/sh

# uses csval npm package
# To install:
#    npm install -g csval
 
for f in $(ls *.csv) 
do 
    echo "checking $f"
    csval $f || exit 1
done
