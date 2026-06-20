==========================
BadWord API
==========================

概要
====

BadWord APIは、|Fess| のNGワード（不適切なサジェストワードの除外）を管理するためのAPIです。
サジェスト機能で表示したくないキーワードを設定できます。

ベースURL
=========

::

    /api/admin/badword

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
     - NGワード一覧取得
   * - GET
     - /setting/{id}
     - NGワード取得
   * - POST
     - /setting
     - NGワード作成
   * - PUT
     - /setting
     - NGワード更新
   * - DELETE
     - /setting/{id}
     - NGワード削除
   * - PUT
     - /upload
     - NGワードCSVアップロード
   * - GET
     - /download
     - NGワードCSVダウンロード

NGワード一覧取得
================

リクエスト
----------

::

    GET /api/admin/badword/settings

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

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
     - 指定したIDのNGワードのみに絞り込み

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word"
          }
        ],
        "total": 5
      }
    }

NGワード取得
============

リクエスト
----------

::

    GET /api/admin/badword/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "badword_id_1",
          "suggestWord": "inappropriate_word"
        }
      }
    }

NGワード作成
============

リクエスト
----------

::

    POST /api/admin/badword/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "spam_keyword"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - フィールド
     - 必須
     - 説明
   * - ``suggestWord``
     - はい
     - 除外するキーワード（空白文字を含めることはできません）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_badword_id",
        "created": true
      }
    }

NGワード更新
============

リクエスト
----------

::

    PUT /api/admin/badword/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_badword_id",
      "suggestWord": "updated_spam_keyword",
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_badword_id",
        "created": false
      }
    }

NGワード削除
============

リクエスト
----------

::

    DELETE /api/admin/badword/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_badword_id",
        "created": false
      }
    }

NGワードCSVアップロード
=======================

CSVファイルからNGワードを一括登録します。ファイルは ``multipart/form-data`` で送信します。インポートはサーバー側で非同期に実行されます。

リクエスト
----------

::

    PUT /api/admin/badword/upload
    Content-Type: multipart/form-data

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``badWordFile``
     - はい
     - アップロードするNGワードCSVファイル

CSVフォーマット
~~~~~~~~~~~~~~~

- 1行目はヘッダー行として読み飛ばされます（列名は任意。ダウンロード時は ``BadWord`` が出力されます）。
- 2行目以降は、1行に1つのNGワードを ``suggestWord`` として記述します。
- 値が空白のみの行は無視されます。
- 単語の先頭に ``--`` を付けると、その単語を削除します（例: ``--spam`` は ``spam`` を削除）。
- 既に登録済みの単語を指定した場合は更新（更新者・更新日時の再設定）として扱われます。

.. note::

   アップロード処理はサーバー側で非同期に実行されるため、レスポンスの ``status: 0`` は
   リクエストの受理を示すものであり、インポート完了を保証するものではありません。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

NGワードCSVダウンロード
=======================

登録済みのNGワードをCSVファイル（``badword.csv``）としてダウンロードします。レスポンスは ``application/octet-stream`` のストリームです。
CSVは1行目に ``BadWord`` というヘッダー行を持ち、2行目以降に登録済みのNGワードが1行に1つずつ出力されます。

リクエスト
----------

::

    GET /api/admin/badword/download

使用例
======

スパムキーワードの除外
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam"
         }'

CSVファイルのアップロード
-------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/badword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "badWordFile=@badword.csv"

CSVファイルのダウンロード
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/badword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o badword.csv

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-suggest` - サジェスト管理API
- :doc:`api-admin-elevateword` - エレベートワードAPI
- :doc:`../../admin/badword-guide` - NGワード管理ガイド
