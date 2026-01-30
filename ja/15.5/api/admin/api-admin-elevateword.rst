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
   * - GET/PUT
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

エレベートワード一覧取得
========================

リクエスト
----------

::

    GET /api/admin/elevateword/settings
    PUT /api/admin/elevateword/settings

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
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "フェス",
            "permissions": [],
            "boost": 10.0,
            "targetRole": "",
            "targetLabel": ""
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
          "permissions": [],
          "boost": 10.0,
          "targetRole": "",
          "targetLabel": ""
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
      "permissions": ["guest"],
      "boost": 15.0,
      "targetRole": "user",
      "targetLabel": "docs"
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
     - アクセス許可ロール
   * - ``boost``
     - いいえ
     - ブースト値（デフォルト: 1.0）
   * - ``targetRole``
     - いいえ
     - 対象ロール
   * - ``targetLabel``
     - いいえ
     - 対象ラベル

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
      "permissions": ["guest", "user"],
      "boost": 20.0,
      "targetRole": "user",
      "targetLabel": "docs",
      "versionNo": 1
    }

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
           "boost": 20.0,
           "permissions": ["guest"]
         }'

特定ラベルへのエレベート
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 10.0,
           "targetLabel": "technical_docs",
           "permissions": ["guest"]
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-keymatch` - キーマッチAPI
- :doc:`api-admin-boostdoc` - ドキュメントブーストAPI
- :doc:`../../admin/elevateword-guide` - エレベートワード管理ガイド
