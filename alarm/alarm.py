import os
import sys
import time

import schedule


def main():
    hour = sys.argv[1]
    minute = sys.argv[2]

    # アラーム時間設定
    get_up_time = f"{str(hour).zfill(2)}:{str(minute).zfill(2)}"
    schedule.every().day.at(get_up_time).do(sound)
    # アラーム待ち
    while True:
        if not os.path.isfile("../alarm/alarm_set.dat"):
            return schedule.CancelJob()
        schedule.run_pending()
        time.sleep(1)


# 目覚まし設定時間取得
def get_time(string):
    minute = 0
    hour = 0
    for char in string:
        if char == "1":
            hour = 10
        if char in ["5", "6", "7", "8", "9"]:
            hour = int(char)
        if char == "3" or char == "半":
            minute = 30
    return int(hour), int(minute)


# 音再生処理
def sound():
    while True:
        os.system("play ../alarm/alarm1.mp3")  # パス指定必要な場合はここで
        if os.path.isfile("../alarm/alarm_set.dat"):
            with open("../alarm/alarm_set.dat","w") as f:
                alarm_ringed = str(1)
                f.write(alarm_ringed)
        time.sleep(1)
        if not os.path.isfile("../alarm/alarm_set.dat"):
            return schedule.CancelJob()


if __name__ == "__main__":
    main()
