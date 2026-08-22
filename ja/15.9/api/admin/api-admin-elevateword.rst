==========================
ElevateWord API
==========================

概要
====

ElevateWord APIは、|Fess| のエレベートワード（特定キーワードでの検索順位操作）を管理するためのAPIです。
特定の検索クエリに対して、特定のドキュメントを上位または下位に配置できます。

ベースURL
=========

::

    /api/admin/elevateword

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
     - エレベートワード一覧取得
   * - GET
     - /setting/{id}
     - エレベートワード取得
   * - POST
     - /setting
     - エレベートワード作成
   * - PUT
     - /setting
     - エレベートワード更新
   * - DELETE
     - /setting/{id}
     - エレベートワード削除
   * - PUT
     - /upload
     - エレベートワードCSVアップロード
   * - GET
     - /download
     - エレベートワードCSVダウンロード

エレベートワード一覧取得
========================

リクエスト
----------

::

    GET /api/admin/elevateword/settings

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
     - エレベートワードIDによる完全一致フィルタ

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "フェス",
            "permissions": "{role}guest",
            "boost": 100.0,
            "labelTypeIds": []
          }
        ],
        "total": 5
      }
    }

エレベートワード取得
====================

リクエスト
----------

::

    GET /api/admin/elevateword/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "elevate_id_1",
          "suggestWord": "fess",
          "reading": "フェス",
          "permissions": "{role}guest",
          "boost": 100.0,
          "labelTypeIds": []
        }
      }
    }

エレベートワード作成
====================

リクエスト
----------

::

    POST /api/admin/elevateword/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "documentation",
      "reading": "ドキュメンテーション",
      "permissions": "{role}guest",
      "boost": 100.0,
      "labelTypeIds": ["label1"]
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``suggestWord``
     - はい
     - エレベート対象のキーワード
   * - ``reading``
     - いいえ
     - 読み仮名
   * - ``permissions``
     - いいえ
     - アクセス権限（1行に1件の改行区切り文字列。フォーム初期値: 検索のデフォルト表示権限）
   * - ``boost``
     - はい
     - ブースト値（フォーム初期値: 100.0）
   * - ``labelTypeIds``
     - いいえ
     - 対象ラベルID（文字列の配列）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_elevate_id",
        "created": true
      }
    }

エレベートワード更新
====================

リクエスト
----------

::

    PUT /api/admin/elevateword/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_elevate_id",
      "suggestWord": "documentation",
      "reading": "ドキュメンテーション",
      "permissions": "{role}guest\n{role}user",
      "boost": 100.0,
      "labelTypeIds": ["label1"],
      "versionNo": 1
    }

.. note::

   更新時は、作成時のフィールドに加えて以下のフィールドが必須です。

   - ``id`` - 更新対象のエレベートワードID
   - ``versionNo`` - 楽観的ロック用のバージョン番号。\ ``GET /setting/{id}`` で取得した値を指定します。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_elevate_id",
        "created": false
      }
    }

エレベートワード削除
====================

リクエスト
----------

::

    DELETE /api/admin/elevateword/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_elevate_id",
        "created": false
      }
    }

エレベートワードCSVアップロード
===============================

CSVファイルからエレベートワードを一括登録します。ファイルは ``multipart/form-data`` で送信します。インポートはサーバー側で非同期に実行されます。

リクエスト
----------

::

    PUT /api/admin/elevateword/upload
    Content-Type: multipart/form-data

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``elevateWordFile``
     - はい
     - アップロードするエレベートワードCSVファイル

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

エレベートワードCSVダウンロード
===============================

登録済みのエレベートワードをCSVファイル（``elevate.csv``）としてダウンロードします。レスポンスは ``application/octet-stream`` のストリームです。

リクエスト
----------

::

    GET /api/admin/elevateword/download

使用例
======

製品名のエレベート
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "Product X",
           "boost": 100.0,
           "permissions": "{role}guest"
         }'

特定ラベルへのエレベート
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 100.0,
           "labelTypeIds": ["technical_docs"],
           "permissions": "{role}guest"
         }'

CSVファイルのアップロード
-------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/elevateword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "elevateWordFile=@elevate.csv"

CSVファイルのダウンロード
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/elevateword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o elevate.csv

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-keymatch` - キーマッチAPI
- :doc:`api-admin-boostdoc` - ドキュメントブーストAPI
- :doc:`../../admin/elevateword-guide` - エレベートワード管理ガイド
