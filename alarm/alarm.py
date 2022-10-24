import pygame.mixer
import schedule
import time
import sys
import os
#installしてない場合はpygameとscheduleを入れる
#アラーム処理
def Alarm():
    print("alarm")
    Sound()
    exit()   #これがないと無限ループになるので注意
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
        print("Sound")
        os.system("play alarm1.mp3")
        time.sleep(5)
        stop = input()
        print(stop)
        for i in range(len(stop)):
            
            if (stop[i] == '止'):
                print("alarm stop")
                return 0
           
    
def main():
    #string = sys.stdin.readline()

    string = input()
    print(string)
    #str = '<s>5時半にかけて</s>'
    minute = 0
    #目覚まし設定時間取得
    
    for i in range(len(string)):
        if string[i] == '1':
            hour = 10
        if string[i] in ['5','6','7','8','9']:
            hour = int(string[i])
        if string[i] == '3' or string[i] == '半':
            minute = 30
    #test
    hour = 14
    minute = 49
    target = f'{str(hour).zfill(2)}:{str(minute).zfill(2)}'
    print(target+'にアラームをセットしました')
    #アラーム時間設定
    schedule.every().day.at(target).do(Alarm)
    #アラーム待ち
    while True:
        schedule.run_pending()
        speak = input()
        print(speak)    
        
        time.sleep(1)
    
if __name__ == '__main__':
    main()
    