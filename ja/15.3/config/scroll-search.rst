==================
検索結果の一括取得
==================

概要
====

|Fess| の通常の検索では、ページング機能により一定数の検索結果のみが表示されます。
すべての検索結果を一括で取得したい場合は、スクロール検索(Scroll Search)機能を利用します。

この機能は、データの一括エクスポートやバックアップ、大量データの分析など、
すべての検索結果を処理する必要がある場合に有用です。

ユースケース
============

スクロール検索は、以下のような用途に適しています。

- 検索結果の全件エクスポート
- データ分析用の大量データ取得
- バッチ処理でのデータ取得
- 外部システムへのデータ同期
- レポート生成用のデータ収集

.. warning::
   スクロール検索は大量のデータを返すため、通常の検索と比較して
   サーバーリソースを多く消費します。必要な場合のみ有効化してください。

設定方法
========

スクロール検索の有効化
----------------------

デフォルトでは、セキュリティとパフォーマンスの観点からスクロール検索は無効になっています。
有効にするには、``fess_config.properties`` または ``/etc/fess/fess_config.properties`` で
以下の設定を変更します。

::

    api.search.scroll=true

.. note::
   設定変更後は、|Fess| を再起動する必要があります。

レスポンスフィールドの設定
--------------------------

検索結果のレスポンスに含めるフィールドをカスタマイズできます。
デフォルトでは基本的なフィールドのみが返されますが、追加のフィールドを指定することができます。

::

    query.additional.scroll.response.fields=content,mimetype,filename,created,last_modified

複数のフィールドを指定する場合は、カンマ区切りで列挙します。

スクロールのタイムアウト設定
----------------------------

スクロールコンテキストの有効期間を設定できます。
デフォルトは1分です。

::

    api.search.scroll.timeout=1m

単位:
- ``s``: 秒
- ``m``: 分
- ``h``: 時間

使用方法
========

基本的な使用方法
----------------

スクロール検索へのアクセスは、以下のURLで実行します。

::

    http://localhost:8080/json/scroll?q=検索キーワード

検索結果は NDJSON(Newline Delimited JSON)形式で返却されます。
1行ごとに1つのドキュメントがJSON形式で出力されます。

**例:**

::

    curl "http://localhost:8080/json/scroll?q=Fess"

リクエストパラメータ
--------------------

スクロール検索では、以下のパラメータを使用できます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - パラメータ名
     - 説明
   * - ``q``
     - 検索クエリ(必須)
   * - ``size``
     - 1回のスクロールで取得する件数(デフォルト: 100)
   * - ``scroll``
     - スクロールコンテキストの有効時間(デフォルト: 1m)
   * - ``fields.label``
     - ラベルによるフィルタリング

検索クエリの指定
----------------

通常の検索と同じように、検索クエリを指定できます。

**例: キーワード検索**

::

    curl "http://localhost:8080/json/scroll?q=検索エンジン"

**例: フィールド指定検索**

::

    curl "http://localhost:8080/json/scroll?q=title:Fess"

**例: 全件取得(検索条件なし)**

::

    curl "http://localhost:8080/json/scroll?q=*:*"

取得件数の指定
--------------

1回のスクロールで取得する件数を変更できます。

::

    curl "http://localhost:8080/json/scroll?q=Fess&size=500"

.. note::
   ``size`` パラメータを大きくしすぎると、メモリ使用量が増加します。
   通常は100〜1000の範囲で設定することを推奨します。

ラベルによるフィルタリング
--------------------------

特定のラベルに属するドキュメントのみを取得できます。

::

    curl "http://localhost:8080/json/scroll?q=*:*&fields.label=public"

認証が必要な場合
----------------

ロールベース検索を使用している場合、認証情報を含める必要があります。

::

    curl -u username:password "http://localhost:8080/json/scroll?q=Fess"

または、APIトークンを使用:

::

    curl -H "Authorization: Bearer YOUR_API_TOKEN" \
         "http://localhost:8080/json/scroll?q=Fess"

レスポンス形式
==============

NDJSON形式
----------

スクロール検索のレスポンスは、NDJSON(Newline Delimited JSON)形式で返されます。
各行が1つのドキュメントを表します。

**例:**

