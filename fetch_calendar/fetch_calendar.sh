#!/bin/bash

readonly calendar_information=$(python3 ./fetch_calendar.py)
IFS=";" ARR=($calendar_information)

for S in "${ARR[@]}"; do echo "$S"; done
