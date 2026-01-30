==========================
Admin API 概要
==========================

概要
====

|Fess| Admin APIは、管理機能にプログラムからアクセスするためのRESTful APIです。
クロール設定、ユーザー管理、スケジューラー制御など、管理画面で行える操作のほとんどをAPI経由で実行できます。

このAPIを使用することで、|Fess| の設定を自動化したり、外部システムと連携したりすることが可能です。

ベースURL
=========

Admin APIのベースURLは以下の形式です:

::

    http://<Server Name>/api/admin/

例えば、ローカル環境の場合:

::

    http://localhost:8080/api/admin/

認証
====

Admin APIにアクセスするには、アクセストークンによる認証が必要です。

アクセストークンの取得
----------------------

1. 管理画面にログイン
2. 「システム」→「アクセストークン」に移動
3. 「新規作成」をクリック
4. トークン名を入力し、必要な権限を選択
5. 「作成」をクリックしてトークンを取得

トークンの使用
--------------

リクエストヘッダーにアクセストークンを含めます:

::

    Authorization: Bearer <アクセストークン>

または、クエリパラメーターで指定:

::

    ?token=<アクセストークン>

cURL例
~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

必要な権限
----------

Admin APIを使用するには、トークンに以下の権限が必要です:

- ``admin-*`` - すべての管理機能へのアクセス
- ``admin-scheduler`` - スケジューラー管理のみ
- ``admin-user`` - ユーザー管理のみ
- その他、機能ごとの権限

共通パターン
============

一覧取得（GET/PUT /settings）
-----------------------------

設定の一覧を取得します。

リクエスト
~~~~~~~~~~

::

    GET /api/admin/<resource>/settings
    PUT /api/admin/<resource>/settings

パラメーター（ページネーション）:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - パラメーター
     - 型
     - 説明
   * - ``size``
     - Integer
     - 1ページあたりの件数（デフォルト: 20）
   * - ``page``
     - Integer
     - ページ番号（0から開始）

レスポンス
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

単一設定取得（GET /setting/{id}）
---------------------------------

IDを指定して単一の設定を取得します。

リクエスト
~~~~~~~~~~

::

    GET /api/admin/<resource>/setting/{id}

レスポンス
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

新規作成（POST /setting）
-------------------------

新しい設定を作成します。

リクエスト
~~~~~~~~~~

::

    POST /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

レスポンス
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

更新（PUT /setting）
--------------------

既存の設定を更新します。

リクエスト
~~~~~~~~~~

::

    PUT /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

レスポンス
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "updated_id",
        "created": false
      }
    }

削除（DELETE /setting/{id}）
----------------------------

設定を削除します。

リクエスト
~~~~~~~~~~

::

    DELETE /api/admin/<resource>/setting/{id}

レスポンス
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

レスポンス形式
==============

成功レスポンス
--------------

.. code-block:: json

    {
      "response": {
        "status": 0,
        ...
      }
    }

``status: 0`` は成功を示します。

エラーレスポンス
----------------

.. code-block:: json

    {
      "response": {
        "status": 1,
        "errors": [
          {"code": "errors.failed_to_create", "args": ["...", "..."]}
        ]
      }
    }

HTTPステータスコード
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - コード
     - 説明
   * - 200
     - リクエスト成功
   * - 400
     - リクエストパラメーターが不正
   * - 401
     - 認証が必要（トークンなしまたは無効）
   * - 403
     - アクセス権限がない
   * - 404
     - リソースが見つからない
   * - 500
     - サーバー内部エラー

利用可能なAPI
=============

|Fess| は以下のAdmin APIを提供しています。

クロール設定
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-webconfig`
     - Webクロール設定
   * - :doc:`api-admin-fileconfig`
     - ファイルクロール設定
   * - :doc:`api-admin-dataconfig`
     - データストア設定

インデックス管理
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-documents`
     - ドキュメント一括操作
   * - :doc:`api-admin-crawlinginfo`
     - クロール情報
   * - :doc:`api-admin-failureurl`
     - 失敗URL管理
   * - :doc:`api-admin-backup`
     - バックアップ/リストア

スケジューラー
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-scheduler`
     - ジョブスケジューリング
   * - :doc:`api-admin-joblog`
     - ジョブログ取得

ユーザー・権限管理
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-user`
     - ユーザー管理
   * - :doc:`api-admin-role`
     - ロール管理
   * - :doc:`api-admin-group`
     - グループ管理
   * - :doc:`api-admin-accesstoken`
     - APIトークン管理

検索チューニング
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-labeltype`
     - ラベルタイプ
   * - :doc:`api-admin-keymatch`
     - キーマッチ
   * - :doc:`api-admin-boostdoc`
     - ドキュメントブースト
   * - :doc:`api-admin-elevateword`
     - エレベートワード
   * - :doc:`api-admin-badword`
     - NGワード
   * - :doc:`api-admin-relatedcontent`
     - 関連コンテンツ
   * - :doc:`api-admin-relatedquery`
     - 関連クエリ
   * - :doc:`api-admin-suggest`
     - サジェスト管理

システム
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-general`
     - 一般設定
   * - :doc:`api-admin-systeminfo`
     - システム情報
   * - :doc:`api-admin-stats`
     - システム統計
   * - :doc:`api-admin-log`
     - ログ取得
   * - :doc:`api-admin-storage`
     - ストレージ管理
   * - :doc:`api-admin-plugin`
     - プラグイン管理

辞書
----

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-dict`
     - 辞書管理（シノニム、ストップワード等）

使用例
======

Webクロール設定の作成
---------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "maxAccessCount": 1000,
           "depth": 3,
           "available": true
         }'

スケジュールジョブの開始
------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

ユーザーの一覧取得
------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`../api-overview` - API概要
- :doc:`../../admin/accesstoken-guide` - アクセストークン管理ガイド
