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
     - /logs
     - ジョブログ一覧取得
   * - GET
     - /log/{id}
     - ジョブログ取得
   * - DELETE
     - /log/{id}
     - ジョブログ削除

ジョブログ一覧取得
==================

リクエスト
----------

::

    GET /api/admin/joblog/logs

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
            "startTime": 1738116000000,
            "endTime": 1738118723000
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": 1738029600000,
            "endTime": 1738030215000
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
     - ジョブステータス
   * - ``target``
     - 実行対象
   * - ``scriptType``
     - スクリプトタイプ
   * - ``scriptData``
     - 実行スクリプト
   * - ``scriptResult``
     - 実行結果
   * - ``startTime``
     - 開始時刻（エポックミリ秒）
   * - ``endTime``
     - 終了時刻（エポックミリ秒）

ジョブログ取得
==============

リクエスト
----------

::

    GET /api/admin/joblog/log/{id}

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
          "startTime": 1738116000000,
          "endTime": 1738118723000
        }
      }
    }

ジョブログ削除
==============

リクエスト
----------

::

    DELETE /api/admin/joblog/log/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

使用例
======

ジョブログ一覧の取得
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

失敗したジョブのみ抽出
----------------------

.. code-block:: bash

    # jqで失敗したジョブをフィルター
    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.jobStatus=="fail")'

ジョブログの取得
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

ジョブログの削除
----------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

ジョブ成功率の計算
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-scheduler` - スケジューラーAPI
- :doc:`api-admin-crawlinginfo` - クロール情報API
- :doc:`../../admin/joblog-guide` - ジョブログ管理ガイド
