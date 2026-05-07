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
有効にするには、 ``app/WEB-INF/classes/fess_config.properties`` または ``/etc/fess/fess_config.properties`` で
以下の設定を変更します。

::

    api.search.scroll=true

.. note::
   設定変更後は、|Fess| を再起動する必要があります。

スクロールタイムアウトの設定
----------------------------

スクロールコンテキストの有効時間はサーバー側の設定で制御されます。
デフォルトは ``3m`` (3分)です。

::

    index.scroll.search.timeout=3m

レスポンスフィールドの設定
--------------------------

検索結果のレスポンスに含めるフィールドをカスタマイズできます。
デフォルトで多数のフィールドが返されますが、追加のフィールドを指定することもできます。

::

    query.additional.scroll.response.fields=content

複数のフィールドを指定する場合は、カンマ区切りで列挙します。

.. note::
   ``content`` フィールドはデフォルトのレスポンスには含まれません。
   全文を取得する場合は上記設定で追加してください。

使用方法
========

基本的な使用方法
----------------

スクロール検索へのアクセスは、以下のURLで実行します。

::

    http://localhost:8080/api/v1/documents/all?q=検索キーワード

検索結果は NDJSON(Newline Delimited JSON)形式で返却されます。
1行ごとに1つのドキュメントがJSON形式で出力されます。

**例:**

::

    curl "http://localhost:8080/api/v1/documents/all?q=Fess"

リクエストパラメータ
--------------------

スクロール検索では、以下のパラメータを使用できます。

.. note::
   スクロール検索は GET メソッドのみ対応しています。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - パラメータ名
     - 説明
   * - ``q``
     - 検索クエリ(必須)
   * - ``num``
     - 1回のスクロールで取得する件数(デフォルト: 10、最大: 100)
   * - ``fields.label``
     - ラベルによるフィルタリング

.. note::
   ``num`` の最大値は ``paging.search.page.max.size`` (デフォルト: 100)で制御されます。
   最大値を超える値を指定した場合、自動的に最大値に切り詰められます。

検索クエリの指定
----------------

通常の検索と同じように、検索クエリを指定できます。

**例: キーワード検索**

::

    curl "http://localhost:8080/api/v1/documents/all?q=検索エンジン"

**例: フィールド指定検索**

::

    curl "http://localhost:8080/api/v1/documents/all?q=title:Fess"

**例: 全件取得(検索条件なし)**

::

    curl "http://localhost:8080/api/v1/documents/all?q=*:*"

取得件数の指定
--------------

1回のスクロールで取得する件数を変更できます。

::

    curl "http://localhost:8080/api/v1/documents/all?q=Fess&num=100"

.. note::
   ``num`` パラメータを大きくしすぎると、メモリ使用量が増加します。
   デフォルトの最大値は100です。より大きな値が必要な場合は
   ``paging.search.page.max.size`` の設定を変更してください。

ラベルによるフィルタリング
--------------------------

特定のラベルに属するドキュメントのみを取得できます。

::

    curl "http://localhost:8080/api/v1/documents/all?q=*:*&fields.label=public"

認証について
------------

.. warning::
   スクロール検索では、|Fess| のロールベースアクセス制御(RBAC)は適用されません。
   検索条件に一致するすべてのドキュメントがユーザーの権限に関係なく返されます。
   アクセス制限が必要な場合は、リバースプロキシ等でIPアドレス制限や認証を設定してください。

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

デフォルトで含まれるフィールド:

- ``score``: 検索スコア
- ``id``: ドキュメントID
- ``doc_id``: ドキュメントID(内部)
- ``boost``: ブースト値
- ``content_length``: コンテンツ長
- ``host``: ホスト名
- ``site``: サイト
- ``last_modified``: 最終更新日時
- ``timestamp``: タイムスタンプ
- ``mimetype``: MIMEタイプ
- ``filetype``: ファイルタイプ
- ``filename``: ファイル名
- ``created``: 作成日時
- ``title``: タイトル
- ``digest``: 本文抜粋
- ``url``: ドキュメントのURL
- ``thumbnail``: サムネイル
- ``click_count``: クリック数
- ``favorite_count``: お気に入り数
- ``config_id``: 設定ID
- ``lang``: 言語
- ``has_cache``: キャッシュ有無

.. note::
   ``content`` (全文)はデフォルトでは含まれません。
   ``query.additional.scroll.response.fields`` で追加できます。

データ処理例
============

Pythonでの処理例
----------------

.. code-block:: python

    import requests
    import json

    # スクロール検索の実行
    url = "http://localhost:8080/api/v1/documents/all"
    params = {
        "q": "Fess",
        "num": 100
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

    curl "http://localhost:8080/api/v1/documents/all?q=*:*" > all_documents.ndjson

CSVへの変換
-----------

jqコマンドを使用してCSVに変換する例:

.. code-block:: bash

    curl "http://localhost:8080/api/v1/documents/all?q=Fess" | \
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

1. **適切なnumパラメータの設定**

   - 小さすぎると通信オーバーヘッドが増加
   - 大きすぎるとメモリ使用量が増加
   - デフォルトの最大値: 100

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

    url = "http://localhost:8080/api/v1/documents/all"
    params = {"q": "*:*", "num": 100}

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

1. ``num`` パラメータを小さくして、処理を分散してください。
2. 検索条件を絞り込んで、取得するデータ量を減らしてください。

メモリ不足エラー
----------------

1. ``num`` パラメータを小さくしてください。
2. |Fess| のヒープメモリサイズを増やしてください。
3. OpenSearch のヒープメモリサイズを確認してください。

レスポンスが空になる
--------------------

1. 検索クエリが正しいか確認してください。
2. 指定したラベルやフィルタ条件が正しいか確認してください。
3. ロールベース検索の権限設定を確認してください。

参考情報
========

- :doc:`search-basic` - 検索機能の詳細
- :doc:`search-advanced` - 検索関連の設定
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
