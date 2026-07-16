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
   * - GET
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
     - 1ページあたりの件数（デフォルト: 25。\ ``fess_config.properties`` の ``paging.page.size`` で変更可能）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始、デフォルト: 1。0以下を指定した場合は1として扱われます）
   * - ``term``
     - String
     - いいえ
     - 検索キーワードによる絞り込み（ワイルドカード検索）
   * - ``content``
     - String
     - いいえ
     - コンテンツ本文による絞り込み（ワイルドカード検索）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
            "virtualHost": "",
            "sortOrder": 0,
            "createdBy": "admin",
            "createdTime": 1700000000000,
            "updatedBy": "admin",
            "updatedTime": 1700000000000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   ``settings`` の各要素および単一取得の ``setting`` には、保存されているエンティティの
   フィールドがそのまま含まれます。\ ``term``、``content``、``sortOrder``、``virtualHost`` に
   加えて、監査用の ``createdBy``・``createdTime``・``updatedBy``・``updatedTime`` と、
   楽観的ロック用の ``versionNo`` も返されます。\ ``createdTime``・``updatedTime`` は
   エポックからのミリ秒（数値）です。値が未設定（null）のフィールドはレスポンスには
   含まれません。また、すべてのレスポンスの ``response`` オブジェクトには、製品バージョンを
   示す ``version`` が常に含まれます（詳細は :doc:`api-admin-overview` を参照）。

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
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
          "virtualHost": "",
          "sortOrder": 0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   更新（PUT）の際に必要となる ``versionNo`` は、この取得結果に含まれる値を指定します。

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
   :widths: 20 15 65

   * - フィールド
     - 必須
     - 説明
   * - ``term``
     - はい
     - 検索キーワード（最大10000文字）
   * - ``content``
     - はい
     - 表示するHTMLコンテンツ（最大10000文字）
   * - ``sortOrder``
     - いいえ
     - 表示順序（0以上2147483647以下の整数）
   * - ``virtualHost``
     - いいえ
     - 仮想ホスト（最大1000文字）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - フィールド
     - 必須
     - 説明
   * - ``id``
     - はい
     - 更新対象の関連コンテンツID（最大1000文字）
   * - ``term``
     - はい
     - 検索キーワード（最大10000文字）
   * - ``content``
     - はい
     - 表示するHTMLコンテンツ（最大10000文字）
   * - ``sortOrder``
     - いいえ
     - 表示順序（0以上2147483647以下の整数）
   * - ``virtualHost``
     - いいえ
     - 仮想ホスト（最大1000文字）
   * - ``versionNo``
     - はい
     - 楽観的ロック用のバージョン番号。\ ``setting/{id}`` の取得結果に含まれる値を指定します。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

.. note::

   ``createdBy``・``createdTime``・``updatedBy``・``updatedTime`` などの監査フィールドや
   ``crudMode`` をリクエストボディに含めても、サーバー側で自動的に設定されるため無視されます。
   作成・更新時に指定する必要はありません。

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
        "version": "15.8.0",
        "status": 0
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
