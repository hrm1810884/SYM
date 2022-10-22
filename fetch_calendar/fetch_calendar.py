import datetime
import os
import pickle
import sys

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# カレンダーAPIで操作できる範囲を設定（今回は読み書き）
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def print_txt(events):
    output = []
    if not events:
        output = "今日は特別な日程はありません"
    # 予定があった場合には、出力
    else:
        for event in events:
            if event["start"].get("dateTime") is None:
                output.append("終日" + event["summary"] + "があります")
            else:
                start = event["start"].get("dateTime")
                end = event["end"].get("dateTime")
                start_time = start.split("T")[1]
                start_hour, start_minute, start_else = start_time.split(":", 2)
                end_time = end.split("T")[1]
                end_hour, end_minute, end_else = end_time.split(":", 2)
                output.append(
                    start_hour
                    + "時"
                    + start_minute
                    + "分から"
                    + end_hour
                    + "時"
                    + end_minute
                    + "分まで"
                    + event["summary"]
                    + "があります"
                )
    sys.stdout.write(";".join(output))


def main():
    # Google にcalendarへのアクセストークンを要求してcredsに格納します。
    creds = None

    # 有効なトークンをすでに持っているかチェック（２回目以降の実行時に認証を省略するため）
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # 期限切れのトークンを持っているかチェック（認証を省略するため）
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refrestoken:
            creds.refresh(Request())
        # アクセストークンを要求
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials_hh.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # アクセストークン保存（２回目以降の実行時に認証を省略するため）
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    # カレンダーAPI操作に必要なインスタンス作成
    service = build("calendar", "v3", credentials=creds)

    # 現在時刻を取得
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    tomorrow = (
        datetime.datetime.today()
        .replace(hour=23, minute=59, second=59, microsecond=999999)
        .isoformat()
        + "Z"
    )
    # カレンダーから予定を取得
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            timeMax=tomorrow,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    print_txt(events)


if __name__ == "__main__":
    main()
