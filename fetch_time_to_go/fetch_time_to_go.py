import datetime
import os
import sys

import requests
from bs4 import BeautifulSoup

from fetch_calendar import fetch_calendar

DIR_INIT = "init"


def fetch_departure_station() -> str:
    """出発駅を取得する

    Returns
    -------
    str
        出発駅
    """
    if not os.path.exists(os.path.join(DIR_INIT, "init.dat")):
        print("Error: You need to initialize SYM first", file=sys.stderr)
        sys.exit()

    with open(os.path.join(DIR_INIT, "init.dat")) as init_file:
        for init_line in init_file:
            key, value = init_line.split()
            if key == "nearest_station":
                return value


def generate_route_url(departure_station: str, destination_information: str) -> str:
    """ルートの URL を生成する

    Parameters
    ----------
    departure_station : str
        出発駅
    destination_information : str
        到着の要件

    Returns
    -------
    str
        ルート検索の URL
    """
    destination_station, arrival_hour, arrival_minute = destination_information
    today = datetime.datetime.now()
    route_url = (
        f"https://transit.yahoo.co.jp/search/print?from={departure_station}"
        + f"&flatlon=&to={destination_station}"
        + "&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode="
        + f"&y={today.year}&m={today.month}&d={today.day}"
        + f"&hh={arrival_hour}&m1={arrival_minute[0]}&m2={arrival_minute[1]}"
        + "&type=4&ticket=ic&expkind=1&userpass=1&"
        + "ws=2&s=1&al=1&shin=1&ex=1&hb=1&lb=1&sr=1"
    )
    return route_url


def main():
    departure_station = fetch_departure_station()
    destination_information = fetch_calendar.fetch_first_destination()
    if destination_information is None:
        return "電車の用事はありません"

    # Requestsを利用してWebページを取得する
    route_url = generate_route_url(departure_station, destination_information)
    route_response = requests.get(route_url)

    # BeautifulSoupを利用してWebページを解析する
    route_soup = BeautifulSoup(route_response.text, "html.parser")

    # 乗り換えの詳細情報を取得
    route_detail = route_soup.find("div", class_="routeDetail")

    # 乗換駅の取得
    stations = []
    stations_elements = route_detail.find_all("div", class_="station")
    for station in stations_elements:
        stations.append(station.get_text().strip())

    # 乗り換え路線の取得
    lines = []
    lines_elements = route_detail.find_all("li", class_="transport")
    for line in lines_elements:
        lines.append(line.find("div").get_text().strip())

    line_target = "[発]"
    line_idx = lines[0].find(line_target)
    departure_line = lines[0][:line_idx]
    station_target = departure_station
    station_idx = stations[0].find(station_target)
    departure_time = stations[0][:station_idx]
    departure_hour,departure_minute = departure_time.split(":")
    return f"{departure_hour}時{departure_minute}分に{departure_station}駅，{departure_line}です"


if __name__ == "__main__":
    main()
