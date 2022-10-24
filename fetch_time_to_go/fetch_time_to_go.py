# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import strip

# 出発駅の入力
departure_station = input("出発駅を入力してください：")
# 到着駅の入力
destination_station = input("到着駅を入力してください：")

destination_year = input("到着year:")
destination_month = input("到着month:")
destination_day = input("到着day:")
destination_hour = input("到着hour:")
destination_minute = input("到着minute:")

# 経路の取得先URL
route_url = "https://transit.yahoo.co.jp/search/print?from=" + departure_station + "&flatlon=&to=" + destination_station + "&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y=" + destination_year + "&m=" + destination_month + \
    "&d=" + destination_hour + "&hh=" + destination_hour + "&m1=" + \
    destination_minute[0] + "&m2=" + destination_minute[1] + \
    "&type=4&ticket=ic&expkind=1&userpass=1&ws=2&s=1&al=1&shin=1&ex=1&hb=1&lb=1&sr=1"
# print(route_url)
# Requestsを利用してWebページを取得する
route_response = requests.get(route_url)

# BeautifulSoupを利用してWebページを解析する
route_soup = BeautifulSoup(route_response.text, 'html.parser')

# 経路のサマリーを取得
route_summary = route_soup.find("div", class_="routeSummary")
# 所要時間を取得
required_time = route_summary.find("li", class_="time").get_text()
# 乗り換え回数を取得
transfer_count = route_summary.find("li", class_="transfer").get_text()
# 料金を取得
fare = route_summary.find("li", class_="fare").get_text()

# print("======"+departure_station+"から"+destination_station+"=======")
# print("所要時間："+required_time)
# print(transfer_count)
# print("料金："+fare)

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

# print(estimated_times)

# 路線ごとの料金を取得
fars = []
fars_tmp = route_detail.find_all("p", class_="fare")
for fare in fars_tmp:
    fars.append(fare.get_text().strip())


# 乗り換え詳細情報の出力
# print("======乗り換え情報======")
# for station,line,estimated_time,fare in zip(stations,lines,estimated_times,fars):
#     print(station)
#     print( " | " + line + " " + estimated_time + " " + fare)

# print(stations[len(stations)-1])
target = '[発]'
idx = lines[0].find(target)
departure_line = lines[0][:idx]
target = departure_station
idx = stations[0].find(target)
departure_time = stations[0][:idx]
print(departure_time + 'に' + departure_station + '駅,' + departure_line + 'です')

# https://transit.yahoo.co.jp/search/result?from=本郷三丁目&to=赤坂&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y=2022&m=10&d=24&hh=13&m1=2&m2=0&type=4&ticket=ic&expkind=1&userpass=1&ws=2&s=1&al=1&shin=1&ex=1&hb=1&lb=1&sr=1
# https://transit.yahoo.co.jp/search/result?from=本郷三丁目&to=赤坂&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y=2022&m=10&d=24&hh=13&m1=2&m2=0&type=4&ticket=ic&expkind=1&userpass=1&ws=2&s=0&al=1&shin=1&ex=1&hb=1&lb=1&sr=1
# https://transit.yahoo.co.jp/search/result?from=本郷三丁目&to=赤坂&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y=2022&m=10&d=24&hh=13&m1=2&m2=0&type=4&ticket
