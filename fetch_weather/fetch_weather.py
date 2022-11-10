import os
import sys
from datetime import datetime

import requests

DIR_DATA = "fetch_weather/data"
DIR_INIT = "init"


def fetch_location_number() -> list:
    """初期設定ファイルからアメダス地点の番号を取得する

    Returns
    -------
    list
        [県の番号, 都市の番号]
    """
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


def fetch_time_information() -> list:
    """時間にまつわる情報を取得する

    Returns
    -------
    list
        [日付，３時間ごとの時間，データの最終更新時刻]
    """
    latest_time_url = "https://www.jma.go.jp/bosai/amedas/data/latest_time.txt"
    latest_time_req = requests.get(latest_time_url)
    latest_datetime = datetime.strptime(
        latest_time_req.text, "%Y-%m-%dT%H:%M:%S%z"
    )  # タイムゾーン込みで日時文字列をdatetime型へ
    yyyymmdd = latest_datetime.strftime("%Y%m%d")  # 年月日 - アメダスデータ取得時に必要
    # ３時間ごとの時間 - アメダスデータ取得時に必要
    h3 = ("0" + str((latest_datetime.hour // 3) * 3))[-2:]
    return [yyyymmdd, h3, latest_datetime]


def recommend_clothes_in_summer(tmp_min: float, tmp_max: float) -> str:
    """夏の服装をレコメンドする

    Parameters
    ----------
    tmp_min : float
        最低気温
    tmp_max : float
        最奥気温

    Returns
    -------
    str
        服装をレコメンドする文面
    """
    if tmp_max > 26:
        recommendation = "本日は非常に暑くなりますので半袖がおすすめです．帽子や日傘，日焼け止めもお忘れなく"
        if tmp_min <= 18:
            recommendation = recommendation + "  ただ，朝晩は少々冷え込みますので薄手の上着をお持ちください"
        return recommendation
    if tmp_max > 21:
        recommendation = "本日は半袖か薄めの長袖がおすすめです"
        if tmp_min <= 16:
            recommendation = recommendation + "  ただ，朝晩は少々冷え込みますので薄手の上着をお持ちください"
        return recommendation
    if tmp_min > 16:
        return "やや肌寒いので重ね着をおすすめします"
    if tmp_min > 12:
        return "かなり冷え込みますので上着をお持ちください"
    return "非常に冷え込みますので厚手の上着をお持ちください"


def recommend_clothes_in_winter(tmp_min: float, tmp_max: float) -> str:
    """冬の服装をレコメンドする

    Parameters
    ----------
    tmp_min : float
        最低気温
    tmp_max : float
        最奥気温

    Returns
    -------
    str
        服装をレコメンドする文面
    """
    if tmp_min <= 6:
        recommendation = "凍える寒さです．厚手の上着をお持ちください．防寒対策も必須です"
        if tmp_max > 16:
            recommendation = recommendation + "  ただ，昼間は気温が上昇しますので上着は脱げるようにしておきましょう"
        return recommendation
    if tmp_min <= 12:
        recommendation = "非常に冷え込みますので，厚手の上着をお持ちください"
        if tmp_max > 16:
            recommendation = recommendation + "  ただ，昼間は気温が上昇しますので上着は脱げるようにしておきましょう"
        return recommendation
    if tmp_min <= 15:
        recommendation = "少々冷え込みますので防寒対策をしてください"
        if tmp_max > 22:
            recommendation = recommendation + "  ただ，昼間は気温が上昇しますので重ね着をおすすめします"
        return recommendation
    if tmp_min > 20:
        return "暖かい日ですので薄手の衣服をおすすめします"
    else:
        return "暑くなりますので半袖や薄手の長袖をおすすめします"


def recommend_clothes(date: str, tmp_min: float, tmp_max: float) -> str:
    """気温を基に服をレコメンドする

    Parameters
    ----------
    date : str
        日付
    tmp_min : float
        最低気温
    tmp_max : float
        最高気温

    Returns
    -------
    str
        服をレコメンドする文面
    """
    yyyy = date[0:4]
    mm_ws = "04"
    mm_sw = "10"
    dd = "00"
    WS = int(yyyy + mm_ws + dd)
    SW = int(yyyy + mm_sw + dd)
    return (
        recommend_clothes_in_summer(tmp_min, tmp_max)
        if WS <= int(date) < SW
        else recommend_clothes_in_winter(tmp_min, tmp_max)
    )


def tell_about_pop(current_precipitation: float) -> str:
    """現在の降水量についての文面を取得する

    Parameters
    ----------
    current_precipitation : float
        現在の降水量

    Returns
    -------
    str
        現在の降水量について説明する文
    """
    if current_precipitation == 0.0:
        return "現在雨は降っていません"
    if current_precipitation < 0.5:
        return "現在雨がパラついています"
    if current_precipitation < 1.0:
        return "現在小雨が降っています"
    if current_precipitation < 4.0:
        return "現在雨が降っています"
    if current_precipitation < 7.5:
        return "現在雨が強く降っています"
    return "現在とんでもない雨です"


def main(detail_required=False, clothes_required=False):
    prefecture_id, city_id = fetch_location_number()
    date, hour, _ = fetch_time_information()

    jma_url = (
        "https://www.jma.go.jp/bosai/forecast/data/forecast/"
        + str(prefecture_id)
        + ".json"
    )
    amd_url = (
        "https://www.jma.go.jp/bosai/amedas/data/point/"
        + str(city_id)
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
        output.append(f"本日の天気は{jma_weather}")
        output.append(f"現在の気温は{latest_temp[0]}℃です")
        if detail_required:
            output.append(f"最低気温は{jma_temp_min}℃，最高気温は{jma_temp_max}℃です")
            output.append(tell_about_pop(latest_precipitation10m))
            output.append(f"午前中の降水確率は{jma_pops[0]}%，午後の降水確率は{jma_pops[1]}%です")

    return "  ".join(output)


if __name__ == "__main__":
    main()
