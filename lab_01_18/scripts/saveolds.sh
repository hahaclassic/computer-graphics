#!/bin/bash
if [ -e "./report-unittesting-old.txt" ]; then 
    mv ./report-unittesting-old.txt ./report-unittesting-oldest.txt
fi
cat ./report-unittesting-latest.txt > ./report-unittesting-old.txt
