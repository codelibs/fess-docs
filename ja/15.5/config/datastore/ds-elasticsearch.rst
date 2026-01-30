==================================
Elasticsearch/OpenSearchコネクタ
==================================

概要
====

Elasticsearch/OpenSearchコネクタは、ElasticsearchまたはOpenSearchクラスタからデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-elasticsearch`` プラグインが必要です。

対応バージョン
==============

- Elasticsearch 7.x / 8.x
- OpenSearch 1.x / 2.x

前提条件
========

1. プラグインのインストールが必要です
2. Elasticsearch/OpenSearchクラスタへの読み取りアクセスが必要です
3. クエリを実行できる権限が必要です

プラグインのインストール
------------------------

方法1: JARファイルを直接配置

::

    # Maven Centralからダウンロード
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-elasticsearch/X.X.X/fess-ds-elasticsearch-X.X.X.jar

    # 配置
    cp fess-ds-elasticsearch-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    cp fess-ds-elasticsearch-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

方法2: 管理画面からインストール

1. 「システム」→「プラグイン」を開く
2. JARファイルをアップロード
3. |Fess| を再起動

設定方法
========

管理画面から「クローラー」→「データストア」→「新規作成」で設定します。

基本設定
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 設定例
   * - 名前
     - External Elasticsearch
   * - ハンドラ名
     - ElasticsearchDataStore
   * - 有効
     - オン

パラメーター設定
----------------

基本的な接続:

::

    hosts=http://localhost:9200
    index=myindex
    scroll_size=100
    scroll_timeout=5m

認証ありの接続:

::

    hosts=https://elasticsearch.example.com:9200
    index=myindex
    username=elastic
    password=changeme
    scroll_size=100
    scroll_timeout=5m

複数ホストの設定:

::

    hosts=http://es-node1:9200,http://es-node2:9200,http://es-node3:9200
    index=myindex
    scroll_size=100
    scroll_timeout=5m

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``hosts``
     - はい
     - Elasticsearch/OpenSearchのホスト（カンマ区切りで複数指定可）
   * - ``index``
     - はい
     - 対象インデックス名
   * - ``username``
     - いいえ
     - 認証用ユーザー名
   * - ``password``
     - いいえ
     - 認証用パスワード
   * - ``scroll_size``
     - いいえ
     - スクロール時の取得件数（デフォルト: 100）
   * - ``scroll_timeout``
     - いいえ
     - スクロールのタイムアウト（デフォルト: 5m）
   * - ``query``
     - いいえ
     - クエリJSON（デフォルト: match_all）
   * - ``fields``
     - いいえ
     - 取得するフィールド（カンマ区切り）

スクリプト設定
--------------

基本的なマッピング:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

ネストしたフィールドへのアクセス:

::

    url=data.metadata.url
    title=data.title
    content=data.body.content
    author=data.author.name
    created=data.created_at
    last_modified=data.updated_at

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

- ``data.<field_name>`` - Elasticsearchドキュメントのフィールド
- ``data._id`` - ドキュメントID
- ``data._index`` - インデックス名
- ``data._type`` - ドキュメントタイプ（Elasticsearch 7未満）
- ``data._score`` - 検索スコア

クエリの設定
============

全ドキュメントの取得
--------------------

デフォルトでは全ドキュメントが取得されます。
``query`` パラメーターを指定しない場合、``match_all`` が使用されます。

特定の条件でフィルタリング
--------------------------

::

    query={"query":{"term":{"status":"published"}}}

範囲指定:

