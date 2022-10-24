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
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
sleep 1
clear

if [ -f "$FILE_INIT" ]; then
  echo -e "\033[31;1mWarning\033[m: You initializtion has already been completed."
  while :
  do
    echo -ne "Are you sure to reinitialize? [y/N]"
    read -r input_comfirmation
    if [ "$input_comfirmation" == 'Y' ] || [ "$input_comfirmation" == 'y' ]; then
      echo "Yes"
      break
    elif [ "$input_comfirmation" == 'n' ] || [ "$input_comfirmation" == 'N' ] || [ -z "$input_comfirmation" ]; then
      echo "No"
      exit 0
    fi
  done
fi

echo -n > "$FILE_INIT"
echo "Tell me your name"
read -r input_name
echo -e "name\t$input_name" > "$FILE_INIT"
echo "Tell me your nearest station（e.g. 本郷三丁目）"
echo "Note: Don't add '駅' at the end"
read -r input_nearest_station
echo -e "nearest_station\t$input_nearest_station" >> "$FILE_INIT"

while :
do
  echo "Select the prefecture you live in:"
  echo "Note: Copy from below and paste"
  while read -r prefecture _
  do
    echo -ne "$prefecture\t"
  done < "jma_prefecture.dat"
  echo ""
  read -r input_prefecture
  if [ "$input_prefecture" == "東京都" ]; then
    break
  fi
  echo "I'm sorry but SYM is only for citizen of Tokyo."
done
echo -e "prefecture\t$input_prefecture" >> "$FILE_INIT"
echo "Select the nearest city from below:"
while read -r city _
do
  echo -ne "$city\t"
done < "amd_city_tokyo.dat"
echo ""
read -r input_city
echo -e "city\t$input_city" >> "$FILE_INIT"


