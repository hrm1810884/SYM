import requests
import sys
import os
from datetime import datetime


DIR_DATA = './data'


def get_place():  # 初期設定ファイルからアメダス地点の番号を返す
    with open(os.path.join(DIR_DATA, 'init.dat')) as init_file:
        init_prefecture, init_city = init_file.read().split('\n')

    prefecture_dict = {}
    with open(os.path.join(DIR_DATA, 'jma_prefecture.dat')) as prefecture_file:
        for prefecture_line in prefecture_file:
            prefecture, num = prefecture_line.split()
            prefecture_dict[prefecture] = num

    city_dict = {}
    with open(os.path.join(DIR_DATA, 'amd_city_tokyo.dat')) as city_file:
        for city_line in city_file:
            city, num = city_line.split()
            city_dict[city] = num

    return [prefecture_dict[init_prefecture], city_dict[init_city]]


def get_time():
    latest_time_url = 'https://www.jma.go.jp/bosai/amedas/data/latest_time.txt'
    latest_time_req = requests.get(latest_time_url)
    latest_datetime = datetime.strptime(
        latest_time_req.text, '%Y-%m-%dT%H:%M:%S%z')  # タイムゾーン込みで日時文字列をdatetime型へ
    yyyymmdd = latest_datetime.strftime('%Y%m%d')  # 年月日　- アメダスデータ取得時に必要
    # 3時間ごとの時間 - アメダスデータ取得時に必要
    h3 = ('0' + str((latest_datetime.hour//3)*3))[-2:]
    return [yyyymmdd, h3]


def judge_pop(latest_precipitation):
    pop_string = ''
    if (latest_precipitation == 0.0):
        pop_string = '現在雨は降っていません'
    elif (latest_precipitation < 0.5):
        pop_string = '現在雨がパラついています'
    elif (latest_precipitation < 1.0):
        pop_string = '現在小雨が降っています'
    elif (latest_precipitation < 4.0):
        pop_string = '現在雨が降っています'
    elif (latest_precipitation < 7.5):
        pop_string = '現在雨が強く降っています'
    else:
        pop_string = '現在とんでもない雨です'
    return pop_string


def main():
    prefecture_num, city_num = get_place()
    date, hour = get_time()
    # 気象庁のデータ取得
    jma_url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/' + \
        str(prefecture_num) + '.json'
    amd_url = 'https://www.jma.go.jp/bosai/amedas/data/point/' + \
        str(city_num) + '/' + str(date) + '_' + str(hour) + '.json'
    jma_json = requests.get(jma_url).json()
    amd_json = requests.get(amd_url).json()

    # 取得したいデータを選択
    jma_weather = jma_json[0]['timeSeries'][0]['areas'][0]['weathers'][0]
    jma_pops = jma_json[0]['timeSeries'][1]['areas'][0]['pops']
    jma_temp_min = jma_json[1]['tempAverage']['areas'][0]['min']
    jma_temp_max = jma_json[1]['tempAverage']['areas'][0]['max']

    # 全角スペース取得
    jma_weather = jma_weather.replace('　', '')

    latest_key = max(amd_json)  # 最新のアメダスデータが入っているkey
    latest_temp = amd_json[latest_key]['temp']  # 最新の気温データを取得, 品質情報を確認
    # 最新の降水量データを取得, 品質情報を確認
    latest_precipitation10m = amd_json[latest_key]['precipitation10m'][0]

    output = []
    output.append('本日の天気は' + jma_weather)
    output.append('現在の気温は' + str(latest_temp[0]) + '℃')
    output.append('最低気温は' + str(jma_temp_min) + '℃，' +
                  '最高気温は' + str(jma_temp_max) + '℃です')
    output.append(judge_pop(latest_precipitation10m))
    output.append('今後の降水確率は６時間ごとに，' + '%，'.join(map(str, jma_pops)) + '%です')

    sys.stdout.write(';'.join(output))


if __name__ == '__main__':
    main()
