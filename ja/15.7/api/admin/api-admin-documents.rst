==========================
Documents API
==========================

概要
====

Documents APIは、|Fess| のインデックスにドキュメントを一括登録するためのAPIです。
複数のドキュメントをまとめてインデックスに追加できます。

ベースURL
=========

::

    /api/admin/documents

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - PUT
     - /bulk
     - ドキュメント一括登録

ドキュメント一括登録
====================

複数のドキュメントをインデックスに一括で登録します。

リクエスト
----------

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "サンプルページ1",
          "content": "ページ1の本文テキストです。"
        },
        {
          "url": "https://example.com/page2",
          "title": "サンプルページ2",
          "content": "ページ2の本文テキストです。"
        }
      ]
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``documents``
     - はい
     - 登録するドキュメントの配列。各ドキュメントはフィールド名と値のマップで指定します。空配列は指定できません。

各ドキュメントには ``url`` 、 ``title`` 、 ``content`` などのインデックスフィールドを自由に指定できます。
``content_length`` 、 ``favorite_count`` 、 ``click_count`` 、 ``boost`` 、 ``role`` 、 ``last_modified`` 、 ``timestamp`` などが省略された場合は既定値が自動的に補完されます。
また、 ``doc_id`` と ID は登録時に自動生成されます。

レスポンス
----------

レスポンスは登録した各ドキュメントの処理結果を ``items`` 配列で返します。
成功した項目は ``result`` と ``id`` を、失敗した項目は ``result`` と ``message`` を含みます。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "CREATED",
            "id": "0123456789abcdef"
          }
        ]
      }
    }

いずれかの項目で登録が失敗した場合、 ``status`` は ``9`` （FAILED）となり、該当項目には ``message`` フィールドが含まれます。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 9,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "BAD_REQUEST",
            "message": "failure reason ..."
          }
        ]
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``items``
     - 各ドキュメントの処理結果の配列
   * - ``items[].result``
     - 処理結果ステータス（例: ``CREATED``）
   * - ``items[].id``
     - 登録されたドキュメントのID（成功時）
   * - ``items[].message``
     - 失敗理由のメッセージ（失敗時）

使用例
======

ドキュメントの一括登録
----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "サンプルページ1",
               "content": "ページ1の本文テキストです。"
             }
           ]
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-searchlist` - ドキュメント検索・管理API
- :doc:`api-admin-crawlinginfo` - クロール情報API
- :doc:`../../admin/searchlist-guide` - 検索一覧管理ガイド
