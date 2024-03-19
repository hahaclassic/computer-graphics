#!/bin/bash
pytest --cov=./src > buf.txt
coverage=$(grep "TOTAL" buf.txt | awk '{print substr($NF, 1, length($NF)-1)}')
echo "coverage: $coverage.0 %"
rm buf.txt
rm .coverage
