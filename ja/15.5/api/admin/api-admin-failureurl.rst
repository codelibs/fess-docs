==========================
FailureUrl API
==========================

概要
====

FailureUrl APIは、|Fess| のクロール失敗URLを管理するためのAPIです。
クロール中にエラーが発生したURLの確認、削除などを操作できます。

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
     - /
     - 失敗URL一覧取得
   * - DELETE
     - /{id}
     - 失敗URL削除
   * - DELETE
     - /delete-all
     - 全失敗URL削除

失敗URL一覧取得
===============

リクエスト
----------

::

    GET /api/admin/failureurl

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
   * - ``errorCountMin``
     - Integer
     - いいえ
     - 最小エラー回数フィルター
   * - ``configId``
     - String
     - いいえ
     - 設定IDフィルター

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "failures": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "configId": "webconfig_id_1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": "2025-01-29T10:00:00Z",
            "threadName": "Crawler-1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "configId": "webconfig_id_1",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": "2025-01-29T09:30:00Z",
            "threadName": "Crawler-2"
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
     - 失敗URL ID
   * - ``url``
     - 失敗したURL
   * - ``configId``
     - クロール設定ID
   * - ``errorName``
     - エラー名
   * - ``errorLog``
     - エラーログ
   * - ``errorCount``
     - エラー発生回数
   * - ``lastAccessTime``
     - 最終アクセス時刻
   * - ``threadName``
     - スレッド名

失敗URL削除
===========

リクエスト
----------

::

    DELETE /api/admin/failureurl/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Failure URL deleted successfully"
      }
    }

全失敗URL削除
=============

リクエスト
----------

::

    DELETE /api/admin/failureurl/delete-all

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``configId``
     - String
     - いいえ
     - 特定設定IDの失敗URLのみ削除
   * - ``errorCountMin``
     - Integer
     - いいえ
     - 指定回数以上のエラーのみ削除

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "All failure URLs deleted successfully",
        "deletedCount": 45
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

失敗URL一覧の取得
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

エラー回数でフィルター
----------------------

.. code-block:: bash

    # 3回以上エラーが発生したURLのみ取得
    curl -X GET "http://localhost:8080/api/admin/failureurl?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

特定設定の失敗URL取得
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

失敗URLの削除
-------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

全失敗URLの削除
---------------

.. code-block:: bash

    # 全ての失敗URLを削除
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 特定設定の失敗URLのみ削除
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 3回以上エラーが発生したURLのみ削除
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

エラータイプ別の集計
--------------------

.. code-block:: bash

    # エラータイプごとにカウント
    curl -X GET "http://localhost:8080/api/admin/failureurl?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.failures[].errorName] | group_by(.) | map({error: .[0], count: length})'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-crawlinginfo` - クロール情報API
- :doc:`api-admin-joblog` - ジョブログAPI
- :doc:`../../admin/failureurl-guide` - 失敗URL管理ガイド
