import schedule
import time
import os
#installしてない場合はscheduleを入れる
  
    
def main():
    string = input()
    while(True):
        print(string)
        if checkTime(string):
            break
        time.sleep(5)
        string = input()
    (hour,minute) = getTime(string)
    #test
    hour = 15
    minute = 36
    #↑にテスト用時刻入れる

    target = f'{str(hour).zfill(2)}:{str(minute).zfill(2)}'
    print(target+'にアラームをセットしました')
    #アラーム時間設定
    schedule.every().day.at(target).do(Sound)
    #アラーム待ち
    while True:
        schedule.run_pending()    
        time.sleep(1)


#目覚まし設定時間取得
def getTime(string):
    minute = 0
    hour = 0
    for i in range(len(string)):
        if string[i] == '':
            hour = 10
        if string[i] in ['5','6','7','8','9']:
            hour = int(string[i])
        if string[i] == '3' or string[i] == '半':
            minute = 30
    return (hour, minute)

#時刻設定だったら1、止めるだったら0
def checkTime(string):
    for i in range(len(string)):
        if string[i] == "止":
            return 0
    return 1

def checkStop(string):   
    if checkTime(string):
        return 0
    return 1

#音再生処理
def Sound():
    while(1): 
        os.system("play alarm1.mp3")#パス指定必要な場合はここで
        time.sleep(5)
        string = input()
        print(string)
        if  checkStop(string):
            print("alarm stopped")
            exit()

        

if __name__ == '__main__':
    main()
    