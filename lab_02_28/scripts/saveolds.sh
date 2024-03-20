#!/bin/bash

if [ -e "./report-unittesting-latest.txt" ]; then
    if [ -e "./report-unittesting-old.txt" ]; then 
        mv ./report-unittesting-old.txt ./report-unittesting-oldest.txt
    fi
    cat ./report-unittesting-latest.txt > ./report-unittesting-old.txt
fi
if [ -e "./report-functesting-latest.txt" ]; then
    if [ -e "./report-functesting-old.txt" ]; then 
        mv ./report-functesting-old.txt ./report-functesting-oldest.txt
    fi
    cat ./report-functesting-latest.txt > ./report-functesting-old.txt
fi
