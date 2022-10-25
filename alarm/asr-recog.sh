#!/bin/bash

#padsp julius -C asr/grammar-mic.jconf | ./asr-output.pl
padsp julius -C alarm/asr/grammar-mic.jconf | ./alarm/asr-output.pl | python3 alarm/alarm.py
#padsp julius -C asr/grammar-mic.jconf
