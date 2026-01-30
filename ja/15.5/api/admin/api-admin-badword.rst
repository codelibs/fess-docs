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
   * - GET/PUT
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

NGワード一覧取得
================

リクエスト
----------

::

    GET /api/admin/badword/settings
    PUT /api/admin/badword/settings

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
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word",
            "targetRole": "",
            "targetLabel": ""
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
          "suggestWord": "inappropriate_word",
          "targetRole": "",
          "targetLabel": ""
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
      "suggestWord": "spam_keyword",
      "targetRole": "guest",
      "targetLabel": ""
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
     - 除外するキーワード
   * - ``targetRole``
     - いいえ
     - 対象ロール（空の場合は全ロール）
   * - ``targetLabel``
     - いいえ
     - 対象ラベル（空の場合は全ラベル）

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
      "targetRole": "guest",
      "targetLabel": "",
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

使用例
======

スパムキーワードの除外
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam",
           "targetRole": "",
           "targetLabel": ""
         }'

特定ロール向けのNGワード
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "internal",
           "targetRole": "guest",
           "targetLabel": ""
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-suggest` - サジェスト管理API
- :doc:`api-admin-elevateword` - エレベートワードAPI
- :doc:`../../admin/badword-guide` - NGワード管理ガイド
