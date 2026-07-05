==========================
LabelType API
==========================

概要
====

LabelType APIは、|Fess| のラベルタイプを管理するためのAPIです。
検索結果のラベル分類、フィルタリング用のラベルタイプを操作できます。

ベースURL
=========

::

    /api/admin/labeltype

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
     - ラベルタイプ一覧取得
   * - GET
     - /setting/{id}
     - ラベルタイプ取得
   * - POST
     - /setting
     - ラベルタイプ作成
   * - PUT
     - /setting
     - ラベルタイプ更新
   * - DELETE
     - /setting/{id}
     - ラベルタイプ削除

ラベルタイプ一覧取得
====================

リクエスト
----------

::

    GET /api/admin/labeltype/settings
    PUT /api/admin/labeltype/settings

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
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

ラベルタイプ取得
================

リクエスト
----------

::

    GET /api/admin/labeltype/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "sortOrder": 0,
          "permissions": [],
          "virtualHost": ""
        }
      }
    }

ラベルタイプ作成
================

リクエスト
----------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": ["guest"]
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - ラベル表示名
   * - ``value``
     - はい
     - ラベル値（検索時に使用）
   * - ``includedPaths``
     - いいえ
     - ラベル対象パスの正規表現（複数の場合は改行区切り）
   * - ``excludedPaths``
     - いいえ
     - ラベル除外パスの正規表現（複数の場合は改行区切り）
   * - ``sortOrder``
     - いいえ
     - 表示順序
   * - ``permissions``
     - いいえ
     - アクセス許可ロール
   * - ``virtualHost``
     - いいえ
     - 仮想ホスト

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

ラベルタイプ更新
================

リクエスト
----------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": ["guest"],
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

ラベルタイプ削除
================

リクエスト
----------

::

    DELETE /api/admin/labeltype/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_label_id",
        "created": false
      }
    }

使用例
======

ドキュメント用ラベル作成
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": ["guest"]
         }'

ラベルを使用した検索
--------------------

.. code-block:: bash

    # ラベルでフィルタリング
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`../api-search` - 検索API
- :doc:`../../admin/labeltype-guide` - ラベルタイプ管理ガイド
