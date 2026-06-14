==========================
WebConfig API
==========================

概要
====

WebConfig APIは、|Fess| のWebクロール設定を管理するためのAPIです。
クロール対象のURL、クロール深度、除外パターンなどの設定を操作できます。

ベースURL
=========

::

    /api/admin/webconfig

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
     - Webクロール設定一覧取得
   * - GET
     - /setting/{id}
     - Webクロール設定取得
   * - POST
     - /setting
     - Webクロール設定作成
   * - PUT
     - /setting
     - Webクロール設定更新
   * - DELETE
     - /setting/{id}
     - Webクロール設定削除

Webクロール設定一覧取得
======================

リクエスト
----------

::

    GET /api/admin/webconfig/settings

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

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
            "id": "webconfig_id_1",
            "name": "Example Site",
            "description": "サンプルサイト",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "Mozilla/5.0",
            "numOfThread": 1,
            "intervalTime": 1000,
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

Webクロール設定取得
==================

リクエスト
----------

::

    GET /api/admin/webconfig/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "webconfig_id_1",
          "name": "Example Site",
          "description": "サンプルサイト",
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "Mozilla/5.0",
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "labelTypeIds": []
        }
      }
    }

Webクロール設定作成
==================

リクエスト
----------

::

    POST /api/admin/webconfig/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe)$",
      "userAgent": "Mozilla/5.0",
      "numOfThread": 3,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user",
      "labelTypeIds": ["label_id_1"]
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - 設定名
   * - ``description``
     - いいえ
     - 設定の説明
   * - ``urls``
     - はい
     - クロール開始URL（複数の場合は改行区切り）
   * - ``includedUrls``
     - いいえ
     - クロール対象URLの正規表現パターン
   * - ``excludedUrls``
     - いいえ
     - クロール除外URLの正規表現パターン
   * - ``includedDocUrls``
     - いいえ
     - インデックス対象URLの正規表現パターン
   * - ``excludedDocUrls``
     - いいえ
     - インデックス除外URLの正規表現パターン
   * - ``configParameter``
     - いいえ
     - 追加設定パラメーター
   * - ``depth``
     - いいえ
     - クロール深度
   * - ``maxAccessCount``
     - いいえ
     - 最大アクセス数
   * - ``userAgent``
     - はい
     - User-Agent文字列
   * - ``numOfThread``
     - はい
     - 並列スレッド数
   * - ``intervalTime``
     - はい
     - リクエスト間隔（ミリ秒）
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
   * - ``labelTypeIds``
     - いいえ
     - ラベルタイプID（配列）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_webconfig_id",
        "created": true
      }
    }

Webクロール設定更新
==================

リクエスト
----------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "userAgent": "Mozilla/5.0",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_webconfig_id",
        "created": false
      }
    }

Webクロール設定削除
==================

リクエスト
----------

::

    DELETE /api/admin/webconfig/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

URLパターンの例
===============

includedUrls / excludedUrls
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - パターン
     - 説明
   * - ``.*example\\.com.*``
     - example.comを含むすべてのURL
   * - ``https://example\\.com/docs/.*``
     - /docs/以下のみ
   * - ``.*\\.(pdf|doc|docx)$``
     - PDF、DOC、DOCXファイル
   * - ``.*\\?.*``
     - クエリパラメーター付きURL
   * - ``.*/(login|logout|admin)/.*``
     - 特定のパスを含むURL

使用例
======

企業サイトのクロール設定
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "userAgent": "Mozilla/5.0",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

ドキュメントサイトのクロール設定
--------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "excludedUrls": "",
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0,
           "labelTypeIds": ["documentation_label_id"]
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-fileconfig` - ファイルクロール設定API
- :doc:`api-admin-dataconfig` - データストア設定API
- :doc:`../../admin/webconfig-guide` - Webクロール設定ガイド
