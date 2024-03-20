#!/bin/bash
pytest --cov=./src "$1" > buf.txt
coverage=$(grep "TOTAL" buf.txt | awk '{print substr($NF, 1, length($NF)-1)}')
echo "coverage: $coverage.00%"
rm buf.txt
rm .coverage
