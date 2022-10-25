import os
import time
import schedule


def main(question):
    input_command = question
    """
    while True:
        print(input_command)
        if check_time(input_command):
            break
        time.sleep(5)
        input_command = input()
    """
    (hour, minute) = calc_time_from_command(input_command)
    # test
    # hour = 15
    # minute = 36

    target = f"{str(hour).zfill(2)}:{str(minute).zfill(2)}"
    print(target + "にアラームをセットしました")
    # アラーム時間設定
    schedule.every().day.at(target).do(sound)
    # アラーム待ち
    while True:
        schedule.run_pending()
        time.sleep(1)


# 目覚まし設定時間取得
def calc_time_from_command(string):
    minute = 0
    hour = 0
    for char in string:
        if char == "1":
            hour = 10
        if char in ["5", "6", "7", "8", "9"]:
            hour = int(char)
        if char == "3" or char == "半":
            minute = 30
    return (hour, minute)


# 時刻設定だったら1、止めるだったら0
def check_time(string):
    if "止" in string:
        return 0
    return 1


def command_is_stop(string):
    return "止" in string


# 音再生処理
def sound():
    while 1:
        os.system("play alarm1.mp3")  # パス指定必要な場合はここで
        time.sleep(5)
        string = input()
        print(string)
        if command_is_stop(string):
            print("alarm stopped")
            exit()


if __name__ == "__main__":
    main()
