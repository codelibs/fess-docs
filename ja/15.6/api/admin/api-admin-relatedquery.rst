==========================
RelatedQuery API
==========================

概要
====

RelatedQuery APIは、|Fess| の関連クエリを管理するためのAPIです。
特定の検索クエリに対して関連する検索キーワードを提案できます。

ベースURL
=========

::

    /api/admin/relatedquery

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
     - 関連クエリ一覧取得
   * - GET
     - /setting/{id}
     - 関連クエリ取得
   * - POST
     - /setting
     - 関連クエリ作成
   * - PUT
     - /setting
     - 関連クエリ更新
   * - DELETE
     - /setting/{id}
     - 関連クエリ削除

関連クエリ一覧取得
==================

リクエスト
----------

::

    GET /api/admin/relatedquery/settings
    PUT /api/admin/relatedquery/settings

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
            "id": "query_id_1",
            "term": "fess",
            "queries": ["fess tutorial", "fess installation", "fess configuration"]
          }
        ],
        "total": 5
      }
    }

関連クエリ取得
==============

リクエスト
----------

::

    GET /api/admin/relatedquery/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": ["fess tutorial", "fess installation", "fess configuration"],
          "virtualHost": ""
        }
      }
    }

関連クエリ作成
==============

リクエスト
----------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": ["search tutorial", "search syntax", "advanced search"],
      "virtualHost": ""
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
   * - ``queries``
     - はい
     - 関連クエリの配列
   * - ``virtualHost``
     - いいえ
     - 仮想ホスト

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

関連クエリ更新
==============

リクエスト
----------

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": ["search tutorial", "search syntax", "advanced search", "search tips"],
      "virtualHost": "",
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

関連クエリ削除
==============

リクエスト
----------

::

    DELETE /api/admin/relatedquery/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_query_id",
        "created": false
      }
    }

使用例
======

製品関連のクエリ
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": ["product features", "product pricing", "product comparison", "product reviews"]
         }'

ヘルプ関連のクエリ
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": ["help center", "help documentation", "help contact support"]
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-relatedcontent` - 関連コンテンツAPI
- :doc:`api-admin-suggest` - サジェスト管理API
- :doc:`../../admin/relatedquery-guide` - 関連クエリ管理ガイド
