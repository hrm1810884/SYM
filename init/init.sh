#!/bin/bash

FILE_INIT="./init/init.dat"

clear

# ファイルがある場合は本当に初期化するか確認する
if [ -f "$FILE_INIT" ]; then
  echo -e "\033[31;1mWarning\033[m: You initializtion has already been completed."
  while :
  do
    echo -ne "Are you sure to reinitialize? [y/N]"
    read -r input_comfirmation
    if [ "$input_comfirmation" == 'Y' ] || [ "$input_comfirmation" == 'y' ]; then
      break
    elif [ "$input_comfirmation" == 'n' ] || [ "$input_comfirmation" == 'N' ] || [ -z "$input_comfirmation" ]; then
      while :
      do
        echo -ne "start SYM? [y/N]"
        read -r input_comfirmation
        if [ "$input_comfirmation" == 'Y' ] || [ "$input_comfirmation" == 'y' ]; then
          sh exe/main.sh
          break
        elif [ "$input_comfirmation" == 'n' ] || [ "$input_comfirmation" == 'N' ] || [ -z "$input_comfirmation" ]; then
          exit 0
        fi
      done
    fi
  done
fi

# ファイルを作成"
echo -n > "$FILE_INIT"

# 名前を取得
echo "Tell me your name"
read -r input_name
echo -e "name $input_name" > "$FILE_INIT"

# 最寄り駅を取得
echo "Tell me your nearest station（e.g. 本郷三丁目）"
echo "Note: Don't add '駅' at the end"
read -r input_nearest_station
echo -e "nearest_station $input_nearest_station" >> "$FILE_INIT"

# 都道府県を取得
while : # 東京都って言わないと終了しない
do
  echo "Select the prefecture you live in:"
  echo "Note: Copy from below and paste"
  while read -r prefecture _
  do
    echo -ne "$prefecture\t"
  done < "./init/data/jma_prefecture.dat"
  echo ""
  read -r input_prefecture
  if [ "$input_prefecture" == "東京都" ]; then
    echo -e "prefecture $input_prefecture" >> "$FILE_INIT"
    break
  fi
  echo -e "I'm sorry but SYM is only for citizen of Tokyo.\n"
done

# 都市を取得
echo "Select the nearest city from below:"
while read -r city _
do
  echo -ne "$city\t"
done < "./init/data/amd_city_tokyo.dat"
echo ""
read -r input_city
echo -e "city $input_city" >> "$FILE_INIT"

echo "Thank you for letting me know about you!"
echo "Installing some modules...."
sleep 2
pip install -r ./init/requirements.txt
echo "all complete"
while :
do
  echo -ne "start SYM? [y/N]"
  read -r input_comfirmation
  if [ "$input_comfirmation" == 'Y' ] || [ "$input_comfirmation" == 'y' ]; then
    echo "Yes"
    sh exe/main.sh
    break
  elif [ "$input_comfirmation" == 'n' ] || [ "$input_comfirmation" == 'N' ] || [ -z "$input_comfirmation" ]; then
    echo "No"
    exit 0
  fi
done
