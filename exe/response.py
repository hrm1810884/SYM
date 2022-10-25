#!/usr/bin/env python3
# coding: utf-8
#
# 応答生成モジュール
# 基本的には
# - 入力と応答の対応リスト(argv[1])
# - 話者認識結果ID (argv[2])
# - 音声認識結果 (argv[3])
# を受け取って応答文および音声を生成する
#
# 前の応答への依存性を持たせたい場合は引数を追加すれば良い
import os
import sys

from alarm import alarm
from alarm import alarm_set
from fetch_calendar import fetch_calendar
from fetch_weather import fetch_weather
from fetch_time_to_go import fetch_time_to_go

jtalkbin = "open_jtalk "
options = (
    "-m"
    + " /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
    + " -ow /tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic"
)


# 音声合成のコマンドを生成 (open jtalk を 使う場合）
def mk_jtalk_command(answer):
    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ";"
    play = "play -q /tmp/dialogue/out.wav; rm /tmp/dialogue/out.wav;"
    return jtalk + play


if __name__ == "__main__":
    # # 応答を辞書 reply に登録
    # conf = open(sys.argv[1],'r')
    # #conf = codecs.open(sys.argv[1],'r','utf8','ignore')
    # reply = {}
    # for line in conf:
    #     line = line.rstrip()
    #     a = line.split();
    #     reply[a[0]] = a[1]
    # conf.close()

    # 話者ID
    sid = int(sys.argv[2])

    # 認識結果
    asrresult = open(sys.argv[3], "r")
    question = asrresult.read().rstrip()
    asrresult.close()

    alarm_status = int(sys.argv[4])

    # 話者ID と認識結果を表示
    print(f"SPK{sid}:{question}")

    answer = ''
    if "天気" in question:
        answer += fetch_weather.main()
    if "予定" in question:
        answer += fetch_calendar.main()
    if "出発" in question:
        answer += fetch_time_to_go.main()
    if "時" in question:
        time = alarm_set.main()
        answer += "アラームを" + time[0] + "時" + time[1] + "分に設定しました"
        alarm.main(time)
        
    os.system(mk_jtalk_command(answer))
