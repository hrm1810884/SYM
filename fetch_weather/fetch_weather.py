import os
import sys
from datetime import datetime

import requests

DIR_DATA = "../fetch_weather/data"
DIR_INIT = "../init"


def get_place():  # 初期設定ファイルからアメダス地点の番号を返す
    if not os.path.exists(os.path.join(DIR_INIT, "init.dat")):
        print("Error: You need to initialize SYM first", file=sys.stderr)
        sys.exit()

    with open(os.path.join(DIR_INIT, "init.dat")) as init_file:
        for init_line in init_file:
            key, value = init_line.split()
            if key == "prefecture":
                init_prefecture = value
            if key == "city":
                init_city = value

    with open(os.path.join(DIR_DATA, "jma_prefecture.dat")) as prefecture_file:
        for prefecture_line in prefecture_file:
            tmp_prefecture_name, tmp_prefecture_id = prefecture_line.split()
            if tmp_prefecture_name == init_prefecture:
                prefecture_id = tmp_prefecture_id
                break

    with open(os.path.join(DIR_DATA, "amd_city_tokyo.dat")) as city_file:
        for city_line in city_file:
            tmp_city_name, tmp_city_id = city_line.split()
            if tmp_city_name == init_city:
                city_id = tmp_city_id
                break

    return [prefecture_id, city_id]


def get_time():
    latest_time_url = "https://www.jma.go.jp/bosai/amedas/data/latest_time.txt"
    latest_time_req = requests.get(latest_time_url)
    latest_datetime = datetime.strptime(
        latest_time_req.text, "%Y-%m-%dT%H:%M:%S%z"
    )  # タイムゾーン込みで日時文字列をdatetime型へ
    yyyymmdd = latest_datetime.strftime("%Y%m%d")  # 年月日　- アメダスデータ取得時に必要
    # 3時間ごとの時間 - アメダスデータ取得時に必要
    h3 = ("0" + str((latest_datetime.hour // 3) * 3))[-2:]
    return [yyyymmdd, h3, latest_datetime]


def recommend_clothes(date, tmp_min, tmp_max):
    yyyy = date[0:4]
    mm_ws = "04"
    mm_sw = "10"
    dd = "00"
    WS = int(yyyy + mm_ws + dd)
    SW = int(yyyy + mm_sw + dd)
    output = []
    if WS <= int(date) < SW:  # 夏季
        if tmp_max > 26:
            output.append("本日は非常に暑くなりますので半袖がおすすめです．帽子や日傘，日焼け止めもお忘れなく")
            if tmp_min <= 18:
                output.append("ただ，朝晩は少々冷え込みますので薄手の上着をお持ちください")
        elif tmp_max > 21:
            output.append("本日は半袖か薄めの長袖がおすすめです")
            if tmp_min <= 16:
                output.append("ただ，朝晩は少々冷え込みますので薄手の上着をお持ちください")
        elif tmp_min > 16:
            output.append("やや肌寒いので重ね着をおすすめします")
        elif tmp_min > 12:
            output.append("かなり冷え込みますので上着をお持ちください")
        else:
            output.append("非常に冷え込みますので厚手の上着をお持ちください")
    else:  # 冬季
        if tmp_min <= 6:
            output.append("凍える寒さです．厚手の上着をお持ちください．防寒対策も必須です")
            if tmp_max > 16:
                output.append("ただ，昼間は気温が上昇しますので上着は脱げるようにしておきましょう")
        elif tmp_min <= 12:
            output.append("非常に冷え込みますので，厚手の上着をお持ちください")
            if tmp_max > 16:
                output.append("ただ，昼間は気温が上昇しますので上着は脱げるようにしておきましょう")
        elif tmp_min <= 15:
            output.append("少々冷え込みますので防寒対策をしてください")
            if tmp_max > 22:
                output.append("ただ，昼間は気温が上昇しますので重ね着をおすすめします")
        elif tmp_min > 20:
            output.append("暖かい日ですので薄手の衣服をお勧めします")
        else:
            output.append("暑くなりますので半袖や薄手の長袖をおすすめします")

    return "  ".join(output)


def judge_pop(latest_precipitation):
    if latest_precipitation == 0.0:
        pop_string = "現在雨は降っていません"
    elif latest_precipitation < 0.5:
        pop_string = "現在雨がパラついています"
    elif latest_precipitation < 1.0:
        pop_string = "現在小雨が降っています"
    elif latest_precipitation < 4.0:
        pop_string = "現在雨が降っています"
    elif latest_precipitation < 7.5:
        pop_string = "現在雨が強く降っています"
    else:
        pop_string = "現在とんでもない雨です"
    return pop_string


def main(detail_required=False, clothes_required=False):
    prefecture_num, city_num = get_place()
    date, hour, datetime = get_time()
    # 気象庁のデータ取得
    jma_url = (
        "https://www.jma.go.jp/bosai/forecast/data/forecast/"
        + str(prefecture_num)
        + ".json"
    )
    amd_url = (
        "https://www.jma.go.jp/bosai/amedas/data/point/"
        + str(city_num)
        + "/"
        + str(date)
        + "_"
        + str(hour)
        + ".json"
    )
    jma_json = requests.get(jma_url).json()
    amd_json = requests.get(amd_url).json()

    # 取得したいデータを選択
    jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
    jma_pops = jma_json[0]["timeSeries"][1]["areas"][0]["pops"]
    jma_temp_min = jma_json[1]["tempAverage"]["areas"][0]["min"]
    jma_temp_max = jma_json[1]["tempAverage"]["areas"][0]["max"]

    # 全角スペース取得
    jma_weather = jma_weather.replace("　", "")

    latest_key = max(amd_json)  # 最新のアメダスデータが入っているkey
    latest_temp = amd_json[latest_key]["temp"]  # 最新の気温データを取得, 品質情報を確認
    # 最新の降水量データを取得, 品質情報を確認
    latest_precipitation10m = amd_json[latest_key]["precipitation10m"][0]

    output = []
    if clothes_required:
        output.append(recommend_clothes(date, float(jma_temp_min), float(jma_temp_max)))
    else:
        output.append("本日の天気は" + jma_weather)
        output.append("現在の気温は" + str(latest_temp[0]) + "℃です")
        if detail_required:
            output.append(
                "最低気温は" + str(jma_temp_min) + "℃，" + "最高気温は" + str(jma_temp_max) + "℃です"
            )
            output.append(judge_pop(latest_precipitation10m))
            output.append(
                "午前中の降水確率は" + jma_pops[0] + "%，午後の降水確率は" + jma_pops[1] + "%です"
            )

    return "  ".join(output)


if __name__ == "__main__":
    main()
