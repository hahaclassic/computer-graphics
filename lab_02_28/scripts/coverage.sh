#!/bin/bash

exit_code=0
if ! pytest --cov=./src "$1" > buf.txt; then
    exit_code=1
    echo "ERROR: Unit testing failed."
    cat buf.txt
else
    coverage=$(grep "TOTAL" buf.txt | awk '{print substr($NF, 1, length($NF)-1)}')
    echo "coverage: $coverage.00%"
fi
rm buf.txt
rm .coverage

exit "$exit_code"