::

    {"url":"http://example.com/page1","title":"Page 1","content":"..."}
    {"url":"http://example.com/page2","title":"Page 2","content":"..."}
    {"url":"http://example.com/page3","title":"Page 3","content":"..."}

レスポンスフィールド
--------------------

デフォルトで含まれる主なフィールド:

- ``url``: ドキュメントのURL
- ``title``: タイトル
- ``content``: 本文(抜粋)
- ``score``: 検索スコア
- ``boost``: ブースト値
- ``created``: 作成日時
- ``last_modified``: 最終更新日時

データ処理例
============

Pythonでの処理例
----------------

.. code-block:: python

    import requests
    import json

    # スクロール検索の実行
    url = "http://localhost:8080/json/scroll"
    params = {
        "q": "Fess",
        "size": 100
    }

    response = requests.get(url, params=params, stream=True)

    # NDJSON形式のレスポンスを1行ずつ処理
    for line in response.iter_lines():
        if line:
            doc = json.loads(line)
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

ファイルへの保存
----------------

検索結果をファイルに保存する例:

.. code-block:: bash

    curl "http://localhost:8080/json/scroll?q=*:*" > all_documents.ndjson

CSVへの変換
-----------

jqコマンドを使用してCSVに変換する例:

.. code-block:: bash

    curl "http://localhost:8080/json/scroll?q=Fess" | \
        jq -r '[.url, .title, .score] | @csv' > results.csv

データ分析
----------

取得したデータを分析する例:

.. code-block:: python

    import json
    import pandas as pd
    from collections import Counter

    # NDJSONファイルの読み込み
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            documents.append(json.loads(line))

    # DataFrameに変換
    df = pd.DataFrame(documents)

    # 基本統計
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # URLのドメイン分析
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

パフォーマンスとベストプラクティス
==================================

効率的な使用方法
----------------

1. **適切なsizeパラメータの設定**

   - 小さすぎると通信オーバーヘッドが増加
   - 大きすぎるとメモリ使用量が増加
   - 推奨: 100〜1000

2. **検索条件の最適化**

   - 必要なドキュメントのみを取得するよう検索条件を指定
   - 全件取得は本当に必要な場合のみ実行

3. **オフピーク時間の利用**

   - 大量データの取得は、システムの負荷が低い時間帯に実行

4. **バッチ処理での利用**

   - 定期的なデータ同期などはバッチジョブとして実行

メモリ使用量の最適化
--------------------

大量のデータを処理する場合、ストリーミング処理を使用してメモリ使用量を抑制します。

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/json/scroll"
    params = {"q": "*:*", "size": 100}

    # ストリーミングで処理
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                doc = json.loads(line)
                # ドキュメントの処理
                process_document(doc)

セキュリティ考慮事項
====================

アクセス制限
------------

スクロール検索は大量のデータを返すため、適切なアクセス制限を設定してください。

1. **IPアドレス制限**

   特定のIPアドレスからのみアクセスを許可

2. **API認証**

   APIトークンやBasic認証を使用

3. **ロールベース制限**

   特定のロールを持つユーザーのみアクセスを許可

レート制限
----------

過度なアクセスを防ぐため、リバースプロキシでレート制限を設定することを推奨します。

トラブルシューティング
======================

スクロール検索が利用できない
----------------------------

1. ``api.search.scroll`` が ``true`` に設定されているか確認してください。
2. |Fess| を再起動したか確認してください。
3. エラーログを確認してください。

タイムアウトエラーが発生する
----------------------------

1. ``api.search.scroll.timeout`` の値を増やしてください。
2. ``size`` パラメータを小さくして、処理を分散してください。
3. 検索条件を絞り込んで、取得するデータ量を減らしてください。

メモリ不足エラー
----------------

1. ``size`` パラメータを小さくしてください。
2. |Fess| のヒープメモリサイズを増やしてください。
3. OpenSearch のヒープメモリサイズを確認してください。

レスポンスが空になる
--------------------

1. 検索クエリが正しいか確認してください。
2. 指定したラベルやフィルタ条件が正しいか確認してください。
3. ロールベース検索の権限設定を確認してください。

参考情報
========

- :doc:`search` - 検索機能の詳細
- :doc:`search-config` - 検索関連の設定
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
