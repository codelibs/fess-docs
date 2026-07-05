==========================
Suggest API
==========================

概要
====

Suggest APIは、|Fess| のサジェスト機能で利用されるサジェストワードを管理するためのAPIです。
サジェストワードの件数に関する統計情報の取得と、サジェストワードの削除を行えます。

サジェストワードには、クロールしたドキュメントから生成されたもの（ドキュメント由来）と、
ユーザーの検索クエリから生成されたもの（検索クエリ由来）があります。本APIでは、これらを
種別ごとに削除したり、すべてまとめて削除したりできます。

認証
====

本APIへのアクセスには、アクセストークンによる認証が必要です。リクエストヘッダーに
アクセストークンを指定してください。

::

    Authorization: Bearer <アクセストークン>

アクセストークンには、Admin APIの権限（既定では ``Radmin-api``）が付与されている必要があります。
アクセストークンの取得方法や権限の詳細は :doc:`api-admin-overview` を参照してください。

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
   * - GET
     - /
     - サジェストワード統計情報の取得
   * - DELETE
     - /all
     - 全サジェストワードの削除
   * - DELETE
     - /document
     - ドキュメント由来のサジェストワードの削除
   * - DELETE
     - /query
     - 検索クエリ由来のサジェストワードの削除

サジェストワード統計情報の取得
==============================

サジェストワードの件数に関する統計情報を取得します。

リクエスト
----------

::

    GET /api/admin/suggest

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 450
        }
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``setting.totalWordsNum``
     - サジェストワードの総数（サジェストインデックスに登録されているサジェストワードの件数）
   * - ``setting.documentWordsNum``
     - ドキュメント由来のサジェストワード数（ドキュメント頻度が1以上のサジェストワードの件数）
   * - ``setting.queryWordsNum``
     - 検索クエリ由来のサジェストワード数（クエリ頻度が1以上のサジェストワードの件数）

.. note::

   ``documentWordsNum`` と ``queryWordsNum`` は排他的ではありません。1つのサジェストワードが
   ドキュメントと検索クエリの両方に由来する場合は、両方の件数に含まれます。このため、
   ``documentWordsNum`` と ``queryWordsNum`` の合計が ``totalWordsNum`` と一致しないことがあります。

全サジェストワードの削除
========================

すべてのサジェストワードを削除します。ドキュメント由来・検索クエリ由来の区別なく、
サジェストインデックス内のすべてのサジェストワードが対象です。

リクエスト
----------

::

    DELETE /api/admin/suggest/all

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

ドキュメント由来のサジェストワードの削除
========================================

ドキュメントから生成されたサジェストワード（ドキュメント由来のサジェストワード）を削除します。

リクエスト
----------

::

    DELETE /api/admin/suggest/document

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

検索クエリ由来のサジェストワードの削除
======================================

検索クエリから生成されたサジェストワード（検索クエリ由来のサジェストワード）を削除します。

リクエスト
----------

::

    DELETE /api/admin/suggest/query

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

エラーレスポンス
================

削除処理に失敗した場合は、HTTPステータス ``400`` とともに、レスポンス本文の ``status`` に
``1``（BAD_REQUEST）が設定され、``message`` にエラーメッセージが含まれます。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "Failed to delete a document."
      }
    }

アクセストークンが未指定・無効な場合や権限が不足している場合は、レスポンス本文の ``status`` に
``3``（UNAUTHORIZED）が設定されます。``status`` の値や HTTP ステータスコードの一覧については、
:doc:`api-admin-overview` を参照してください。

使用例
======

統計情報の取得
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/suggest" \
         -H "Authorization: Bearer YOUR_TOKEN"

全サジェストワードの削除
------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

ドキュメント由来のサジェストワードの削除
----------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/document" \
         -H "Authorization: Bearer YOUR_TOKEN"

検索クエリ由来のサジェストワードの削除
--------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/query" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-badword` - NGワードAPI
- :doc:`api-admin-elevateword` - エレベートワードAPI
- :doc:`../../admin/suggest-guide` - サジェスト管理ガイド
