==========================
BoostDoc API
==========================

概要
====

BoostDoc APIは、|Fess| のドキュメントブースト設定を管理するためのAPIです。
特定の条件に一致するドキュメントの検索順位を調整できます。

ベースURL
=========

::

    /api/admin/boostdoc

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
     - ドキュメントブースト一覧取得
   * - GET
     - /setting/{id}
     - ドキュメントブースト取得
   * - POST
     - /setting
     - ドキュメントブースト作成
   * - PUT
     - /setting
     - ドキュメントブースト更新
   * - DELETE
     - /setting/{id}
     - ドキュメントブースト削除

ドキュメントブースト一覧取得
============================

リクエスト
----------

::

    GET /api/admin/boostdoc/settings
    PUT /api/admin/boostdoc/settings

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
            "id": "boostdoc_id_1",
            "urlExpr": ".*docs\\.example\\.com.*",
            "boostExpr": "3.0",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

ドキュメントブースト取得
========================

リクエスト
----------

::

    GET /api/admin/boostdoc/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "urlExpr": ".*docs\\.example\\.com.*",
          "boostExpr": "3.0",
          "sortOrder": 0
        }
      }
    }

ドキュメントブースト作成
========================

リクエスト
----------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "5.0",
      "sortOrder": 0
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``urlExpr``
     - はい
     - URL正規表現パターン
   * - ``boostExpr``
     - はい
     - ブースト式（数値または式）
   * - ``sortOrder``
     - いいえ
     - 適用順序

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

ドキュメントブースト更新
========================

リクエスト
----------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

ドキュメントブースト削除
========================

リクエスト
----------

::

    DELETE /api/admin/boostdoc/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_boostdoc_id",
        "created": false
      }
    }

ブースト式の例
==============

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ブースト式
     - 説明
   * - ``2.0``
     - 固定値でブースト
   * - ``doc['boost'].value * 2``
     - ドキュメントのboost値を2倍
   * - ``Math.log(doc['click_count'].value + 1)``
     - クリック数に基づく対数スケールブースト
   * - ``doc['last_modified'].value > now - 7d ? 3.0 : 1.0``
     - 最終更新日が1週間以内なら3倍

使用例
======

ドキュメントサイトのブースト
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*docs\\.example\\.com.*",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

新しいコンテンツのブースト
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*",
           "boostExpr": "doc[\"last_modified\"].value > now - 30d ? 2.0 : 1.0",
           "sortOrder": 10
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-elevateword` - エレベートワードAPI
- :doc:`../../admin/boostdoc-guide` - ドキュメントブースト管理ガイド
