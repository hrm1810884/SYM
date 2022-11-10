#!/bin/bash

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

activate_selected=0

while :
do
  if [ $activate_selected -eq 0 ]; then
    echo "> Activate SYM"
    echo "  Initialize Setting"
  else
    echo "  Activate SYM"
    echo "> Initialize Setting"
  fi

  echo "Enter w/s to move upward/downward"

  read -r -n 1 input_key
  if [ "$input_key" == "w" ] || [ "$input_key" == "W" ]; then
    activate_selected=0
  elif [ "$input_key" == "s" ] || [ "$input_key" == "S" ]; then
    activate_selected=1
  elif [ "$input_key" == "" ]; then
    break
  fi
  clear
done

if [ $activate_selected -eq 0 ]; then
  bash exe/main.sh
else [ $activate_selected -eq 1 ]
  bash init/init.sh
fi
