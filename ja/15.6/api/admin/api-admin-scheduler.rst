==========================
Scheduler API
==========================

概要
====

Scheduler APIは、|Fess| のスケジュールジョブを管理するためのAPIです。
クロールジョブの起動・停止、スケジュール設定の作成・更新・削除などを行えます。

ベースURL
=========

::

    /api/admin/scheduler

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET/PUT
     - /settings
     - スケジュールジョブ一覧取得
   * - GET
     - /setting/{id}
     - スケジュールジョブ取得
   * - POST
     - /setting
     - スケジュールジョブ作成
   * - PUT
     - /setting
     - スケジュールジョブ更新
   * - DELETE
     - /setting/{id}
     - スケジュールジョブ削除
   * - PUT
     - /{id}/start
     - ジョブ開始
   * - PUT
     - /{id}/stop
     - ジョブ停止

スケジュールジョブ一覧取得
==========================

リクエスト
----------

::

    GET /api/admin/scheduler/settings
    PUT /api/admin/scheduler/settings

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
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": true,
            "crawler": true,
            "available": true,
            "sortOrder": 0,
            "running": false
          }
        ],
        "total": 5
      }
    }

スケジュールジョブ取得
======================

リクエスト
----------

::

    GET /api/admin/scheduler/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "job_id_1",
          "name": "Default Crawler",
          "target": "all",
          "cronExpression": "0 0 0 * * ?",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "jobLogging": true,
          "crawler": true,
          "available": true,
          "sortOrder": 0,
          "running": false
        }
      }
    }

スケジュールジョブ作成
======================

リクエスト
----------

::

    POST /api/admin/scheduler/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Daily Crawler",
      "target": "all",
      "cronExpression": "0 0 2 * * ?",
      "scriptType": "groovy",
      "scriptData": "return container.getComponent(\"crawlJob\").execute();",
      "jobLogging": true,
      "crawler": true,
      "available": true,
      "sortOrder": 1
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - ジョブ名
   * - ``target``
     - はい
     - 実行対象（"all" または特定のターゲット）
   * - ``cronExpression``
     - はい
     - Cron式（秒 分 時 日 月 曜日）
   * - ``scriptType``
     - はい
     - スクリプトタイプ（"groovy"）
   * - ``scriptData``
     - はい
     - 実行スクリプト
   * - ``jobLogging``
     - いいえ
     - ログ記録を有効化（デフォルト: true）
   * - ``crawler``
     - いいえ
     - クローラージョブかどうか（デフォルト: false）
   * - ``available``
     - いいえ
     - 有効/無効（デフォルト: true）
   * - ``sortOrder``
     - いいえ
     - 表示順序

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_job_id",
        "created": true
      }
    }

Cron式の例
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Cron式
     - 説明
   * - ``0 0 2 * * ?``
     - 毎日午前2時に実行
   * - ``0 0 0/6 * * ?``
     - 6時間ごとに実行
   * - ``0 0 2 * * MON``
     - 毎週月曜日の午前2時に実行
   * - ``0 0 2 1 * ?``
     - 毎月1日の午前2時に実行

スケジュールジョブ更新
======================

リクエスト
----------

::

    PUT /api/admin/scheduler/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_job_id",
      "name": "Updated Crawler",
      "target": "all",
      "cronExpression": "0 0 3 * * ?",
      "scriptType": "groovy",
      "scriptData": "...",
      "jobLogging": true,
      "crawler": true,
      "available": true,
      "sortOrder": 1,
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_job_id",
        "created": false
      }
    }

スケジュールジョブ削除
======================

リクエスト
----------

::

    DELETE /api/admin/scheduler/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_job_id",
        "created": false
      }
    }

ジョブ開始
==========

スケジュールジョブを即座に実行します。

リクエスト
----------

::

    PUT /api/admin/scheduler/{id}/start

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

注意事項
--------

- ジョブが既に実行中の場合、エラーが返されます
- ジョブが無効（``available: false``）の場合、エラーが返されます

ジョブ停止
==========

実行中のジョブを停止します。

リクエスト
----------

::

    PUT /api/admin/scheduler/{id}/stop

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

クロールジョブの作成と実行
--------------------------

.. code-block:: bash

    # ジョブを作成
    curl -X POST "http://localhost:8080/api/admin/scheduler/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Hourly Crawler",
           "target": "all",
           "cronExpression": "0 0 * * * ?",
           "scriptType": "groovy",
           "scriptData": "return container.getComponent(\"crawlJob\").execute();",
           "jobLogging": true,
           "crawler": true,
           "available": true
         }'

    # ジョブを即座に実行
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

ジョブの状態確認
----------------

.. code-block:: bash

    # 全ジョブの状態を確認
    curl "http://localhost:8080/api/admin/scheduler/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # runningフィールドで実行状態を確認できます

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-joblog` - ジョブログAPI
- :doc:`../../admin/scheduler-guide` - スケジューラー管理ガイド
