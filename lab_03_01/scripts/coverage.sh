#!/bin/bash

exit_code=$(pytest --cov=./src "$1" > buf.txt)
if [[ $exit_code -eq 1 ]] ; then
    exit_code=1
    echo "ERROR: Unit testing failed."
    cat buf.txt
else
    coverage=$(grep "TOTAL" buf.txt | awk '{print substr($NF, 1, length($NF)-1)}')
    echo "coverage: $coverage.00%"
fi
rm -f buf.txt
rm -f .coverage

exit $exit_code
