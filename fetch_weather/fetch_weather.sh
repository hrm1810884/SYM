#!/bin/bash

readonly weather_information=$(python3 ./fetch_weather.py)
IFS=";" ARR=($weather_information)

for S in "${ARR[@]}"; do echo "$S"; done
