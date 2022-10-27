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

def reform_answer(answer):
    if '所' in answer:
        answer = answer.replace('所','ところ')
    if '℃' in answer:
        answer = answer.replace('℃ ', '度')
    if '時00分' in answer:
        answer = answer.replace('時00分','時')
    return answer


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
        open("tmp/already_asked.dat", "w")
        already_asked = False
        clothes_asking = False
        answer = fetch_weather.main(already_asked, clothes_asking)
        answer = answer.replace('℃', '℃ ')
    elif "詳しく" in question:
        already_asked = os.path.isfile("tmp/already_asked.dat")
        clothes_asking = False
        answer = fetch_weather.main(already_asked, clothes_asking)
        answer = answer.replace('℃', '℃ ')
    elif "服" in question:
        already_asked = False
        clothes_asking = True
        answer = fetch_weather.main(already_asked, clothes_asking)
    elif "予定" in question:
        answer = fetch_calendar.main()
    elif "出発" in question:
        answer = fetch_time_to_go.main()
    elif "時" in question:
        alarm_hour, alarm_minute = alarm.get_time(question)
        answer = f"アラームを{alarm_hour}時{alarm_minute}分に設定しました"
        if os.path.isfile("tmp/already_asked.dat"):
            os.remove("tmp/already_asked.dat")
        with open("tmp/alarm_set.dat", mode="w") as f:
            alarm_ringed = str(0)
            f.write(alarm_ringed)
        proc = subprocess.Popen(
            "python3 alarm/alarm.py {0} {1}".format(alarm_hour, alarm_minute),
            shell=True,
        )
    elif "止" in question:
        if os.path.isfile("tmp/alarm_set.dat"):
            with open("tmp/alarm_set.dat") as f:
                alarm_ringed = bool(int(f.read()))  # 0 or 1
                print(alarm_ringed)
                if alarm_ringed:
                    answer = "おはようございます"
                else:
                    answer = "アラームを解除しました"
            os.remove("tmp/alarm_set.dat")
        else:
            answer = "アラームがセットされていません"
    else:
        answer = "認識できません．もう一度お願いします"

    print("SYM:" + answer.replace('  ', '\n    '))
    os.system(mk_jtalk_command(reform_answer(answer)))
