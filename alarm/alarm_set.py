import os
import re
import time


def main(question):
    input_command = question
    return calc_time_from_command(input_command)


# 目覚まし設定時間取得
def calc_time_from_command(string):
    hour, minute, others = re.split('[時分]', string)
    return int(hour), int(minute)


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
