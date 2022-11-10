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
    """回答を発音しやすいように書き換える

    Parameters
    ----------
    answer : str
        書き換える回答文
    """
    if "所" in answer:
        answer = answer.replace("所", "ところ")
    if "℃" in answer:
        answer = answer.replace("℃ ", "度")
    if "時00分" in answer:
        answer = answer.replace("時00分", "時")
    if "時0分" in answer:
        answer = answer.replace("時0分", "時")
    return answer


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
        open("tmp/already_asked.dat", "w")
        answer = fetch_weather.main(detail_required=False, clothes_required=False)
        answer = answer.replace("℃", "℃ ")
    elif "詳しく" in question:
        answer = fetch_weather.main(
            detail_required=os.path.isfile("tmp/already_asked.dat"),
            clothes_required=False,
        )
        answer = answer.replace("℃", "℃ ")
    elif "服" in question:
        answer = fetch_weather.main(detail_required=False, clothes_required=True)
    elif "予定" in question:
        answer = fetch_calendar.main()
    elif "出発" in question:
        answer = fetch_time_to_go.main()
    elif "時" in question:
        if os.path.isfile("tmp/alarm_set.dat"):
            answer = "既にアラームがセットされています"
        else:
            alarm_hour, alarm_minute = alarm.extract_time_from_command(question)
            answer = f"アラームを{alarm_hour}時{alarm_minute}分に設定しました"
            if os.path.isfile("tmp/already_asked.dat"):
                os.remove("tmp/already_asked.dat")
            with open("tmp/alarm_set.dat", mode="w") as f:
                f.write("0")
            subprocess.Popen(
                "python3 alarm/alarm.py {0} {1}".format(alarm_hour, alarm_minute),
                shell=True,
            )
    elif "止" in question:
        if os.path.isfile("tmp/alarm_set.dat"):
            with open("tmp/alarm_set.dat") as f:
                alarm_ringed = bool(int(f.read()))  # 0 or 1
            answer = "おはようございます" if alarm_ringed else "アラームを解除しました"
            os.remove("tmp/alarm_set.dat")
        else:
            answer = "アラームがセットされていません"
    else:
        answer = "認識できません．もう一度お願いします"
    return answer


def main():
    # 認識情報を取得
    asrresult = open(sys.argv[1], "r")
    question = asrresult.read().rstrip()
    asrresult.close()

    # 話者 ID と認識結果を表示
    print(f"{question}")

    answer = exe(question)
    print("SYM:" + answer.replace("  ", "\n    "))
    os.system(mk_jtalk_command(reform_answer(answer)))


if __name__ == "__main__":
    main()
