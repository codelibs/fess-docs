==========================
Suggest API
==========================

概要
====

Suggest APIは、|Fess| のサジェスト機能を管理するためのAPIです。
サジェストワードの統計情報の取得と、サジェストワードの削除を操作できます。

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
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 300
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
     - サジェストワードの総数
   * - ``setting.documentWordsNum``
     - ドキュメント由来のサジェストワード数
   * - ``setting.queryWordsNum``
     - 検索クエリ由来のサジェストワード数

全サジェストワードの削除
========================

すべてのサジェストワードを削除します。

リクエスト
----------

::

    DELETE /api/admin/suggest/all

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

ドキュメント由来のサジェストワードの削除
========================================

ドキュメントから生成されたサジェストワードを削除します。

リクエスト
----------

::

    DELETE /api/admin/suggest/document

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

検索クエリ由来のサジェストワードの削除
======================================

検索クエリから生成されたサジェストワードを削除します。

リクエスト
----------

::

    DELETE /api/admin/suggest/query

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

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

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-badword` - NGワードAPI
- :doc:`api-admin-elevateword` - エレベートワードAPI
- :doc:`../../admin/suggest-guide` - サジェスト管理ガイド
