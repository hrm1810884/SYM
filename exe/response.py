#!/usr/bin/env python3
# coding: utf-8

import os
import subprocess
import sys

from alarm import alarm_set
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

    answer = ""
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
        alarm_hour, alarm_minute = alarm_set.main(question)
        answer = f"アラームを{alarm_hour}時{alarm_minute}分に設定しました"
        os.system(mk_jtalk_command(answer))
        print("SYM:" + answer)
        path_txt = "../alarm/alarm_set_tmp.txt"
        with open(path_txt, mode="w") as f:
            f.write(answer)
        proc = subprocess.run("../alarm/asr-recog.sh", shell=True)
        answer = "おはようございます"
    elif "止" in question:
        answer = "アラームがセットされていません"
    else:
        answer = "認識できません．もう一度お願いします"

    print("SYM:" + answer)
    os.system(mk_jtalk_command(answer))
