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
            "included_urls": ".*example\\.com.*",
            "excluded_urls": ".*\\.(pdf|zip)$",
            "included_doc_urls": "",
            "excluded_doc_urls": "",
            "config_parameter": "",
            "depth": 3,
            "max_access_count": 1000,
            "user_agent": "Mozilla/5.0",
            "num_of_thread": 1,
            "interval_time": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtual_hosts": "",
            "sort_order": 0
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
          "included_urls": ".*example\\.com.*",
          "excluded_urls": ".*\\.(pdf|zip)$",
          "included_doc_urls": "",
          "excluded_doc_urls": "",
          "config_parameter": "",
          "depth": 3,
          "max_access_count": 1000,
          "user_agent": "Mozilla/5.0",
          "num_of_thread": 1,
          "interval_time": 1000,
          "boost": 1.0,
          "available": "true",
          "sort_order": 0,
          "permissions": "{role}admin",
          "virtual_hosts": "",
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   レスポンスには、登録・更新時に自動設定される ``created_by`` 、 ``created_time`` 、
   ``updated_by`` 、 ``updated_time`` 、 ``version_no`` が含まれます。
   ``version_no`` は更新時に必要です（後述の「Webクロール設定更新」を参照）。

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
      "included_urls": ".*www\\.example\\.com.*",
      "excluded_urls": ".*\\.(pdf|zip|exe)$",
      "user_agent": "Mozilla/5.0",
      "num_of_thread": 3,
      "interval_time": 500,
      "boost": 1.0,
      "available": "true",
      "sort_order": 0,
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
   * - ``included_urls``
     - いいえ
     - クロール対象URLの正規表現パターン
   * - ``excluded_urls``
     - いいえ
     - クロール除外URLの正規表現パターン
   * - ``included_doc_urls``
     - いいえ
     - インデックス対象URLの正規表現パターン
   * - ``excluded_doc_urls``
     - いいえ
     - インデックス除外URLの正規表現パターン
   * - ``config_parameter``
     - いいえ
     - 追加設定パラメーター（``key=value`` 形式、1行に1項目）
   * - ``depth``
     - いいえ
     - クロール深度（0以上）
   * - ``max_access_count``
     - いいえ
     - 最大アクセス数（0以上）
   * - ``user_agent``
     - はい
     - User-Agent文字列（最大200文字）
   * - ``num_of_thread``
     - はい
     - 並列スレッド数（1以上）
   * - ``interval_time``
     - はい
     - アクセス間隔（ミリ秒、0以上）
   * - ``boost``
     - はい
     - 検索結果のブースト値
   * - ``available``
     - はい
     - 有効/無効（文字列 ``"true"`` / ``"false"``）
   * - ``sort_order``
     - はい
     - 表示順序（0以上）
   * - ``permissions``
     - いいえ
     - アクセス許可ロール（複数の場合は改行区切り）
   * - ``virtual_hosts``
     - いいえ
     - 仮想ホスト（複数の場合は改行区切り）

.. note::

   ``created_by`` 、 ``created_time`` 、 ``updated_by`` 、 ``updated_time`` などの監査用フィールドは
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

更新時は、作成時のフィールドに加えて、更新対象を特定する ``id`` とバージョン番号 ``version_no`` が必須です。
``version_no`` には取得API（GET）のレスポンスに含まれる現在の値を指定します。

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "included_urls": ".*www\\.example\\.com.*",
      "excluded_urls": ".*\\.(pdf|zip|exe|dmg)$",
      "user_agent": "Mozilla/5.0",
      "depth": 10,
      "max_access_count": 10000,
      "num_of_thread": 5,
      "interval_time": 300,
      "boost": 1.2,
      "available": "true",
      "sort_order": 0,
      "version_no": 1
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
   * - ``version_no``
     - はい
     - 更新対象の現在のバージョン番号。取得API（GET）のレスポンスに含まれる ``version_no`` を指定します

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

``included_urls`` / ``excluded_urls`` / ``included_doc_urls`` / ``excluded_doc_urls`` には正規表現を指定します。

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
           "included_urls": ".*www\\.example\\.com.*",
           "excluded_urls": ".*/(login|admin|api)/.*",
           "user_agent": "Mozilla/5.0",
           "depth": 5,
           "max_access_count": 10000,
           "num_of_thread": 3,
           "interval_time": 500,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
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
           "included_urls": ".*docs\\.example\\.com.*",
           "included_doc_urls": ".*\\.(html|htm)$",
           "user_agent": "Mozilla/5.0",
           "max_access_count": 50000,
           "num_of_thread": 5,
           "interval_time": 200,
           "boost": 1.5,
           "available": "true",
           "sort_order": 0
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-fileconfig` - ファイルクロール設定API
- :doc:`api-admin-dataconfig` - データストア設定API
- :doc:`../../admin/webconfig-guide` - Webクロール設定ガイド
