#!/bin/bash

readonly test1=$(python3 ./fetch_weather.py 123)
IFS=";" ARR=($test1)

for S in "${ARR[@]}"; do echo "$S"; done
