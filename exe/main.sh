#!/bin/bash

## dialogue directory ##
tmpdirname=/tmp/dialogue

# もしディレクトリが存在しなければ作成
if [ ! -e $tmpdirname ];then
  mkdir ${tmpdirname}
fi

while :
do
  # adinrec による録音
  filename=${tmpdirname}/input.wav
  padsp adinrec $filename > /dev/null
  
  # Ctrl-C で抜けるための処理
  if [ ! -e $filename ];then
    rmdir $tmpdirname
    exit;
  fi

  # 音声認識
  asrresult=${tmpdirname}/asrresult.txt
  echo $filename > ${tmpdirname}/list.txt

  # 音声認識をして結果をファイルに保存
  # もし前の状態を保存しておきたければ別変数/別ファイルを用意する
  padsp julius -C grammar/grammar.jconf -filelist ${tmpdirname}/list.txt 2> /dev/null | grep "^sentence1: " | sed -e 's/sentence1://' -e 's/silB//' -e 's/silE//' -e 's/ //g' > ${asrresult}
  rm ${tmpdirname}/list.txt	

  # 話者認識/音声認識結果を応答を生成する
  # 状態/履歴への依存性を持たせたければこのプログラムを適宜修正（引数変更等）
  # 初期では話者ID を元に異なる応答リストを読み込む仕様

  python3 exe/response.py $asrresult 
  
  # 事後処理
  rm $asrresult
done

# ここは実行されないはず
rmdir $tmpdirname
