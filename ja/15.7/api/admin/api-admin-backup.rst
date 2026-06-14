==========================
Backup API
==========================

概要
====

Backup APIは、|Fess| のバックアップ対象データを参照・ダウンロードするためのAPIです。
バックアップ対象の一覧取得と、個別のバックアップファイル（システムプロパティ、各インデックスのバルクデータ、ログのNDJSONデータ）のダウンロードを行えます。

ベースURL
=========

::

    /api/admin/backup

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

バックアップ対象の一覧を返します。対象は ``index.backup.targets`` および ``index.backup.log.targets`` の設定に基づきます。

リクエスト
----------

::

    GET /api/admin/backup/files

レスポンス
----------

``files`` にバックアップ対象を表すオブジェクトの配列、``total`` に件数が格納されます。
各オブジェクトは ``id`` と ``name`` を持ち、いずれも対象名（``fess_config.bulk``、``system.properties``、``search_log.ndjson`` など）が設定されます。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "fess_config.bulk",
            "name": "fess_config.bulk"
          },
          {
            "id": "system.properties",
            "name": "system.properties"
          },
          {
            "id": "search_log.ndjson",
            "name": "search_log.ndjson"
          }
        ],
        "total": 3
      }
    }

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
     - システムプロパティの内容
   * - ``*.bulk`` または ``.bulk`` 拡張子なしのインデックス名
     - 対象インデックスをスクロールして生成したバルクデータ
   * - ``*.ndjson`` （``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``）
     - 対応するログのNDJSONデータ

バックアップ対象に存在しない ``{id}`` を指定した場合はエラーになります。

リクエスト
----------

::

    GET /api/admin/backup/file/{id}

レスポンス
----------

バックアップファイルのストリーム。NDJSON形式の場合は ``Content-Type: application/x-ndjson``、それ以外は ``application/octet-stream`` で返されます。

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
