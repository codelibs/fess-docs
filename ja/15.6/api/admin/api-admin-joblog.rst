==========================
JobLog API
==========================

概要
====

JobLog APIは、|Fess| のジョブ実行ログを取得するためのAPIです。
スケジュールジョブやクロールジョブの実行履歴、エラー情報などを確認できます。

ベースURL
=========

::

    /api/admin/joblog

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
     - ジョブログ一覧取得
   * - GET
     - /{id}
     - ジョブログ詳細取得
   * - DELETE
     - /{id}
     - ジョブログ削除
   * - DELETE
     - /delete-all
     - 全ジョブログ削除

ジョブログ一覧取得
==================

リクエスト
----------

::

    GET /api/admin/joblog

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
   * - ``status``
     - String
     - いいえ
     - ステータスフィルター（ok/fail/running）
   * - ``from``
     - String
     - いいえ
     - 開始日時（ISO 8601形式）
   * - ``to``
     - String
     - いいえ
     - 終了日時（ISO 8601形式）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "joblog_id_1",
            "jobName": "Default Crawler",
            "jobStatus": "ok",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Job completed successfully",
            "startTime": "2025-01-29T02:00:00Z",
            "endTime": "2025-01-29T02:45:23Z",
            "executionTime": 2723000
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "2025-01-28T02:00:00Z",
            "endTime": "2025-01-28T02:10:15Z",
            "executionTime": 615000
          }
        ],
        "total": 100
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
     - ジョブログID
   * - ``jobName``
     - ジョブ名
   * - ``jobStatus``
     - ジョブステータス（ok/fail/running）
   * - ``target``
     - 実行対象
   * - ``scriptType``
     - スクリプトタイプ
   * - ``scriptData``
     - 実行スクリプト
   * - ``scriptResult``
     - 実行結果
   * - ``startTime``
     - 開始時刻
   * - ``endTime``
     - 終了時刻
   * - ``executionTime``
     - 実行時間（ミリ秒）

ジョブログ詳細取得
==================

リクエスト
----------

::

    GET /api/admin/joblog/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "joblog_id_1",
          "jobName": "Default Crawler",
          "jobStatus": "ok",
          "target": "all",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "scriptResult": "Crawl completed successfully.\nDocuments indexed: 1234\nDocuments updated: 567\nDocuments deleted: 12\nErrors: 0",
          "startTime": "2025-01-29T02:00:00Z",
          "endTime": "2025-01-29T02:45:23Z",
          "executionTime": 2723000
        }
      }
    }

ジョブログ削除
==============

リクエスト
----------

::

    DELETE /api/admin/joblog/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job log deleted successfully"
      }
    }

全ジョブログ削除
================

リクエスト
----------

::

    DELETE /api/admin/joblog/delete-all

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
   * - ``status``
     - String
     - いいえ
     - 特定ステータスのログのみ削除

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job logs deleted successfully",
        "deletedCount": 50
      }
    }

使用例
======

ジョブログ一覧の取得
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

失敗したジョブのみ取得
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

特定期間のジョブログ
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

ジョブログ詳細の取得
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

古いジョブログの削除
--------------------

.. code-block:: bash

    # 30日より前のログを削除
    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

失敗したジョブログのみ削除
--------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

実行時間が長いジョブの検出
--------------------------

.. code-block:: bash

    # 1時間以上かかったジョブを抽出
    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.executionTime > 3600000) | {jobName, startTime, executionTime}'

ジョブ成功率の計算
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-scheduler` - スケジューラーAPI
- :doc:`api-admin-crawlinginfo` - クロール情報API
- :doc:`../../admin/joblog-guide` - ジョブログ管理ガイド
