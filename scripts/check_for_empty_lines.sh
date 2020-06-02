#!/bin/bash

path="$*"
output=$(grep --line-number --with-filename '^\s*$' $path)
grep_exit=$?

if [ $grep_exit -eq 0 ] ; then
    echo "× Found empty lines in the following files/line number:"
    echo $output
    exit 1
else
    echo "✓ No empty lines found"
    exit 0
fi

