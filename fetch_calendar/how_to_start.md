# SYMとGoggle Calendarの接続について
SYMには予定を取得する機能があり,そこでGoogleのCalendar機能を利用しています.そこで,ここではSYMとGoogle Calendarを接続する方法を紹介していきます.
## 方法
1. [GCPにログイン](#anchor1)
1. [カレンダのAPIを有効化](#anchor2)
1. [認証情報の登録](#anchor3)
1. [クレデンシャルの登録](#anchor4)

<a id="anchor1"></a>

1. GCPにログイン  
  SYMではGoogle CalendarのAPIを利用して情報をやりとりする ため, GCPでカレンダのAPIを取得していきます.  
  まず,Googleのアカウントをお持ちでない方は[こちら]('https://accounts.google.com')からアカウントを作成できます.  
  アカウントを取得できたら [Google Cloud Platform (GCP)]('https://console.cloud.google.com')にログインをしてください.
<a id="anchor2"></a>

1. カレンダのAPIを有効化  
   ログインしたら,検索バーからGoogle Calendar APIと検索してください.検索結果の一番上に出てくるGoogle Calendar APIをクリックし, 以下の画面が出てきたら「有効にする」で有効化を行います.  
    <p align="center">
    　　<img width="250" src=Calendar_activate.png>
    </p>
    これで有効化は完了です.
<a id="anchor3"></a>

3. 認証情報を登録  
    有効化を行ったら,ページ内の「チュートリアルとドキュメント」の[Get Started with the Calendar API]("https://developers.google.com/calendar/api/guides/overview")をクリックし,左のサイドバーから使用する言語を選択できます.ここではpythonを用いてAPI連携を行うため,「python」を選択してください.  
    選択先のチュートリアルに従い, APIを有効化（一度すでに行っていますが,念の為ここでも行っておきます.)し,チュートリアルに戻ってGo to Credentialsをクリックしてください.  
    クリック先で認証情報を登録し,取得できるクレデンシャルがSYMとカレンダを連携してくれます.  
    「＋認証情報を作成」から「OAuth クライアントID」を選択してください.指示に従い,必要な情報を登録することでクレデンシャルが発行されるはずです,使用するアプリケーションの種類は「デスクトップアプリ」を選択してください.  
    登録が完了し,クライアントIDとシークレット情報のjsonファイルが表示されたらダウンロードを行ってください.ここでダウンロードされたjsonファイルがSYMとの連携に必要なファイルになります.
<a id="anchor4"></a>

1. クレデンシャルの登録  
   ダウンロードしたjsonファイル（クレデンシャル）をどうしましょう？

   
