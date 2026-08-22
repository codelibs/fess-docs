==========================
JobLog API
==========================

概要
====

JobLog APIは、|Fess| のジョブ実行ログを参照・管理するためのAPIです。
スケジュールジョブやクロールジョブの実行履歴、実行結果、エラー情報などを取得・削除できます。

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
     - 1ページあたりの件数（デフォルト: 20）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始、デフォルト: 1）
   * - ``id``
     - String
     - いいえ
     - ジョブログIDによる絞り込み（完全一致）

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
            "startTime": "1738116000000",
            "endTime": "1738118723000"
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "1738029600000",
            "endTime": "1738030215000"
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
     - ジョブステータス（``ok``: 成功、``fail``: 失敗、``running``: 実行中）
   * - ``target``
     - 実行対象（スケジューラーのターゲット名。既定値は ``all``）
   * - ``scriptType``
     - スクリプトタイプ（例: ``groovy``）
   * - ``scriptData``
     - 実行スクリプト
   * - ``scriptResult``
     - 実行結果
   * - ``startTime``
     - 開始時刻（エポックミリ秒。文字列として返されます）
   * - ``endTime``
     - 終了時刻（エポックミリ秒。文字列として返されます）。実行中のジョブでは返されません。

.. note::

   レスポンスの各ログオブジェクトには、内部的に使用される ``crudMode`` フィールド
   （CRUD操作モードを示す整数値で、参照時は常に ``0``）が含まれます。
   クライアント側では無視して問題ありません。

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
          "startTime": "1738116000000",
          "endTime": "1738118723000"
        }
      }
    }

指定したIDのジョブログが存在しない場合は、``status`` に 0 以外の値が設定された
エラーレスポンスが返されます。

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

指定したIDのジョブログが存在しない場合は、``status`` に 0 以外の値が設定された
エラーレスポンスが返されます。

使用例
======

ジョブログ一覧の取得
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=50&page=1" \
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
