==========================
Log API
==========================

概要
====

Log APIは、|Fess| のログ情報を取得するためのAPIです。
検索ログ、クローラーログ、システムログなどを参照できます。

ベースURL
=========

::

    /api/admin/log

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /search
     - 検索ログ取得
   * - GET
     - /click
     - クリックログ取得
   * - GET
     - /favorite
     - お気に入りログ取得
   * - DELETE
     - /search/delete
     - 検索ログ削除

検索ログ取得
============

リクエスト
----------

::

    GET /api/admin/log/search

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
   * - ``from``
     - String
     - いいえ
     - 開始日時（ISO 8601形式）
   * - ``to``
     - String
     - いいえ
     - 終了日時（ISO 8601形式）
   * - ``query``
     - String
     - いいえ
     - 検索クエリフィルター

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "log_id_1",
            "queryId": "query_id_1",
            "query": "fess search",
            "requestedAt": "2025-01-29T10:30:00Z",
            "responseTime": 123,
            "hitCount": 567,
            "user": "guest",
            "roles": ["guest"],
            "languages": ["ja"],
            "clientIp": "192.168.1.100",
            "userAgent": "Mozilla/5.0..."
          }
        ],
        "total": 1234
      }
    }

クリックログ取得
================

リクエスト
----------

::

    GET /api/admin/log/click

パラメーター
~~~~~~~~~~~~

検索ログと同様のパラメーターに加えて以下を指定可能:

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``url``
     - String
     - いいえ
     - クリックされたURLフィルター
   * - ``queryId``
     - String
     - いいえ
     - 検索クエリIDフィルター

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "click_log_id_1",
            "queryId": "query_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "order": 1,
            "clickedAt": "2025-01-29T10:31:00Z",
            "user": "guest",
            "clientIp": "192.168.1.100"
          }
        ],
        "total": 567
      }
    }

お気に入りログ取得
==================

リクエスト
----------

::

    GET /api/admin/log/favorite

パラメーター
~~~~~~~~~~~~

クリックログと同様のパラメーター

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "favorite_log_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "createdAt": "2025-01-29T10:32:00Z",
            "user": "user123"
          }
        ],
        "total": 123
      }
    }

検索ログ削除
============

リクエスト
----------

::

    DELETE /api/admin/log/search/delete

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``before``
     - String
     - はい
     - この日時より前のログを削除（ISO 8601形式）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deletedCount": 5678
      }
    }

使用例
======

最近の検索ログ取得
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

特定期間の検索ログ
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

特定クエリの検索ログ
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?query=fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

クリックログ取得
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/click?size=100" \
         -H "Authorization: Bearer YOUR_TOKEN"

古い検索ログの削除
------------------

.. code-block:: bash

    # 30日より前のログを削除
    curl -X DELETE "http://localhost:8080/api/admin/log/search/delete?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-stats` - 統計API
- :doc:`../../admin/log-guide` - ログ管理ガイド
