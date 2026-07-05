==========================
RelatedContent API
==========================

概要
====

RelatedContent APIは、|Fess| の関連コンテンツを管理するためのAPIです。
特定のキーワードに関連するコンテンツをカスタム表示できます。

ベースURL
=========

::

    /api/admin/relatedcontent

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
     - 関連コンテンツ一覧取得
   * - GET
     - /setting/{id}
     - 関連コンテンツ取得
   * - POST
     - /setting
     - 関連コンテンツ作成
   * - PUT
     - /setting
     - 関連コンテンツ更新
   * - DELETE
     - /setting/{id}
     - 関連コンテンツ削除

関連コンテンツ一覧取得
======================

リクエスト
----------

::

    GET /api/admin/relatedcontent/settings
    PUT /api/admin/relatedcontent/settings

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
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

関連コンテンツ取得
==================

リクエスト
----------

::

    GET /api/admin/relatedcontent/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
          "sortOrder": 0,
          "virtualHost": ""
        }
      }
    }

関連コンテンツ作成
==================

リクエスト
----------

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "content": "<div class='related'><h3>About Search</h3><p>Learn more about search features...</p></div>",
      "sortOrder": 0,
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
   * - ``content``
     - はい
     - 表示するHTMLコンテンツ
   * - ``sortOrder``
     - いいえ
     - 表示順序
   * - ``virtualHost``
     - いいえ
     - 仮想ホスト

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

関連コンテンツ更新
==================

リクエスト
----------

::

    PUT /api/admin/relatedcontent/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_content_id",
      "term": "search",
      "content": "<div class='related updated'><h3>About Search</h3><p>Updated information...</p></div>",
      "sortOrder": 0,
      "virtualHost": "",
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

関連コンテンツ削除
==================

リクエスト
----------

::

    DELETE /api/admin/relatedcontent/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_content_id",
        "created": false
      }
    }

使用例
======

製品情報の関連コンテンツ
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "content": "<div class=\"product-info\"><h3>Our Products</h3><ul><li>Product A</li><li>Product B</li></ul></div>",
           "sortOrder": 0
         }'

サポート情報の関連コンテンツ
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "support",
           "content": "<div><p>Need help? Contact: support@example.com</p></div>",
           "sortOrder": 0
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-relatedquery` - 関連クエリAPI
- :doc:`../../admin/relatedcontent-guide` - 関連コンテンツ管理ガイド
