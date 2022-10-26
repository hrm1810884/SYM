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


def mk_jtalk_command(answer):
    """音声情報のコマンドを生成する

    Parameters
    ----------
    answer : str
        応答する内容

    Returns
    -------
    str
        音声情報のコマンド
    """
    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ";"
    play = "play -q /tmp/dialogue/out.wav; rm /tmp/dialogue/out.wav;"
    return jtalk + play

def reform_answer(answer):
    if '所' in answer:
        answer.replace('所','ところ')
    if '℃' in answer:
        answer.replace('℃ ', '℃')
    if '時00分' in answer:
        answer.replace('時00分','時')


def exe(question):
    """質問内容に応じて応答を返す

    Parameters
    ----------
    question : str
        質問文

    Returns
    -------
    str
        SYM の応答
    """
    if "天気" in question:
        open("already_asked.dat", "w")
        answer = fetch_weather.main(detail_required=False, clothes_required=False)
        answer = answer.replace('℃', '℃ ')
    elif "詳しく" in question:
        answer = fetch_weather.main(
            detail_required=os.path.isfile("already_asked.dat"),
            clothes_required=False
        )
        answer = answer.replace('℃', '℃ ')
    elif "服" in question:
        answer = fetch_weather.main(detail_required=False, clothes_required=True)
    elif "予定" in question:
        answer = fetch_calendar.main()
    elif "出発" in question:
        answer = fetch_time_to_go.main()
    elif "時" in question:
        alarm_hour, alarm_minute = alarm.get_time(question)
        answer = f"アラームを{alarm_hour}時{alarm_minute}分に設定しました"
        if os.path.isfile("already_asked.dat"):
            os.remove("already_asked.dat")
        with open("alarm_set.dat", mode="w") as f:
            f.write("0")
        subprocess.Popen(
            "python3 alarm/alarm.py {0} {1}".format(alarm_hour, alarm_minute),
            shell=True,
        )
    elif "止" in question:
        if os.path.isfile("alarm_set.dat"):
            with open("alarm_set.dat") as f:
                alarm_ringed = bool(int(f.read()))  # 0 or 1
                print(alarm_ringed)
            answer = "おはようございます" if alarm_ringed else "アラームを解除しました"
            os.remove("alarm_set.dat")
        else:
            answer = "アラームがセットされていません"
    else:
        answer = "認識できません．もう一度お願いします"

    return answer


def main():
    # 認識情報を取得
    speaker_id = int(sys.argv[2])
    asrresult = open(sys.argv[3], "r")
    question = asrresult.read().rstrip()
    asrresult.close()

    # 話者ID と認識結果を表示
    print(f"SPK{speaker_id}:{question}")

    answer = exe(question)

    print("SYM:" + answer.replace('  ', '\n    '))
    reform_answer(answer)
    os.system(mk_jtalk_command(answer))


if __name__ == "__main__":
    main()
