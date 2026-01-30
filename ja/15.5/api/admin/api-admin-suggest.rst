==========================
Suggest API
==========================

概要
====

Suggest APIは、|Fess| のサジェスト機能を管理するためのAPIです。
サジェストワードの追加、削除、更新などを操作できます。

ベースURL
=========

::

    /api/admin/suggest

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
     - サジェストワード一覧取得
   * - GET
     - /setting/{id}
     - サジェストワード取得
   * - POST
     - /setting
     - サジェストワード作成
   * - PUT
     - /setting
     - サジェストワード更新
   * - DELETE
     - /setting/{id}
     - サジェストワード削除
   * - DELETE
     - /delete-all
     - 全サジェストワード削除

サジェストワード一覧取得
========================

リクエスト
----------

::

    GET /api/admin/suggest/settings
    PUT /api/admin/suggest/settings

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
            "id": "suggest_id_1",
            "text": "fess",
            "reading": "フェス",
            "fields": ["title", "content"],
            "tags": ["product"],
            "roles": ["guest"],
            "lang": "ja",
            "score": 1.0
          }
        ],
        "total": 100
      }
    }

サジェストワード取得
====================

リクエスト
----------

::

    GET /api/admin/suggest/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "suggest_id_1",
          "text": "fess",
          "reading": "フェス",
          "fields": ["title", "content"],
          "tags": ["product"],
          "roles": ["guest"],
          "lang": "ja",
          "score": 1.0
        }
      }
    }

サジェストワード作成
====================

リクエスト
----------

::

    POST /api/admin/suggest/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "text": "search engine",
      "reading": "サーチエンジン",
      "fields": ["title"],
      "tags": ["feature"],
      "roles": ["guest"],
      "lang": "en",
      "score": 1.0
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``text``
     - はい
     - サジェストテキスト
   * - ``reading``
     - いいえ
     - 読み仮名
   * - ``fields``
     - いいえ
     - 対象フィールド
   * - ``tags``
     - いいえ
     - タグ
   * - ``roles``
     - いいえ
     - アクセス許可ロール
   * - ``lang``
     - いいえ
     - 言語コード
   * - ``score``
     - いいえ
     - スコア（デフォルト: 1.0）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_suggest_id",
        "created": true
      }
    }

サジェストワード更新
====================

リクエスト
----------

::

    PUT /api/admin/suggest/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_suggest_id",
      "text": "search engine",
      "reading": "サーチエンジン",
      "fields": ["title", "content"],
      "tags": ["feature", "popular"],
      "roles": ["guest"],
      "lang": "en",
      "score": 2.0,
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_suggest_id",
        "created": false
      }
    }

サジェストワード削除
====================

リクエスト
----------

::

    DELETE /api/admin/suggest/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_suggest_id",
        "created": false
      }
    }

全サジェストワード削除
======================

リクエスト
----------

::

    DELETE /api/admin/suggest/delete-all

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "count": 250
      }
    }

使用例
======

人気キーワードの追加
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/suggest/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "text": "getting started",
           "fields": ["title"],
           "tags": ["tutorial"],
           "roles": ["guest"],
           "lang": "en",
           "score": 5.0
         }'

サジェストの一括削除
--------------------

.. code-block:: bash

    # 全サジェストを削除
    curl -X DELETE "http://localhost:8080/api/admin/suggest/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-badword` - NGワードAPI
- :doc:`api-admin-elevateword` - エレベートワードAPI
- :doc:`../../admin/suggest-guide` - サジェスト管理ガイド
