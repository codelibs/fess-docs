==========================
DataConfig API
==========================

概要
====

DataConfig APIは、|Fess| のデータストア設定を管理するためのAPIです。
データベース、CSV、JSONなどのデータソースのクロール設定を操作できます。

ベースURL
=========

::

    /api/admin/dataconfig

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /settings
     - データストア設定一覧取得
   * - GET
     - /setting/{id}
     - データストア設定取得
   * - POST
     - /setting
     - データストア設定作成
   * - PUT
     - /setting
     - データストア設定更新
   * - DELETE
     - /setting/{id}
     - データストア設定削除

データストア設定一覧取得
========================

リクエスト
----------

::

    GET /api/admin/dataconfig/settings

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``size``
     - Integer
     - いいえ
     - 1ページあたりの件数（デフォルト: 25）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始、デフォルト: 1）
   * - ``name``
     - String
     - いいえ
     - 設定名による絞り込み
   * - ``handlerName``
     - String
     - いいえ
     - ハンドラー名による絞り込み
   * - ``description``
     - String
     - いいえ
     - 説明による絞り込み

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "description": "データベースクローラー",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

データストア設定取得
====================

リクエスト
----------

::

    GET /api/admin/dataconfig/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "dataconfig_id_1",
          "name": "Database Crawler",
          "description": "データベースクローラー",
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": ""
        }
      }
    }

データストア設定作成
====================

リクエスト
----------

::

    POST /api/admin/dataconfig/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=pass",
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description",
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - 設定名
   * - ``description``
     - いいえ
     - 設定の説明
   * - ``handlerName``
     - はい
     - データストアハンドラー名
   * - ``handlerParameter``
     - いいえ
     - ハンドラーパラメーター（接続情報など）
   * - ``handlerScript``
     - いいえ
     - データ変換スクリプト
   * - ``boost``
     - はい
     - 検索結果のブースト値
   * - ``available``
     - はい
     - 有効/無効（文字列 ``"true"`` / ``"false"``）
   * - ``sortOrder``
     - はい
     - 表示順序
   * - ``permissions``
     - いいえ
     - アクセス許可ロール（複数の場合は改行区切り）
   * - ``virtualHosts``
     - いいえ
     - 仮想ホスト（複数の場合は改行区切り）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_dataconfig_id",
        "created": true
      }
    }

データストア設定更新
====================

リクエスト
----------

::

    PUT /api/admin/dataconfig/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_dataconfig_id",
      "name": "Updated Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=newpass",
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description + \" \" + features",
      "boost": 1.5,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

更新リクエストでは、作成時と同じ必須フィールド（``name`` 、 ``handlerName`` 、 ``boost`` 、
``available`` 、 ``sortOrder`` ）に加えて、以下のフィールドが必須です。

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``id``
     - はい
     - 更新対象の設定ID
   * - ``versionNo``
     - はい
     - 楽観ロック用のバージョン番号（取得時の値を指定）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_dataconfig_id",
        "created": false
      }
    }

データストア設定削除
====================

リクエスト
----------

::

    DELETE /api/admin/dataconfig/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

ハンドラータイプ
================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ハンドラー名
     - 説明
   * - ``DatabaseDataStore``
     - JDBC経由でデータベースに接続
   * - ``CsvDataStore``
     - CSVファイルからデータを読み込み（1行を1ドキュメントとして処理）
   * - ``CsvListDataStore``
     - CSVファイルを読み込み、処理済みファイルを自動削除（タイムスタンプによるフィルタリングに対応した ``CsvDataStore`` の拡張）
   * - ``JsonDataStore``
     - JSONファイルまたはJSON APIからデータを読み込み

.. note::

   利用可能なハンドラータイプは、インストールされているデータストアプラグインによって異なります。
   上記は標準で含まれるハンドラーです。SharePoint、Slack、Salesforce などのデータストア
   プラグインを追加すると、それぞれに対応するハンドラー名が利用可能になります。

使用例
======

データベースクロール設定
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dataconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "User Database",
           "handlerName": "DatabaseDataStore",
           "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/userdb\nusername=dbuser\npassword=dbpass\nsql=SELECT * FROM users WHERE active=true",
           "handlerScript": "url=\"https://example.com/user/\" + user_id\ntitle=username\ncontent=profile",
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-webconfig` - Webクロール設定API
- :doc:`api-admin-fileconfig` - ファイルクロール設定API
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
