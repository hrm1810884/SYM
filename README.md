<h1 align="center">
  <img src=./asset/SYM_logo_text.png width="300">
</h1>

## これはなに

SYM（Smarter than You in the Morning）は，朝忙しい時間帯に物理的に手が離せないあなたを助ける音声対話システムです．

## 使い方

### 初期化

以下のコードを実行してください．実行に必要な以下の情報を取得した後，必要なライブラリをインストールします．

- 名前
- 最寄り駅
- 住んでいる都道府県
- 地域

```[bash]
bash ./init/init.sh
```

なお，過去に初期化したことがある場合は以下の警告が出ます．

```[bash]
Warning: You initializtion has already been completed.
Are you sure to reinitialize? [y/N]
```

情報の変更などで変更する場合は <kbd>y</kbd> または <kbd>Y</kbd> を押して，変更を行ってください．

### アラーム

音声のみでアラームを操作できます.使用の流れは

- 夜にアラーム時間を設定する(5:00-10:30, 30分おきに設定可能)
- 朝にアラームを止める

の2つです.

「アラームを7:00にかけて」と話すとSYMはアラーム設定時間を復唱します.SYMは設定時間になるとアラーム音を鳴らします.

「アラーム止めて」と話すとアラームが止まり、SYMは”おはようございます”と話します.



### 天気予報

「今日の天気は？」と話すことで簡易版が発動し，

- その日の天気
- 現在の気温

を教えてくれます．

加えて，「詳しく」と話すと，

- その日の天気
- 現在の気温
- その日の最高気温・最低気温
- 現在の降水量
- おすすめの服装

を話してくれます．

### カレンダー

「今日の予定は？」と聞くことで発動します．

### 乗換案内

「何時に出発？」と聞くことで発動します．

カレンダーのその日の予定の中で最初のものに駅が指定されている場合，自分の最寄り駅からその駅への経路を調べてくれます．
その後，そのうち最も出発時刻の遅いものの出発時刻，路線名を話してくれます．

## 参考にしたもの
．`update_references` ブランチからどうぞ

- [Waking up is the hardest thing I do all day: Sleep inertia and sleep drunkenness](https://pubmed.ncbi.nlm.nih.gov/27692973/)
- [Sleep inertia, sleep homeostatic, and circadian influences on higher-order cognitive functions](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5124508/)
- [【Python】GoogleカレンダーAPIを操作して予定の取得・追加をする方法](https://kosuke-space.com/google-calendar-api-python)
- [PythonでGoogleカレンダーAPIを使用する方法](https://maasaablog.com/development/python/4744/)
- [Python で Google Calendar API を使ってみた](https://www.coppla-note.net/posts/tutorial/google-calendar-api/)
- [【Python】気象庁API から天気予報を取得してみた](https://qiita.com/ehjivh/items/121afaecad59a7e11c61)
- [Python と気象庁の天気予報 JSON を使って全国の天気予報を取得してみる](https://www.gis-py.com/entry/weather-json)
- [気象庁JSONデータ](https://qiita.com/michan06/items/48503631dd30275288f7)
- [【Colab / Python】気象庁API - 気象データの収集](https://qiita.com/T_Ryota/items/ef96d6575404a0fd46dd)
- [yahoo路線乗り換え案内の情報を抽出したい](https://qiita.com/hirohiroto522/items/2fc33cbc36ea8600f867)
- [yahoo路線の運行情報を取得したい](https://qiita.com/hirohiroto522/items/6ff29be1344be805ecb0)
- [Pythonからシェルコマンドを実行！subprocessでサブプロセスを実行する方法まとめ](https://dev.classmethod.jp/articles/python-subprocess-shell-command/)
- [あpython　subprocess.run内のコマンドで　変数を利用したい](https://teratail.com/questions/183775)
