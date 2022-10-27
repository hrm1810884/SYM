# silly_siri

## 開発にあたって

- コミットには可能な限りコミットメッセージを残しましょう
  - 後で誰が何をやったのか確認する時に便利です
  - 余裕があれば `add` / `fix` / `doc` などのプレフィックスを付けましょう
- 機能開発を行う際は必ず `feature/` で始まる名前のブランチを切って，そこで作業を行ってマージするようにしてください
  - `main` を直書きしたらぶっ飛ばします
  - ブランチを切る根本は `main` などの適切なブランチにしてください
- 必要のないゴミをアップロードしないように気をつけてください
  - .DS_Store
  - C 言語の実行ファイルなど，実行に必要のないファイル
  - テストファイル
- Jupyter Notebook（`ipynb`）をアップロードする時は出力はリセットしてください．差分を取った時に不幸せになるのを防ぐためです

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
