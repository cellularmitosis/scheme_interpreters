#!/bin/bash

set -e

TMP=`mktemp`
echo "Using tmp file $TMP"

for f in text_1.1.1 ex_1.1.1
do
    echo "Testing $f.in"
    ./scheme.py $f.in > "${TMP}"
    diff "${TMP}" $f.out
done
