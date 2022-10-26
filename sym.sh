#!/bin/bash

FILE_INIT="./init.dat"

clear
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃                                 ┃"
echo -n "┃         "
echo -n -e "\033[1mWelcome to SYM\033[m"
echo -e "\033[0m          \033[m┃"
echo "┃                                 ┃"
echo "┃ Smarter than You in the Morning ┃"
echo "┃                                 ┃"
echo "┃    Press any key to continue    ┃"
echo "┃                                 ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"

stty -echo
read -r _
stty echo

clear

clear
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃                                 ┃"
echo -n "┃      "
echo -n -e "\033[1mChoose the function\033[m"
echo -e "\033[0m        \033[m┃"
echo "┃                                 ┃"
echo "┃      1. Initial Setting         ┃"
echo "┃      2. Get start SYM           ┃"
echo "┃        Press 1 or 2             ┃"
echo "┃                                 ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"

while :
do
  read -r chosen_num 
    if [ "$chosen_num" = "1" ]; then
      bash init/init.sh
      break
    elif [ "$chosen_num" = "2" ]; then
      sh exe/main.sh
      break
    else
      echo "Input 1 or 2 key"
  fi
done
