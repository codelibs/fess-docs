==========================
KeyMatch API
==========================

概要
====

KeyMatch APIは、|Fess| のキーマッチ（検索キーワードと結果の紐付け）を管理するためのAPIです。
特定のキーワードに対して特定のドキュメントを上位表示させることができます。

ベースURL
=========

::

    /api/admin/keymatch

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
     - キーマッチ一覧取得
   * - GET
     - /setting/{id}
     - キーマッチ取得
   * - POST
     - /setting
     - キーマッチ作成
   * - PUT
     - /setting
     - キーマッチ更新
   * - DELETE
     - /setting/{id}
     - キーマッチ削除

キーマッチ一覧取得
==================

リクエスト
----------

::

    GET /api/admin/keymatch/settings
    PUT /api/admin/keymatch/settings

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
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "maxSize": 10,
            "boost": 10.0
          }
        ],
        "total": 5
      }
    }

キーマッチ取得
==============

リクエスト
----------

::

    GET /api/admin/keymatch/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "keymatch_id_1",
          "term": "download",
          "query": "title:download OR content:download",
          "maxSize": 10,
          "boost": 10.0
        }
      }
    }

キーマッチ作成
==============

リクエスト
----------

::

    POST /api/admin/keymatch/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing",
      "maxSize": 5,
      "boost": 20.0
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``term``
     - はい
     - 検索キーワード
   * - ``query``
     - はい
     - マッチ条件クエリ
   * - ``maxSize``
     - いいえ
     - 最大表示件数（デフォルト: 10）
   * - ``boost``
     - いいえ
     - ブースト値（デフォルト: 1.0）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_keymatch_id",
        "created": true
      }
    }

キーマッチ更新
==============

リクエスト
----------

::

    PUT /api/admin/keymatch/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_keymatch_id",
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing OR content:price",
      "maxSize": 10,
      "boost": 15.0,
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_keymatch_id",
        "created": false
      }
    }

キーマッチ削除
==============

リクエスト
----------

::

    DELETE /api/admin/keymatch/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_keymatch_id",
        "created": false
      }
    }

使用例
======

製品ページのキーマッチ作成
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "maxSize": 10,
           "boost": 15.0
         }'

サポートページのキーマッチ
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "query": "url:*/support/* OR url:*/help/* OR url:*/faq/*",
           "maxSize": 5,
           "boost": 20.0
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-elevateword` - エレベートワードAPI
- :doc:`../../admin/keymatch-guide` - キーマッチ管理ガイド
