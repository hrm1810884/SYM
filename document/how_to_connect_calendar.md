# SYM と Google Calendar の接続について

SYM には予定を取得する機能があり，そこで Google の Calendar 機能を利用しています．そこで，ここでは SYM と Google Calendar を接続する方法を紹介していきます．

## 方法

### 1． GCP にログイン

SYM では Google Calendar の API を利用して情報をやりとりするため，Google Cloud Platform（GCP）でカレンダの API を取得していきます．
まず，Google のアカウントをお持ちでない方は [こちら](https://accounts.google.com) からアカウントを作成できます．
アカウントを取得できたら [GCP](https://console.cloud.google.com)にログインをしてください．

### 2． カレンダーの API を有効化

ログインしたら，検索バーから Google Calendar API と検索してください．
検索結果の一番上に出てくる Google Calendar API をクリックし，以下の画面が出てきたら「有効にする」で有効化を行います．

<p align="center">
  <img width="500" src=../asset/calendar_api_activate.png>
</p>

これで有効化は完了です．

### 3． 認証情報を登録

有効化を行ったら，ページ内の「チュートリアルとドキュメント」の [Get Started with the Calendar API](https://developers.google.com/calendar/api/guides/overview) をクリックし，左のサイドバーから使用する言語を選択できます．
ここでは Python を用いて API 連携を行うため，[Python](https://developers.google.com/calendar/api/quickstart/python) を選択してください．

選択先のチュートリアルに従い，API を有効化（一度すでに行っていますが，念の為ここでも行っておきます）し，チュートリアルに戻って Go to Credentials をクリックしてください．
クリック先で認証情報を登録し，取得できるクレデンシャルが SYM とカレンダを連携してくれます．

「＋認証情報を作成」から「OAuth クライアント ID」を選択してください．その後，

- OAuth 同意画面：「外部」
- アプリ情報：

必要な情報を登録することでクレデンシャルが発行されるはずです，使用するアプリケーションの種類は「デスクトップアプリ」を選択してください．
登録が完了し，クライアント ID とシークレット情報の json ファイルが表示されたらダウンロードを行ってください．
ここでダウンロードされた json ファイルが SYM との連携に必要なファイルになります．

### 4． クレデンシャルの登録

ダウンロードしたjsonファイル（クレデンシャル）をどうしましょう？
