#!/usr/bin/env python3
# coding: utf-8

import os
import subprocess
import sys

from alarm import alarm
from fetch_calendar import fetch_calendar
from fetch_time_to_go import fetch_time_to_go
from fetch_weather import fetch_weather

jtalkbin = "open_jtalk "
options = (
    "-m "
    + "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
    + " -ow /tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic"
)


# 音声合成のコマンドを生成 (open jtalk を 使う場合）
def mk_jtalk_command(answer):
    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ";"
    play = "play -q /tmp/dialogue/out.wav; rm /tmp/dialogue/out.wav;"
    return jtalk + play


if __name__ == "__main__":
    # 話者ID
    sid = int(sys.argv[2])

    # 認識結果
    asrresult = open(sys.argv[3], "r")
    question = asrresult.read().rstrip()
    asrresult.close()

    # 話者ID と認識結果を表示
    print(f"SPK{sid}:{question}")

    if "天気" in question:
        open("already_asked.dat", "w")
        answer = fetch_weather.main(False)
    elif "詳しく" in question:
        already_asked = os.path.isfile("already_asked.dat")
        answer = fetch_weather.main(already_asked)
    elif "予定" in question:
        answer = fetch_calendar.main()
    elif "出発" in question:
        answer = fetch_time_to_go.main()
    elif "時" in question:
        alarm_hour, alarm_minute = alarm.get_time(question)
        answer = f"アラームを{alarm_hour}時{alarm_minute}分に設定しました"
        if os.path.isfile("already_asked.dat"):
            os.remove("already_asked.dat")
        with open("../alarm/alarm_set.dat", mode="w") as f:
            alarm_ringed = str(0)
            f.write(alarm_ringed)
        proc = subprocess.Popen("python3 ../alarm/alarm.py {0} {1}".format(alarm_hour,alarm_minute), shell=True)
    elif "止" in question:
        if os.path.isfile("../alarm/alarm_set.dat"):
            with open("../alarm/alarm_set.dat") as f:
                alarm_ringed = bool(int(f.read())) #0or1
                print(alarm_ringed)
                if(alarm_ringed):
                    answer = "おはようございます"
                else:
                    answer = "アラームを解除しました"
            os.remove("../alarm/alarm_set.dat")
        else:
            answer = "アラームがセットされていません"
    else:
        answer = "認識できません．もう一度お願いします"

    print("SYM:" + answer)
    os.system(mk_jtalk_command(answer))