::

    query={"query":{"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}}

複数条件:

::

    query={"query":{"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}}

ソート指定:

::

    query={"query":{"match_all":{}},"sort":[{"timestamp":{"order":"desc"}}]}

特定のフィールドのみ取得
========================

fieldsパラメーターで取得フィールドを限定
----------------------------------------

::

    hosts=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    scroll_size=100

すべてのフィールドを取得する場合は ``fields`` を指定しないか、空にします。

使用例
======

基本的なインデックスのクロール
------------------------------

パラメーター:

::

    hosts=http://localhost:9200
    index=articles
    scroll_size=100
    scroll_timeout=5m

スクリプト:

::

    url=data.url
    title=data.title
    content=data.content
    created=data.created_at
    last_modified=data.updated_at

認証付きクラスタからのクロール
------------------------------

パラメーター:

::

    hosts=https://es.example.com:9200
    index=products
    username=elastic
    password=changeme
    scroll_size=200
    scroll_timeout=10m

スクリプト:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " " + data.specifications
    digest=data.category
    last_modified=data.updated_at

複数インデックスからのクロール
------------------------------

パラメーター:

::

    hosts=http://localhost:9200
    index=logs-2024-*
    query={"query":{"term":{"level":"error"}}}
    scroll_size=100

スクリプト:

::

    url="https://logs.example.com/view/" + data._id
    title=data.message
    content=data.stack_trace
    digest=data.service + " - " + data.level
    last_modified=data.timestamp

OpenSearchクラスタのクロール
----------------------------

パラメーター:

::

    hosts=https://opensearch.example.com:9200
    index=documents
    username=admin
    password=admin
    scroll_size=100
    scroll_timeout=5m

スクリプト:

::

    url=data.url
    title=data.title
    content=data.body
    last_modified=data.modified_date

フィールドを限定してクロール
----------------------------

パラメーター:

::

    hosts=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    scroll_size=100

スクリプト:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

複数ホストでの負荷分散
----------------------

パラメーター:

::

    hosts=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    scroll_size=100
    scroll_timeout=5m

スクリプト:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

トラブルシューティング
======================

接続エラー
----------

**症状**: ``Connection refused`` または ``No route to host``

**確認事項**:

1. ホストURLが正しいか確認（プロトコル、ホスト名、ポート）
2. Elasticsearch/OpenSearchが起動しているか確認
3. ファイアウォール設定を確認
4. HTTPSの場合、証明書が有効か確認

認証エラー
----------

**症状**: ``401 Unauthorized`` または ``403 Forbidden``

**確認事項**:

1. ユーザー名とパスワードが正しいか確認
2. ユーザーに適切な権限があるか確認:

   - インデックスへの読み取り権限
   - スクロールAPIの使用権限

3. Elasticsearch Security（X-Pack）が有効な場合、適切に設定されているか確認

インデックスが見つからない
--------------------------

**症状**: ``index_not_found_exception``

**確認事項**:

1. インデックス名が正しいか確認（大文字小文字を含む）
2. インデックスが存在するか確認:

   ::

       GET /_cat/indices

3. ワイルドカードパターンが正しいか確認（例: ``logs-*``）

クエリエラー
------------

**症状**: ``parsing_exception`` または ``search_phase_execution_exception``

**確認事項**:

1. クエリJSONが正しいか確認
2. Elasticsearch/OpenSearchのバージョンに対応したクエリか確認
3. フィールド名が正しいか確認
4. クエリを直接Elasticsearch/OpenSearchで実行してテスト:

   ::

       POST /myindex/_search
       {
         "query": {...}
       }

スクロールタイムアウト
----------------------

**症状**: ``No search context found`` または ``Scroll timeout``

**解決方法**:

1. ``scroll_timeout`` を長くする:

   ::

       scroll_timeout=10m

2. ``scroll_size`` を小さくする:

   ::

       scroll_size=50

3. クラスタのリソースを確認

大量データのクロール
--------------------

**症状**: クロールが遅い、またはタイムアウトする

**解決方法**:

1. ``scroll_size`` を調整（大きすぎると遅くなる）:

   ::

       scroll_size=100  # デフォルト
       scroll_size=500  # 大きめ

2. ``fields`` で取得フィールドを限定
3. ``query`` で必要なドキュメントのみフィルタリング
4. 複数のデータストアに分割（インデックス単位、時間範囲単位など）

メモリ不足
----------

**症状**: OutOfMemoryError

**解決方法**:

1. ``scroll_size`` を小さくする
2. ``fields`` で取得フィールドを限定
3. |Fess| のヒープサイズを増やす
4. 大きなフィールド（バイナリデータなど）を除外

SSL/TLS接続
===========

自己署名証明書の場合
--------------------

.. warning::
   本番環境では適切に署名された証明書を使用してください。

自己署名証明書を使用する場合、Java keystoreに証明書を追加:

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

クライアント証明書認証
----------------------

クライアント証明書が必要な場合、追加のパラメーター設定が必要です。
詳細はElasticsearchクライアントのドキュメントを参照してください。

高度なクエリ例
==============

集約を含むクエリ
----------------

.. note::
   集約結果は取得されず、ドキュメントのみが取得されます。

::

    query={"query":{"match_all":{}},"aggs":{"categories":{"terms":{"field":"category"}}}}

スクリプトフィールド
--------------------

::

    query={"query":{"match_all":{}},"script_fields":{"full_url":{"script":"doc['protocol'].value + '://' + doc['host'].value + doc['path'].value"}}}

スクリプト:

::

    url=data.full_url
    title=data.title
    content=data.content

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-database` - データベースコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
