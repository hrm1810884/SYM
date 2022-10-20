#!/bin/bash

#padsp julius -C asr/grammar-mic.jconf | ./asr-output.pl
padsp julius -C asr/grammar-mic.jconf | ./asr-output.pl | python3 alarm.py
#padsp julius -C asr/grammar-mic.jconf
