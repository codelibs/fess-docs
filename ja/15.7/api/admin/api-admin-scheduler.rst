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
   * - GET
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
     - 1ページあたりの件数（デフォルト: 25。``fess_config.properties`` の ``paging.page.size`` で変更可能）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始。デフォルト: 1）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": "true",
            "crawler": "true",
            "available": "true",
            "sortOrder": 0,
            "versionNo": 1,
            "running": false
          }
        ],
        "total": 5
      }
    }

.. note::

   レスポンスの ``response`` オブジェクトには、製品バージョンを示す ``version`` と処理結果を示す ``status`` が常に含まれます（共通仕様は :doc:`api-admin-overview` を参照）。以降の例では簡潔さのために ``version`` を省略する場合があります。

.. note::

   レスポンス内の ``jobLogging`` / ``crawler`` / ``available`` は文字列（``"true"`` / ``"false"``）として返されます。``running`` はブール値で、ジョブが現在実行中かどうかを示すレスポンス専用フィールドです（リクエストでは指定できません）。``total`` は条件に一致する全ジョブ数です。

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
          "jobLogging": "true",
          "crawler": "true",
          "available": "true",
          "sortOrder": 0,
          "versionNo": 1,
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
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
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
     - ジョブ名（最大100文字）
   * - ``target``
     - はい
     - 実行対象（最大100文字）。``all`` または特定のターゲット名を指定します
   * - ``cronExpression``
     - いいえ
     - Cron式（秒 分 時 日 月 曜日）。最大100文字で、Cron式として検証されます。空の場合はスケジュール実行されず、手動でのみ起動できます
   * - ``scriptType``
     - はい
     - スクリプトタイプ（最大100文字）。現在は ``groovy`` のみがサポートされています
   * - ``scriptData``
     - いいえ
     - 実行スクリプト。最大サイズは ``fess_config.properties`` の ``form.admin.max.input.size`` に従います
   * - ``jobLogging``
     - いいえ
     - ジョブログの記録を有効化（文字列）
   * - ``crawler``
     - いいえ
     - クローラージョブかどうか（文字列）
   * - ``available``
     - いいえ
     - 有効/無効（文字列）
   * - ``sortOrder``
     - はい
     - 表示順序（0〜2147483647の整数）

.. note::

   ``jobLogging`` / ``crawler`` / ``available`` は文字列フィールドです。リクエストでは ``"on"`` または ``"true"``（大文字小文字を区別しない）を指定すると有効になり、それ以外の値（``"false"``、空文字列、未指定など）は無効として扱われます。レスポンスでは ``"true"`` / ``"false"`` として返されます。

.. note::

   ``crudMode`` はサーバー側で自動的に設定されるため、リクエストで指定する必要はありません。``createdBy`` / ``createdTime`` などの監査フィールドもサーバー側で設定されます。

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
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
      "sortOrder": 1,
      "versionNo": 1
    }

.. note::

   更新では ``id``（最大1000文字）と ``versionNo`` が必須です。``versionNo`` は楽観的ロックに使用され、取得時のレスポンスに含まれる値を指定します。値が一致しない場合は更新が失敗します。そのほかの必須フィールド（``name`` / ``target`` / ``scriptType`` / ``sortOrder``）は作成時と同様です。

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
        "status": 0,
        "jobLogId": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``jobLogId``
     - 起動したジョブのジョブログID。ジョブログが有効な場合に発行されます。ジョブログが無効な場合は ``null`` になります。

注意事項
--------

- ジョブが既に実行中の場合、起動に失敗しエラー（``status`` が ``0`` 以外）が返されます
- ジョブが無効（``available`` が有効でない）の場合も、同様に起動に失敗しエラーが返されます
- ``jobLogId`` は、ジョブログが有効（``jobLogging`` が有効）な場合にのみ発行されます

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
           "jobLogging": "true",
           "crawler": "true",
           "available": "true",
           "sortOrder": 1
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
