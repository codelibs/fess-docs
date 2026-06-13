==========================
FailureUrl API
==========================

概要
====

FailureUrl APIは、|Fess| のクロール障害URLを管理するためのAPIです。
クロール中にエラーが発生したURLの一覧取得、個別取得、削除などを操作できます。

ベースURL
=========

::

    /api/admin/failureurl

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /logs
     - 障害URL一覧取得
   * - GET
     - /log/{id}
     - 障害URL取得
   * - DELETE
     - /log/{id}
     - 障害URL削除
   * - DELETE
     - /all
     - 全障害URL削除

障害URL一覧取得
===============

リクエスト
----------

::

    GET /api/admin/failureurl/logs

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
     - 1ページあたりの件数
   * - ``page``
     - Integer
     - いいえ
     - ページ番号
   * - ``url``
     - String
     - いいえ
     - URLフィルター
   * - ``errorCountMin``
     - Integer
     - いいえ
     - 最小エラー回数フィルター
   * - ``errorCountMax``
     - Integer
     - いいえ
     - 最大エラー回数フィルター
   * - ``errorName``
     - String
     - いいえ
     - エラー名フィルター

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "threadName": "Crawler-1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": 1738144800000,
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": 1738143000000,
            "configId": "webConfig_id_1"
          }
        ],
        "total": 45
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``id``
     - 障害URL ID
   * - ``url``
     - 失敗したURL
   * - ``threadName``
     - スレッド名
   * - ``errorName``
     - エラー名
   * - ``errorLog``
     - エラーログ
   * - ``errorCount``
     - エラー発生回数
   * - ``lastAccessTime``
     - 最終アクセス時刻（エポックミリ秒）
   * - ``configId``
     - クロール設定ID

障害URL取得
===========

リクエスト
----------

::

    GET /api/admin/failureurl/log/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "failure_id_1",
          "url": "https://example.com/broken-page",
          "threadName": "Crawler-1",
          "errorName": "ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": 3,
          "lastAccessTime": 1738144800000,
          "configId": "webConfig_id_1"
        }
      }
    }

障害URL削除
===========

リクエスト
----------

::

    DELETE /api/admin/failureurl/log/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

全障害URL削除
=============

すべての障害URLを削除します。パラメーターはありません。

リクエスト
----------

::

    DELETE /api/admin/failureurl/all

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

エラータイプ
============

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エラー名
     - 説明
   * - ``ConnectException``
     - 接続エラー
   * - ``HttpStatusException``
     - HTTPステータスエラー（404, 500など）
   * - ``SocketTimeoutException``
     - タイムアウトエラー
   * - ``UnknownHostException``
     - ホスト名解決エラー
   * - ``SSLException``
     - SSL証明書エラー
   * - ``IOException``
     - 入出力エラー

使用例
======

障害URL一覧の取得
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

エラー回数でフィルター
----------------------

.. code-block:: bash

    # 3回以上エラーが発生したURLのみ取得
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

エラー名でフィルター
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=ConnectException" \
         -H "Authorization: Bearer YOUR_TOKEN"

障害URLの取得
-------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

障害URLの削除
-------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

全障害URLの削除
---------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

エラータイプ別の集計
--------------------

.. code-block:: bash

    # エラータイプごとにカウント
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.logs[].errorName] | group_by(.) | map({error: .[0], count: length})'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-crawlinginfo` - クロール情報API
- :doc:`api-admin-joblog` - ジョブログAPI
- :doc:`../../admin/failureurl-guide` - 障害URL管理ガイド
