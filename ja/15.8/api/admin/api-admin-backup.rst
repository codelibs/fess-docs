==========================
Backup API
==========================

概要
====

Backup APIは、|Fess| のバックアップ対象データを参照・ダウンロードするためのAPIです。
バックアップ対象の一覧取得と、個別のバックアップファイル（システムプロパティ、各インデックスのバルクデータ、ログのNDJSONデータ）のダウンロードを行えます。

このAPIは参照・ダウンロード（読み取り）専用です。バックアップファイルをアップロードして復元するリストア機能はAPIでは提供されていないため、リストアが必要な場合は管理画面の「システム情報」→「バックアップ」から行ってください。

ベースURL
=========

::

    /api/admin/backup

認証
====

他のAdmin APIと同様に、アクセストークンによる認証が必要です。アクセストークンには ``Radmin-api`` 権限（``api.admin.access.permissions`` で設定。既定値は ``Radmin-api``）が必要です。
リクエストヘッダーにアクセストークンを指定します。

::

    Authorization: Bearer <アクセストークン>

認証やアクセストークンの取得方法の詳細は :doc:`api-admin-overview` を参照してください。

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /files
     - バックアップ対象一覧取得
   * - GET
     - /file/{id}
     - バックアップファイルのダウンロード

バックアップ対象一覧取得
========================

バックアップ対象の一覧を返します。対象は ``index.backup.targets`` および ``index.backup.log.targets`` の設定に基づき、両者を結合した一覧が返されます。

リクエスト
----------

::

    GET /api/admin/backup/files

レスポンス
----------

``files`` にバックアップ対象を表すオブジェクトの配列、``total`` に件数が格納されます。
各オブジェクトは ``id`` と ``name`` を持ち、いずれも対象名（``fess_config.bulk``、``system.properties``、``search_log.ndjson`` など）が設定されます。

以下は既定設定（``index.backup.targets`` と ``index.backup.log.targets`` がデフォルト値）の場合の例です。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "files": [
          { "id": "fess_basic_config.bulk", "name": "fess_basic_config.bulk" },
          { "id": "fess_config.bulk", "name": "fess_config.bulk" },
          { "id": "fess_user.bulk", "name": "fess_user.bulk" },
          { "id": "system.properties", "name": "system.properties" },
          { "id": "fess.json", "name": "fess.json" },
          { "id": "doc.json", "name": "doc.json" },
          { "id": "click_log.ndjson", "name": "click_log.ndjson" },
          { "id": "favorite_log.ndjson", "name": "favorite_log.ndjson" },
          { "id": "search_log.ndjson", "name": "search_log.ndjson" },
          { "id": "user_info.ndjson", "name": "user_info.ndjson" }
        ],
        "total": 10
      }
    }

.. note::

   ``version`` には実行中の |Fess| の製品バージョンが設定されます。``files`` の内容は
   ``index.backup.targets`` / ``index.backup.log.targets`` の設定によって変わるため、
   上記は既定値での一例です。

バックアップファイルのダウンロード
==================================

指定したバックアップファイルの内容をダウンロードします。``{id}`` には一覧取得で得られた ``id`` （対象名）を指定します。
``{id}`` の種別によって、レスポンス内容が以下のように切り替わります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - 内容
   * - ``system.properties``
     - システムプロパティの内容（``application/octet-stream``）
   * - ``*.bulk`` または拡張子なしのインデックス名
     - 対象名と同名のインデックスをスクロールして生成したバルクデータ（``application/octet-stream``）。``.bulk`` を取り除いた名前をインデックス名として扱います。
   * - ``*.ndjson`` （``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``）
     - 対応するログのNDJSONデータ（``application/x-ndjson``）

.. note::

   ``fess.json`` と ``doc.json`` はインデックスのマッピング定義（スキーマ）ファイルです。
   対象一覧（``/files``）には含まれますが、このAPIのダウンロードでは ``.bulk`` と同様に
   インデックスのスクロール処理として扱われます。マッピング定義を含むバックアップ／
   リストアは管理画面の「システム情報」→「バックアップ」を利用してください。

バックアップ対象に存在しない ``{id}`` を指定した場合は、``status`` に 0 以外の値とエラーメッセージ（``Could not find any backup index.``）を含むエラーレスポンスが返されます。

リクエスト
----------

::

    GET /api/admin/backup/file/{id}

レスポンス
----------

バックアップファイルのストリーム。NDJSON形式の場合は ``Content-Type: application/x-ndjson``、それ以外は ``application/octet-stream`` で返されます。

.. note::

   ログ（``*.ndjson``）のエクスポートは ``index.backup.log.load.timeout`` （既定値 60000 ミリ秒）
   の制約を受けます。出力に時間がかかる場合、ログデータが途中で打ち切られることがあります。

使用例
======

バックアップ対象一覧の取得
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

設定インデックスのダウンロード
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/fess_config.bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess_config.bulk

検索ログのダウンロード
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/search_log.ndjson" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o search_log.ndjson

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-log` - ログAPI
