import datetime
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# カレンダーAPIで操作できる範囲を設定（今回は読み書き）
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def generate_credentials():
    """credentials を取得する

    Returns
    -------
    object
        credentials の中身
    """
    credentials = None

    # 既にアクセストークンを取得していればそれを持ってくる
    if os.path.exists("tmp/token.pickle"):
        with open("tmp/token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        # アクセストークンを要求
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "tmp/credentials.json", SCOPES
            )
            credentials = flow.run_local_server(port=0)

        # アクセストークン保存（２回目以降の実行時に認証を省略するため）
        with open("tmp/token.pickle", "wb") as token:
            pickle.dump(credentials, token)
    return credentials


def generate_events_text(events):
    """用事の文面を生成する

    Parameters
    ----------
    events : object
        用事を入れたオブジェクト

    Returns
    -------
    str
        用事をまとめた文面
    """
    if not events:
        return "今日は特別な日程はありません"

    result = []
    for event in events:
        if event["start"].get("dateTime") is None:
            result.append("終日" + event["summary"] + "があります")
        else:
            start = event["start"].get("dateTime")
            start_ymd, start_time = start.split("T")
            start_day = start_ymd.split("-")[2]
            start_hour, start_minute, _ = start_time.split(":", 2)

            end = event["end"].get("dateTime")
            end_ymd, end_time = end.split("T")
            end_day = end_ymd.split("-")[2]
            end_hour, end_minute, _ = end_time.split(":", 2)
            if end_day > start_day:
                end_hour = str(int(end_hour) + 24)

            result.append(
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
 
    return '  '.join(result)


def fetch_first_destination():
    """その日の予定の最初のものの場所を取得

    Returns
    -------
    str
        その日の予定の最初のものの場所
    """
    events = fetch_events()
    if not events:
        return None

    first_event = events[0]
    if "location" in first_event:
        start = first_event["start"].get("dateTime")
        _, start_time = start.split("T")
        start_hour, start_minute, _ = start_time.split(":", 2)
        return [first_event["location"], start_hour, start_minute]

    return None


def fetch_events():
    """その日の予定の一覧を取得する

    Returns
    -------
    object
        その日の予定の一覧
    """
    credentials = generate_credentials()

    # カレンダーAPI操作に必要なインスタンス作成
    service = build("calendar", "v3", credentials=credentials)

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
    return events


def main():
    events = fetch_events()
    return generate_events_text(events)


if __name__ == "__main__":
    main()
