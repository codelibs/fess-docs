==========================
Storage API
==========================

概要
====

Storage APIは、|Fess| のストレージ管理を行うためのAPIです。
インデックスのストレージ使用状況や最適化を操作できます。

ベースURL
=========

::

    /api/admin/storage

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
     - ストレージ情報取得
   * - POST
     - /optimize
     - インデックス最適化
   * - POST
     - /flush
     - インデックスフラッシュ

ストレージ情報取得
==================

リクエスト
----------

::

    GET /api/admin/storage

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "storage": {
          "indices": [
            {
              "name": "fess.20250129",
              "status": "open",
              "health": "green",
              "docsCount": 123456,
              "docsDeleted": 234,
              "storeSize": "5.2gb",
              "primariesStoreSize": "2.6gb",
              "shards": 5,
              "replicas": 1
            }
          ],
          "totalStoreSize": "5.2gb",
          "totalDocsCount": 123456,
          "clusterHealth": "green",
          "diskUsage": {
            "total": "107374182400",
            "available": "53687091200",
            "used": "53687091200",
            "usedPercent": 50.0
          }
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
   * - ``indices``
     - インデックス一覧
   * - ``name``
     - インデックス名
   * - ``status``
     - インデックスステータス（open/close）
   * - ``health``
     - ヘルスステータス（green/yellow/red）
   * - ``docsCount``
     - ドキュメント数
   * - ``docsDeleted``
     - 削除済みドキュメント数
   * - ``storeSize``
     - ストレージサイズ
   * - ``primariesStoreSize``
     - プライマリシャードのサイズ
   * - ``shards``
     - シャード数
   * - ``replicas``
     - レプリカ数
   * - ``totalStoreSize``
     - 総ストレージサイズ
   * - ``totalDocsCount``
     - 総ドキュメント数
   * - ``clusterHealth``
     - クラスターヘルス
   * - ``diskUsage``
     - ディスク使用状況

インデックス最適化
==================

リクエスト
----------

::

    POST /api/admin/storage/optimize
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129",
      "maxNumSegments": 1,
      "onlyExpungeDeletes": false,
      "flush": true
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``index``
     - いいえ
     - インデックス名（未指定の場合は全インデックス）
   * - ``maxNumSegments``
     - いいえ
     - 最大セグメント数（デフォルト: 1）
   * - ``onlyExpungeDeletes``
     - いいえ
     - 削除済みドキュメントのみ削除（デフォルト: false）
   * - ``flush``
     - いいえ
     - 最適化後にフラッシュ（デフォルト: true）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index optimization started"
      }
    }

インデックスフラッシュ
======================

リクエスト
----------

::

    POST /api/admin/storage/flush
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``index``
     - いいえ
     - インデックス名（未指定の場合は全インデックス）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index flushed successfully"
      }
    }

使用例
======

ストレージ情報の取得
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage" \
         -H "Authorization: Bearer YOUR_TOKEN"

全インデックスの最適化
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "maxNumSegments": 1,
           "flush": true
         }'

特定インデックスの最適化
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129",
           "maxNumSegments": 1,
           "onlyExpungeDeletes": false
         }'

削除済みドキュメントの削除
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "onlyExpungeDeletes": true
         }'

インデックスのフラッシュ
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/flush" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129"
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-systeminfo` - システム情報API
- :doc:`../../admin/storage-guide` - ストレージ管理ガイド
