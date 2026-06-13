==========================
SearchList API
==========================

概要
====

SearchList APIは、|Fess| のインデックス内のドキュメントを検索・管理するためのAPIです。
ドキュメントの検索、取得、作成、更新、削除を操作できます。

ベースURL
=========

::

    /api/admin/searchlist

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET / PUT
     - /docs
     - ドキュメント検索
   * - GET
     - /doc/{id}
     - ドキュメント取得
   * - POST
     - /doc
     - ドキュメント作成
   * - PUT
     - /doc
     - ドキュメント更新
   * - DELETE
     - /doc/{id}
     - ドキュメント削除（ID指定）
   * - DELETE
     - /query
     - ドキュメント削除（クエリ指定）

ドキュメント検索
================

検索条件に一致するドキュメントを検索します。

リクエスト
----------

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``q``
     - String
     - いいえ
     - 検索クエリ。未指定の場合は全件が対象になります。
   * - ``sort``
     - String
     - いいえ
     - ソートフィールドと方向
   * - ``start``
     - Integer
     - いいえ
     - 検索結果の開始位置
   * - ``offset``
     - Integer
     - いいえ
     - ページングのオフセット
   * - ``num``
     - Integer
     - いいえ
     - 取得件数
   * - ``size``
     - Integer
     - いいえ
     - 取得件数（ ``num`` のエイリアス）
   * - ``lang``
     - String[]
     - いいえ
     - 言語

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "queryId": "...",
        "execTime": "0.05",
        "pageSize": 20,
        "pageNumber": 1,
        "recordCount": 234,
        "recordCountRelation": "EQUAL_TO",
        "pageCount": 12,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "サンプルページ1",
            "content_description": "..."
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
   * - ``queryId``
     - 検索クエリID
   * - ``docs``
     - 検索結果ドキュメントの配列
   * - ``execTime``
     - 検索実行時間
   * - ``pageSize``
     - 1ページあたりの件数
   * - ``pageNumber``
     - 現在のページ番号
   * - ``recordCount``
     - 該当件数
   * - ``recordCountRelation``
     - 該当件数の関係（完全一致か下限値か）
   * - ``pageCount``
     - 総ページ数

ドキュメント取得
================

ドキュメントIDを指定して、1件のドキュメントを取得します。

リクエスト
----------

::

    GET /api/admin/searchlist/doc/{id}

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``id``
     - String
     - はい
     - ドキュメントID（ ``doc_id`` 、パスパラメーター）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "サンプルページ1"
        }
      }
    }

ドキュメント作成
================

新しいドキュメントをインデックスに作成します。

リクエスト
----------

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "サンプルページ1",
        "content": "本文テキストです。"
      }
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``doc``
     - はい
     - 登録するドキュメント。フィールド名と値のマップで指定します。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

ドキュメント更新
================

既存のドキュメントを更新します。

リクエスト
----------

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "更新後のタイトル",
        "content": "更新後の本文テキストです。"
      }
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``doc``
     - はい
     - 更新するドキュメント。フィールド名と値のマップで指定します。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

ドキュメント削除（ID指定）
==========================

ドキュメントIDを指定して削除します。

リクエスト
----------

::

    DELETE /api/admin/searchlist/doc/{id}

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``id``
     - String
     - はい
     - ドキュメントID（ ``doc_id`` 、パスパラメーター）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

ドキュメント削除（クエリ指定）
==============================

検索クエリに一致するドキュメントを一括削除します。

リクエスト
----------

::

    DELETE /api/admin/searchlist/query

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``q``
     - String
     - はい
     - 削除対象の検索クエリ

レスポンス
----------

削除されたドキュメント件数を ``count`` で返します。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "count": 150
      }
    }

使用例
======

ドキュメント検索
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

ドキュメント取得
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

クエリ指定でのドキュメント削除
------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-documents` - ドキュメント一括登録API
- :doc:`api-admin-crawlinginfo` - クロール情報API
- :doc:`../../admin/searchlist-guide` - 検索一覧管理ガイド
