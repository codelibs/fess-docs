==========================
SearchLog API
==========================

概要
====

SearchLog APIは、|Fess| の検索ログを取得・管理するためのAPIです。
ユーザーの検索行動分析、検索品質の改善に活用できます。

ベースURL
=========

::

    /api/admin/searchlog

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
     - 検索ログ一覧取得
   * - GET
     - /{id}
     - 検索ログ詳細取得
   * - DELETE
     - /{id}
     - 検索ログ削除
   * - DELETE
     - /delete-all
     - 検索ログ一括削除
   * - GET
     - /stats
     - 検索統計取得

検索ログ一覧取得
================

リクエスト
----------

::

    GET /api/admin/searchlog

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
     - 検索クエリでフィルター
   * - ``user``
     - String
     - いいえ
     - ユーザーIDでフィルター

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "searchlog_id_1",
            "searchWord": "Fess インストール",
            "requestedAt": "2025-01-29T10:00:00Z",
            "responseTime": 125,
            "hitCount": 234,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user001",
            "userSessionId": "session_abc123",
            "clientIp": "192.168.1.100",
            "referer": "https://example.com/",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user", "admin"],
            "languages": ["ja"]
          },
          {
            "id": "searchlog_id_2",
            "searchWord": "検索 設定",
            "requestedAt": "2025-01-29T09:55:00Z",
            "responseTime": 98,
            "hitCount": 567,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user002",
            "userSessionId": "session_def456",
            "clientIp": "192.168.1.101",
            "referer": "",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user"],
            "languages": ["ja", "en"]
          }
        ],
        "total": 10000
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
     - 検索ログID
   * - ``searchWord``
     - 検索キーワード
   * - ``requestedAt``
     - 検索日時
   * - ``responseTime``
     - レスポンス時間（ミリ秒）
   * - ``hitCount``
     - ヒット件数
   * - ``queryOffset``
     - 結果のオフセット
   * - ``queryPageSize``
     - ページサイズ
   * - ``user``
     - ユーザーID
   * - ``userSessionId``
     - セッションID
   * - ``clientIp``
     - クライアントIPアドレス
   * - ``referer``
     - リファラー
   * - ``userAgent``
     - ユーザーエージェント
   * - ``roles``
     - ユーザーロール
   * - ``languages``
     - 検索言語

検索ログ詳細取得
================

リクエスト
----------

::

    GET /api/admin/searchlog/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "searchlog_id_1",
          "searchWord": "Fess インストール",
          "requestedAt": "2025-01-29T10:00:00Z",
          "responseTime": 125,
          "hitCount": 234,
          "queryOffset": 0,
          "queryPageSize": 10,
          "user": "user001",
          "userSessionId": "session_abc123",
          "clientIp": "192.168.1.100",
          "referer": "https://example.com/",
          "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
          "roles": ["user", "admin"],
          "languages": ["ja"],
          "clickLogs": [
            {
              "url": "https://fess.codelibs.org/install.html",
              "docId": "doc_123",
              "order": 1,
              "clickedAt": "2025-01-29T10:00:15Z"
            }
          ]
        }
      }
    }

検索ログ削除
============

リクエスト
----------

::

    DELETE /api/admin/searchlog/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search log deleted successfully"
      }
    }

検索ログ一括削除
================

リクエスト
----------

::

    DELETE /api/admin/searchlog/delete-all

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
     - いいえ
     - この日時より前のログを削除（ISO 8601形式）
   * - ``user``
     - String
     - いいえ
     - 特定ユーザーのログのみ削除

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search logs deleted successfully",
        "deletedCount": 5000
      }
    }

検索統計取得
============

リクエスト
----------

::

    GET /api/admin/searchlog/stats

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``from``
     - String
     - いいえ
     - 開始日時（ISO 8601形式）
   * - ``to``
     - String
     - いいえ
     - 終了日時（ISO 8601形式）
   * - ``interval``
     - String
     - いいえ
     - 集計間隔（hour/day/week/month）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalSearches": 50000,
          "uniqueUsers": 1234,
          "averageResponseTime": 156,
          "averageHitCount": 345,
          "zeroHitRate": 0.05,
          "topSearchWords": [
            {"word": "Fess", "count": 1500},
            {"word": "インストール", "count": 800},
            {"word": "設定", "count": 650}
          ],
          "searchesByDate": [
            {"date": "2025-01-29", "count": 2500},
            {"date": "2025-01-28", "count": 2300},
            {"date": "2025-01-27", "count": 2100}
          ]
        }
      }
    }

使用例
======

検索ログ一覧の取得
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

期間を指定して取得
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?from=2025-01-01T00:00:00Z&to=2025-01-31T23:59:59Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

特定ユーザーの検索ログ
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?user=user001" \
         -H "Authorization: Bearer YOUR_TOKEN"

特定キーワードの検索ログ
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?query=Fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

検索統計の取得
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31&interval=day" \
         -H "Authorization: Bearer YOUR_TOKEN"

古い検索ログの削除
------------------

.. code-block:: bash

    # 30日より前のログを削除
    curl -X DELETE "http://localhost:8080/api/admin/searchlog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

人気検索キーワードの抽出
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.topSearchWords'

検索品質の分析
--------------

.. code-block:: bash

    # ゼロヒット率の確認
    curl -X GET "http://localhost:8080/api/admin/searchlog/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '{zeroHitRate: .response.stats.zeroHitRate, averageHitCount: .response.stats.averageHitCount}'

日別検索数の推移
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?interval=day&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.searchesByDate'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-stats` - システム統計API
- :doc:`../../admin/searchlog-guide` - 検索ログ管理ガイド
- :doc:`../../config/search-analytics` - 検索分析設定ガイド
