==================================
JSONコネクタ
==================================

概要
====

JSONコネクタは、ローカルのJSONファイルからデータを取得して
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

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``files``
     - はい
     - JSONファイルのパス（複数指定可：カンマ区切り）
   * - ``fileEncoding``
     - いいえ
     - 文字エンコーディング（デフォルト: UTF-8）

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

単純な配列
----------

::

    [
      {
        "id": 1,
        "name": "Product A",
        "description": "Description A",
        "price": 1000
      },
      {
        "id": 2,
        "name": "Product B",
        "description": "Description B",
        "price": 2000
      }
    ]

ネストした構造
--------------

::

    {
      "data": {
        "products": [
          {
            "id": 1,
            "name": "Product A",
            "details": {
              "description": "Description A",
              "price": 1000,
              "category": {
                "id": 10,
                "name": "Electronics"
              }
            }
          }
        ]
      }
    }

スクリプト:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.details.description
    price=data.details.price
    category=data.details.category.name

複雑な配列
----------

::

    {
      "articles": [
        {
          "id": 1,
          "title": "Article 1",
          "content": "Content 1",
          "tags": ["tag1", "tag2", "tag3"],
          "author": {
            "name": "John Doe",
            "email": "john@example.com"
          }
        }
      ]
    }

スクリプト:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    author=data.author.name
    tags=data.tags.join(", ")

使用例
======

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

**症状**: ``FileNotFoundException`` または ``No such file``

**確認事項**:

1. ファイルパスが正しいか確認（絶対パス推奨）
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
4. フィールド名が正しいか確認（大文字小文字を含む）
5. ログでエラーメッセージを確認

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

::

    if (data.status == "published" && data.price > 1000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

配列の結合
----------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.map(function(c) { return c.name; }).join(", ")

デフォルト値の設定
------------------

::

    url="https://example.com/item/" + data.id
    title=data.title || "無題"
    content=data.description || data.summary || "説明なし"
    price=data.price || 0

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
    price=parseFloat(data.price)
    stock=parseInt(data.stock_quantity)

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-csv` - CSVコネクタ
- :doc:`ds-database` - データベースコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
