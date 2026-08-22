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

.. note::

   すべてのエンドポイントには管理者権限と有効なアクセストークンが必要です。
   認証方法については :doc:`api-admin-overview` を参照してください。

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
=======================

リクエスト
----------

::

    GET /api/admin/webconfig/settings

.. note::

   一覧取得エンドポイントは ``GET`` に加えて ``PUT`` でもアクセスできます。

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始、デフォルト: 1）
   * - ``size``
     - Integer
     - いいえ
     - 1ページあたりの件数（デフォルト: 25。\ ``paging.page.size`` 設定に従います）
   * - ``name``
     - String
     - いいえ
     - 設定名による絞り込み
   * - ``urls``
     - String
     - いいえ
     - クロールURLによる絞り込み
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

``total`` は条件に一致する設定の総件数を表します。

Webクロール設定取得
===================

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
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   レスポンスには、登録・更新時に自動設定される ``createdBy`` 、 ``createdTime`` 、
   ``updatedBy`` 、 ``updatedTime`` 、 ``versionNo`` が含まれます。
   ``versionNo`` は更新時に必要です（後述の「Webクロール設定更新」を参照）。

Webクロール設定作成
===================

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
      "permissions": "{role}admin\n{role}user"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - 設定名（最大200文字）
   * - ``description``
     - いいえ
     - 設定の説明（最大1000文字）
   * - ``urls``
     - はい
     - クロール開始URL（複数の場合は改行区切り）。\ ``http:`` または ``https:`` で指定します
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
     - 追加設定パラメーター（``key=value`` 形式、1行に1項目）
   * - ``depth``
     - いいえ
     - クロール深度（0以上）
   * - ``maxAccessCount``
     - いいえ
     - 最大アクセス数（0以上）
   * - ``userAgent``
     - はい
     - User-Agent文字列（最大200文字）
   * - ``numOfThread``
     - はい
     - 並列スレッド数（1以上）
   * - ``intervalTime``
     - はい
     - アクセス間隔（ミリ秒、0以上）
   * - ``boost``
     - はい
     - 検索結果のブースト値
   * - ``available``
     - はい
     - 有効/無効（文字列 ``"true"`` / ``"false"``）
   * - ``sortOrder``
     - はい
     - 表示順序（0以上）
   * - ``permissions``
     - いいえ
     - アクセス許可ロール（複数の場合は改行区切り）
   * - ``virtualHosts``
     - いいえ
     - 仮想ホスト（複数の場合は改行区切り）

.. note::

   ``createdBy`` 、 ``createdTime`` 、 ``updatedBy`` 、 ``updatedTime`` などの監査用フィールドは
   サーバー側で自動設定されるため、リクエストボディで指定する必要はありません。

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
===================

リクエスト
----------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

更新時は、作成時のフィールドに加えて、更新対象を特定する ``id`` とバージョン番号 ``versionNo`` が必須です。
``versionNo`` には取得API（GET）のレスポンスに含まれる現在の値を指定します。

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

更新時の追加フィールド
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - フィールド
     - 必須
     - 説明
   * - ``id``
     - はい
     - 更新対象の設定ID（最大1000文字）
   * - ``versionNo``
     - はい
     - 更新対象の現在のバージョン番号。取得API（GET）のレスポンスに含まれる ``versionNo`` を指定します

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
===================

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

``includedUrls`` / ``excludedUrls`` / ``includedDocUrls`` / ``excludedDocUrls`` には正規表現を指定します。

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
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-fileconfig` - ファイルクロール設定API
- :doc:`api-admin-dataconfig` - データストア設定API
- :doc:`../../admin/webconfig-guide` - Webクロール設定ガイド
