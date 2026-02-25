==========================
Stats API
==========================

概要
====

Stats APIは、|Fess| の統計情報を取得するためのAPIです。
検索クエリ、クリック、お気に入りなどの統計データを確認できます。

ベースURL
=========

::

    /api/admin/stats

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
     - 統計情報取得

統計情報取得
============

リクエスト
----------

::

    GET /api/admin/stats

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
   * - ``type``
     - String
     - いいえ
     - 統計タイプ（query/click/favorite）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalQueries": 12345,
          "uniqueQueries": 5678,
          "totalClicks": 9876,
          "totalFavorites": 543,
          "averageResponseTime": 123.45,
          "topQueries": [
            {
              "query": "fess",
              "count": 567
            },
            {
              "query": "search",
              "count": 432
            }
          ],
          "topClickedDocuments": [
            {
              "url": "https://example.com/doc1",
              "title": "Document 1",
              "count": 234
            }
          ],
          "queryTrends": [
            {
              "date": "2025-01-01",
              "count": 234
            },
            {
              "date": "2025-01-02",
              "count": 267
            }
          ]
        }
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``totalQueries``
     - 総検索クエリ数
   * - ``uniqueQueries``
     - ユニーク検索クエリ数
   * - ``totalClicks``
     - 総クリック数
   * - ``totalFavorites``
     - 総お気に入り数
   * - ``averageResponseTime``
     - 平均レスポンス時間（ミリ秒）
   * - ``topQueries``
     - 人気検索クエリ
   * - ``topClickedDocuments``
     - 人気ドキュメント
   * - ``queryTrends``
     - クエリトレンド

検索クエリ統計
==============

リクエスト
----------

::

    GET /api/admin/stats?type=query&from=2025-01-01&to=2025-01-31

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalQueries": 5678,
          "uniqueQueries": 2345,
          "topQueries": [
            {
              "query": "documentation",
              "count": 234,
              "avgResponseTime": 98.7
            }
          ],
          "queriesByHour": [
            {
              "hour": 0,
              "count": 45
            },
            {
              "hour": 1,
              "count": 23
            }
          ],
          "queriesByDay": [
            {
              "day": "Monday",
              "count": 567
            }
          ]
        }
      }
    }

クリック統計
============

リクエスト
----------

::

    GET /api/admin/stats?type=click&from=2025-01-01&to=2025-01-31

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalClicks": 3456,
          "topClickedDocuments": [
            {
              "url": "https://example.com/popular-doc",
              "title": "Popular Document",
              "count": 234,
              "clickThroughRate": 0.45
            }
          ],
          "clicksByPosition": [
            {
              "position": 1,
              "count": 1234
            },
            {
              "position": 2,
              "count": 567
            }
          ]
        }
      }
    }

使用例
======

全統計情報の取得
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

期間指定での統計取得
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

検索クエリ統計の取得
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

人気クエリTOP10の取得
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.stats.topQueries[:10]'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-log` - ログAPI
- :doc:`api-admin-systeminfo` - システム情報API
- :doc:`../../admin/searchlog-guide` - 検索ログ