#!/bin/bash

padsp julius -C alarm/asr/grammar-mic.jconf | ./alarm/asr-output.pl | python3 alarm/alarm.py
