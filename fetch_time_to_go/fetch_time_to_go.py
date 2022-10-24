import datetime
import os
import sys

import requests
from bs4 import BeautifulSoup

from fetch_calendar.fetch_calendar import get_destination

DIR_INIT = "../init"


def fetch_departure_station():
    if not os.path.exists(os.path.join(DIR_INIT, "init.dat")):
        print("Error: You need to initialize SYM first", file=sys.stderr)
        sys.exit()

    with open(os.path.join(DIR_INIT, "init.dat")) as init_file:
        for init_line in init_file:
            key, value = init_line.split()
            if key == "nearest_stations":
                return value


def generate_route_url(departure_station):
    destination_information = get_destination()
    if destination_information is None:
        return "電車の用事はありません"
    destination_station, arrival_hour, arrival_minute = destination_information
    today = datetime.datetime.now()
    route_url = (
        "https://transit.yahoo.co.jp/search/print?from="
        + departure_station
        + "&flatlon=&to="
        + destination_station
        + "&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y="
        + today.year
        + "&m="
        + today.month
        + "&d="
        + today.day
        + "&hh="
        + arrival_hour
        + "&m1="
        + arrival_minute[0]
        + "&m2="
        + arrival_minute[1]
        + "&type=4&ticket=ic&expkind=1&userpass=1&"
        + "ws=2&s=1&al=1&shin=1&ex=1&hb=1&lb=1&sr=1"
    )
    return route_url


def main():
    departure_station = fetch_departure_station()

    # Requestsを利用してWebページを取得する
    route_url = generate_route_url(departure_station)
    route_response = requests.get(route_url)

    # BeautifulSoupを利用してWebページを解析する
    route_soup = BeautifulSoup(route_response.text, "html.parser")

    # 経路のサマリーを取得
    route_summary = route_soup.find("div", class_="routeSummary")
    # 所要時間を取得
    # required_time = route_summary.find("li", class_="time").get_text()
    # 乗り換え回数を取得
    # transfer_count = route_summary.find("li", class_="transfer").get_text()
    # 料金を取得
    fare = route_summary.find("li", class_="fare").get_text()

    # 乗り換えの詳細情報を取得
    route_detail = route_soup.find("div", class_="routeDetail")

    # 乗換駅の取得
    stations = []
    stations_tmp = route_detail.find_all("div", class_="station")
    for station in stations_tmp:
        stations.append(station.get_text().strip())

    # 乗り換え路線の取得
    lines = []
    lines_tmp = route_detail.find_all("li", class_="transport")
    for line in lines_tmp:
        line = line.find("div").get_text().strip()
        lines.append(line)

    # 路線ごとの所要時間を取得
    estimated_times = []
    estimated_times_tmp = route_detail.find_all("li", class_="estimatedTime")
    for estimated_time in estimated_times_tmp:
        estimated_times.append(estimated_time.get_text())

    # 路線ごとの料金を取得
    fars = []
    fars_tmp = route_detail.find_all("p", class_="fare")
    for fare in fars_tmp:
        fars.append(fare.get_text().strip())

    target = "[発]"
    idx = lines[0].find(target)
    departure_line = lines[0][:idx]
    target = departure_station
    idx = stations[0].find(target)
    departure_time = stations[0][:idx]
    return departure_time + "に" + departure_station + "駅，" + departure_line + "です"


if __name__ == "__main__":
    main()
