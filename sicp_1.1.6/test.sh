#!/bin/bash

set -e

TMP=`mktemp`
echo "Using tmp file $TMP"

for f in \
../sicp_1.1.1/text_1.1.1 \
../sicp_1.1.1/ex_1.1.1 \
../sicp_1.1.2/text_1.1.2 \
../sicp_1.1.2/ex_1.1.2 \
../sicp_1.1.3/text_1.1.3 \
../sicp_1.1.4/text_1.1.4 \
text_1.1.6 \
ex_1.3 \
ex_1.4 \
ex_1.4
do
    echo "Testing $f.in"
    ./scheme.py $f.in > "${TMP}"
    diff "${TMP}" $f.out
done

echo "All tests passed."
