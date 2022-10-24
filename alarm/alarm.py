import schedule
import time
import os
#installしてない場合はscheduleを入れる
#アラーム処理
def Alarm():
    Sound()
    print("end")
    exit()   #これがないと無限ループになる
#音再生処理
def Sound():
    """
    #pygameがjuliusと衝突して音がならないためos.systemに切り替え
    print("sound")
    pygame.mixer.init() #初期化
    pygame.mixer.music.load('alarm1.mp3') #読み込み
    
    pygame.mixer.music.play(-1) #ループ再生（引数を1にすると1回のみ再生）
    input()
    pygame.mixer.music.stop() #終了
    """
    while(1): 
        os.system("play alarm1.mp3")#パス指定必要な場合はここで
        time.sleep(5)
        string = input()
        print(string)
        if  checkStop(string):
            return 

           
    
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
    #hour = 15
    #minute = 22
    #↑にテスト用時刻入れる

    target = f'{str(hour).zfill(2)}:{str(minute).zfill(2)}'
    print(target+'にアラームをセットしました')
    #アラーム時間設定
    schedule.every().day.at(target).do(Alarm)
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
    print(hour)
    print(minute)
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

if __name__ == '__main__':
    main()
    