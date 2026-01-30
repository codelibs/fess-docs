==========================
CrawlingInfo API
==========================

概要
====

CrawlingInfo APIは、|Fess| のクロール情報を取得するためのAPIです。
クロールセッションの状態、進捗状況、統計情報などを参照できます。

ベースURL
=========

::

    /api/admin/crawlinginfo

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
     - クロール情報一覧取得
   * - GET
     - /{sessionId}
     - クロールセッション詳細取得
   * - DELETE
     - /{sessionId}
     - クロールセッション削除

クロール情報一覧取得
====================

リクエスト
----------

::

    GET /api/admin/crawlinginfo

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
        "sessions": [
          {
            "sessionId": "session_20250129_100000",
            "name": "Default Crawler",
            "status": "running",
            "startTime": "2025-01-29T10:00:00Z",
            "endTime": null,
            "crawlingInfoCount": 567,
            "createdDocCount": 234,
            "updatedDocCount": 123,
            "deletedDocCount": 12
          },
          {
            "sessionId": "session_20250128_100000",
            "name": "Default Crawler",
            "status": "completed",
            "startTime": "2025-01-28T10:00:00Z",
            "endTime": "2025-01-28T10:45:23Z",
            "crawlingInfoCount": 1234,
            "createdDocCount": 456,
            "updatedDocCount": 678,
            "deletedDocCount": 23
          }
        ],
        "total": 10
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``sessionId``
     - セッションID
   * - ``name``
     - クローラー名
   * - ``status``
     - ステータス（running/completed/failed）
   * - ``startTime``
     - 開始時刻
   * - ``endTime``
     - 終了時刻
   * - ``crawlingInfoCount``
     - クロール情報数
   * - ``createdDocCount``
     - 作成ドキュメント数
   * - ``updatedDocCount``
     - 更新ドキュメント数
   * - ``deletedDocCount``
     - 削除ドキュメント数

クロールセッション詳細取得
==========================

リクエスト
----------

::

    GET /api/admin/crawlinginfo/{sessionId}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session": {
          "sessionId": "session_20250129_100000",
          "name": "Default Crawler",
          "status": "running",
          "startTime": "2025-01-29T10:00:00Z",
          "endTime": null,
          "crawlingInfoCount": 567,
          "createdDocCount": 234,
          "updatedDocCount": 123,
          "deletedDocCount": 12,
          "infos": [
            {
              "url": "https://example.com/page1",
              "status": "OK",
              "method": "GET",
              "httpStatusCode": 200,
              "contentLength": 12345,
              "executionTime": 123,
              "lastModified": "2025-01-29T09:55:00Z"
            }
          ]
        }
      }
    }

クロールセッション削除
======================

リクエスト
----------

::

    DELETE /api/admin/crawlinginfo/{sessionId}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Crawling session deleted successfully"
      }
    }

使用例
======

クロール情報一覧の取得
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

実行中のクロールセッション取得
------------------------------

.. code-block:: bash

    # 全セッションを取得してrunningをフィルター
    curl -X GET "http://localhost:8080/api/admin/crawlinginfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.sessions[] | select(.status=="running")'

特定セッションの詳細取得
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/session_20250129_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

古いセッションの削除
--------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/session_20250101_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

進捗状況の監視
--------------

.. code-block:: bash

    # 実行中のセッションの進捗を定期的に確認
    while true; do
      curl -s "http://localhost:8080/api/admin/crawlinginfo" \
           -H "Authorization: Bearer YOUR_TOKEN" | \
           jq '.response.sessions[] | select(.status=="running") | {sessionId, crawlingInfoCount, createdDocCount}'
      sleep 10
    done

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-failureurl` - 失敗URL API
- :doc:`api-admin-joblog` - ジョブログAPI
- :doc:`../../admin/crawlinginfo-guide` - クロール情報ガイド
