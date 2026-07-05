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
   * - GET/PUT
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
    PUT /api/admin/dataconfig/settings

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
     - 1ページあたりの件数（デフォルト: 20）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（0から開始）

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
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
            "boost": 1.0,
            "available": true,
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
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
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
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description",
      "boost": 1.0,
      "available": true,
      "permissions": ["admin", "user"],
      "labelTypeIds": ["label_id_1"]
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
   * - ``handlerName``
     - はい
     - データストアハンドラー名
   * - ``handlerParameter``
     - いいえ
     - ハンドラーパラメーター（接続情報など）
   * - ``handlerScript``
     - はい
     - データ変換スクリプト
   * - ``boost``
     - いいえ
     - 検索結果のブースト値（デフォルト: 1.0）
   * - ``available``
     - いいえ
     - 有効/無効（デフォルト: true）
   * - ``sortOrder``
     - いいえ
     - 表示順序
   * - ``permissions``
     - いいえ
     - アクセス許可ロール
   * - ``virtualHosts``
     - いいえ
     - 仮想ホスト
   * - ``labelTypeIds``
     - いいえ
     - ラベルタイプID

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
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description + \" \" + data.features",
      "boost": 1.5,
      "available": true,
      "versionNo": 1
    }

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
        "status": 0,
        "id": "deleted_dataconfig_id",
        "created": false
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
     - CSVファイルからデータを読み込み
   * - ``JsonDataStore``
     - JSONファイルまたはJSON APIからデータを読み込み

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
           "handlerScript": "url=\"https://example.com/user/\" + data.user_id\ntitle=data.username\ncontent=data.profile",
           "boost": 1.0,
           "available": true
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-webconfig` - Webクロール設定API
- :doc:`api-admin-fileconfig` - ファイルクロール設定API
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
