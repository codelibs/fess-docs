==================================
JSONコネクタ
==================================

概要
====

JSONコネクタは、JSONファイルまたはJSON APIからデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-json`` プラグインが必要です。

前提条件
========

1. プラグインのインストールが必要です
2. JSONファイルまたはAPIへのアクセス権が必要です
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

    file_path=/path/to/data.json
    encoding=UTF-8
    json_path=$

HTTPファイル:

::

    file_path=https://api.example.com/products.json
    encoding=UTF-8
    json_path=$.data

REST API（認証あり）:

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=your_api_token_here

複数ファイル:

::

    file_path=/path/to/data1.json,https://api.example.com/data2.json
    encoding=UTF-8
    json_path=$

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``file_path``
     - はい
     - JSONファイルのパス、またはAPI URL（複数指定可：カンマ区切り）
   * - ``encoding``
     - いいえ
     - 文字エンコーディング（デフォルト: UTF-8）
   * - ``json_path``
     - いいえ
     - JSONPathによるデータ抽出パス（デフォルト: ``$``）
   * - ``http_method``
     - いいえ
     - HTTPメソッド（GET、POST等、デフォルト: GET）
   * - ``auth_type``
     - いいえ
     - 認証タイプ（bearer、basic）
   * - ``auth_token``
     - いいえ
     - 認証トークン（bearer認証の場合）
   * - ``auth_username``
     - いいえ
     - 認証ユーザー名（basic認証の場合）
   * - ``auth_password``
     - いいえ
     - 認証パスワード（basic認証の場合）
   * - ``http_headers``
     - いいえ
     - カスタムHTTPヘッダー（JSON形式）

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

パラメーター:

::

    json_path=$

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

パラメーター:

::

    json_path=$.data.products

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

パラメーター:

::

    json_path=$.articles

スクリプト:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    author=data.author.name
    tags=data.tags.join(", ")

JSONPath の使用
===============

JSONPathとは
------------

JSONPathは、JSON内の要素を指定するためのクエリ言語です。
XMLにおけるXPathに相当します。

基本的な構文
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 構文
     - 説明
   * - ``$``
     - ルート要素
   * - ``$.field``
     - トップレベルのフィールド
   * - ``$.parent.child``
     - ネストしたフィールド
   * - ``$.array[0]``
     - 配列の最初の要素
   * - ``$.array[*]``
     - 配列のすべての要素
   * - ``$..field``
     - 再帰的な検索

JSONPath の例
-------------

全要素を対象（ルート）:

::

    json_path=$

特定の配列を対象:

::

    json_path=$.data.items

ネストした配列:

::

    json_path=$.response.results.products

再帰的な検索:

::

    json_path=$..products

使用例
======

製品カタログAPI
---------------

APIレスポンス:

::

    {
      "status": "success",
      "data": {
        "products": [
          {
            "product_id": "P001",
            "name": "ノートPC",
            "description": "高性能ノートパソコン",
            "price": 120000,
            "category": "パソコン",
            "in_stock": true
          }
        ]
      }
    }

パラメーター:

::

    file_path=https://api.example.com/products
    encoding=UTF-8
    json_path=$.data.products

スクリプト:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " 価格: " + data.price + "円"
    digest=data.category
    price=data.price

ブログ記事API
-------------

APIレスポンス:

::

    {
      "posts": [
        {
          "id": 1,
          "title": "記事タイトル",
          "body": "記事の本文...",
          "author": {
            "name": "山田太郎",
            "email": "yamada@example.com"
          },
          "tags": ["技術", "プログラミング"],
          "published_at": "2024-01-15T10:00:00Z"
        }
      ]
    }

パラメーター:

::

    file_path=https://blog.example.com/api/posts
    encoding=UTF-8
    json_path=$.posts

スクリプト:

::

    url="https://blog.example.com/post/" + data.id
    title=data.title
    content=data.body
    author=data.author.name
    tags=data.tags.join(", ")
    created=data.published_at

Bearer認証のAPI
---------------

パラメーター:

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

スクリプト:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.description

Basic認証のAPI
--------------

パラメーター:

::

    file_path=https://api.example.com/data
    encoding=UTF-8
    json_path=$.data
    http_method=GET
    auth_type=basic
    auth_username=apiuser
    auth_password=password123

スクリプト:

::

    url="https://example.com/data/" + data.id
    title=data.name
    content=data.content

カスタムヘッダーを使用
----------------------

パラメーター:

::

    file_path=https://api.example.com/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    http_headers={"X-API-Key":"your-api-key","Accept":"application/json"}

スクリプト:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

複数JSONファイルの統合
---------------------

パラメーター:

::

    file_path=/var/data/data1.json,/var/data/data2.json,https://api.example.com/data3.json
    encoding=UTF-8
    json_path=$.items

スクリプト:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

POSTリクエスト
--------------

パラメーター:

::

    file_path=https://api.example.com/search
    encoding=UTF-8
    json_path=$.results
    http_method=POST
    http_headers={"Content-Type":"application/json"}
    post_body={"query":"search term","limit":100}

スクリプト:

::

    url="https://example.com/result/" + data.id
    title=data.title
    content=data.content

トラブルシューティング
======================

ファイルが見つからない
----------------------

**症状**: ``FileNotFoundException`` または ``404 Not Found``

**確認事項**:

1. ファイルパスまたはURLが正しいか確認
2. ファイルが存在するか確認
3. URLの場合、APIが稼働しているか確認
4. ネットワーク接続を確認

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

JSONPathエラー
--------------

**症状**: データが取得できない、または空の結果

**確認事項**:

1. JSONPath構文が正しいか確認
2. 対象の要素が存在するか確認
3. JSONPath をテストツールで検証:

   ::

       # jqを使用した確認
       cat data.json | jq '$.data.products'

4. パスが正しい階層を指しているか確認

認証エラー
----------

**症状**: ``401 Unauthorized`` または ``403 Forbidden``

**確認事項**:

1. 認証タイプが正しいか確認（bearer、basic）
2. 認証トークンまたはユーザー名/パスワードが正しいか確認
3. トークンの有効期限を確認
4. APIの権限設定を確認

データが取得できない
--------------------

**症状**: クロールは成功するが件数が0

**確認事項**:

1. JSONPath が正しい要素を指しているか確認
2. JSON構造を確認
3. スクリプト設定が正しいか確認
4. フィールド名が正しいか確認（大文字小文字を含む）
5. ログでエラーメッセージを確認

配列の処理
----------

JSONが配列の場合:

::

    [
      {"id": 1, "name": "Item 1"},
      {"id": 2, "name": "Item 2"}
    ]

パラメーター:

::

    json_path=$

JSONがオブジェクトで配列を含む場合:

::

    {
      "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
      ]
    }

パラメーター:

::

    json_path=$.items

大きなJSONファイル
------------------

**症状**: メモリ不足またはタイムアウト

**解決方法**:

1. JSONファイルを複数に分割
2. JSONPath で必要な部分のみを抽出
3. APIの場合、ページネーションを使用
4. |Fess| のヒープサイズを増やす

APIレート制限
-------------

**症状**: ``429 Too Many Requests``

**解決方法**:

1. クロール間隔を長くする
2. APIのレート制限を確認
3. 複数のAPIキーを使用して負荷分散

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
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
