==================================
JSONコネクタ
==================================

概要
====

JSONコネクタは、ローカルのJSONファイルやJSONLファイルからデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-json`` プラグインが必要です。

前提条件
========

1. プラグインのインストールが必要です
2. JSONファイルへのアクセス権が必要です
3. JSONの構造を理解している必要があります

プラグインのインストール
------------------------

方法1: JARファイルを直接配置

::

    # Maven Centralからダウンロード
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # 配置
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Products JSON
   * - ハンドラ名
     - JsonDataStore
   * - 有効
     - オン

パラメーター設定
----------------

ローカルファイル:

::

    files=/path/to/data.json
    fileEncoding=UTF-8

複数ファイル:

::

    files=/path/to/data1.json,/path/to/data2.json
    fileEncoding=UTF-8

ディレクトリ指定:

::

    directories=/path/to/json_dir/
    fileEncoding=UTF-8

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - パラメーター
     - 必須
     - 説明
   * - ``files``
     - いいえ
     - JSONファイルのパス（複数指定可：カンマ区切り）
   * - ``directories``
     - いいえ
     - JSONファイルを含むディレクトリのパス
   * - ``fileEncoding``
     - いいえ
     - 文字エンコーディング（デフォルト: UTF-8）

.. warning::
   ``files`` または ``directories`` のいずれかを指定する必要があります。
   両方が未指定の場合、 ``DataStoreException`` が発生します。
   両方を指定した場合、 ``files`` が優先され ``directories`` は無視されます。

.. note::
   このコネクタはローカルファイルシステム上のJSONファイルのみを対象とし、HTTPアクセスやAPI認証機能はサポートしていません。

スクリプト設定
--------------

単純なJSONオブジェクト:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price
    category=data.category

ネストしたJSONオブジェクト:

::

    url="https://example.com/product/" + data.id
    title=data.product.name
    content=data.product.description
    price=data.product.pricing.amount
    author=data.product.author.name

配列要素の処理:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.body
    tags=data.tags.join(", ")
    categories=data.categories[0].name

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

- ``data.<フィールド名>`` - JSONオブジェクトのフィールド
- ``data.<親>.<子>`` - ネストしたオブジェクト
- ``data.<配列>[<インデックス>]`` - 配列要素
- ``data.<配列>.<メソッド>`` - 配列のメソッド（join、lengthなど）

JSON形式の詳細
==============

JSONファイル形式
----------------

JSONコネクタは、JSONL（JSON Lines）形式のファイルを読み込みます。
1行に1つのJSONオブジェクトを記述する形式です。

.. note::
   配列形式のJSONファイル（ ``[{...}, {...}]`` ）は直接読み込めません。
   JSONL形式に変換してください。

JSONL形式のファイル:

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

使用例
======

製品カタログ
--------------

パラメーター:

::

    files=/var/data/products.json
    fileEncoding=UTF-8

スクリプト:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " 価格: " + data.price + "円"
    digest=data.category
    price=data.price

複数JSONファイルの統合
---------------------

パラメーター:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

スクリプト:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

トラブルシューティング
======================

ファイルが見つからない
----------------------

**症状**: ``FileNotFoundException``

**確認事項**:

1. ファイルパスが正しいか確認
2. ファイルが存在するか確認
3. ファイルの読み取り権限があるか確認

JSON解析エラー
--------------

**症状**: ``JsonParseException`` または ``Unexpected character``

**確認事項**:

1. JSONファイルが正しい形式か確認:

   ::

       # JSONの検証
       cat data.json | jq .

2. 文字エンコーディングが正しいか確認
3. 不正な文字や改行がないか確認
4. コメントが含まれていないか確認（JSON標準ではコメント不可）

データが取得できない
--------------------

**症状**: クロールは成功するが件数が0

**確認事項**:

1. JSON構造を確認
2. スクリプト設定が正しいか確認
3. フィールド名が正しいか確認（大文字小文字を含む）
4. ログでエラーメッセージを確認

大きなJSONファイル
------------------

**症状**: メモリ不足またはタイムアウト

**解決方法**:

1. JSONファイルを複数に分割
2. |Fess| のヒープサイズを増やす

スクリプトの高度な使用例
========================

条件付き処理
------------

各フィールドは独立した式として評価されます。条件付きの値は三項演算子を使用します:

::

    url=data.status == "published" ? "https://example.com/product/" + data.id : null
    title=data.status == "published" ? data.name : null
    content=data.status == "published" ? data.description : null
    price=data.status == "published" ? data.price : null

配列の結合
----------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.collect { it.name }.join(", ")

デフォルト値の設定
------------------

::

    url="https://example.com/item/" + data.id
    title=data.title ?: "無題"
    content=data.description ?: (data.summary ?: "説明なし")
    price=data.price ?: 0

日付のフォーマット
------------------

::

    url="https://example.com/post/" + data.id
    title=data.title
    content=data.body
    created=data.created_at
    last_modified=data.updated_at

数値の処理
----------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price as Float
    stock=data.stock_quantity as Integer

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-csv` - CSVコネクタ
- :doc:`ds-database` - データベースコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
