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
        if not os.path.isfile("alarm_set.dat"):
            return schedule.CancelJob()
        schedule.run_pending()
        time.sleep(1)


def extract_time_from_command(command):
    """文字列からアラームの時刻を計算する

    Parameters
    ----------
    command : str
        入力されたコマンド

    Returns
    -------
    tuple
        (アラームをセットする時, アラームをセットする分)
    """
    for char in command:
        if char == "1":
            hour = 10
        if char in ["5", "6", "7", "8", "9"]:
            hour = int(char)
        if char in ["3", "半"]:
            minute = 30
    return hour, minute


def sound():
    """音を鳴らす
    """
    while True:
        os.system("play alarm/alarm1.mp3")  # パス指定必要な場合はここで
        if os.path.isfile("alarm_set.dat"):
            with open("alarm_set.dat", "w") as f:
                f.write("1")
        time.sleep(1)
        if not os.path.isfile("alarm_set.dat"):
            return schedule.CancelJob()


if __name__ == "__main__":
    main()
