==========================
Group API
==========================

概要
====

Group APIは、|Fess| のグループを管理するためのAPIです。
グループの作成、更新、削除などを操作できます。

ベースURL
=========

::

    /api/admin/group

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
     - グループ一覧取得
   * - GET
     - /setting/{id}
     - グループ取得
   * - POST
     - /setting
     - グループ作成
   * - PUT
     - /setting
     - グループ更新
   * - DELETE
     - /setting/{id}
     - グループ削除

グループ一覧取得
================

リクエスト
----------

::

    GET /api/admin/group/settings

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
     - 1ページあたりの件数（デフォルト: 25）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始、デフォルト: 1）
   * - ``id``
     - String
     - いいえ
     - 指定したグループIDで完全一致フィルタリングします

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "group_id_1",
            "name": "Engineering",
            "attributes": {
              "gidNumber": "1000"
            },
            "versionNo": 1
          },
          {
            "id": "group_id_2",
            "name": "Sales",
            "attributes": {
              "gidNumber": "1001"
            },
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

グループ取得
============

リクエスト
----------

::

    GET /api/admin/group/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "group_id_1",
          "name": "Engineering",
          "attributes": {
            "gidNumber": "1000"
          },
          "versionNo": 1
        }
      }
    }

グループ作成
============

リクエスト
----------

::

    POST /api/admin/group/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Marketing",
      "attributes": {
        "gidNumber": "1002"
      }
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - グループ名（最大100文字）
   * - ``attributes``
     - いいえ
     - 属性のマップ（``gidNumber`` などのLDAP属性を含む）。値は文字列で指定します

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_group_id",
        "created": true
      }
    }

グループ更新
============

リクエスト
----------

::

    PUT /api/admin/group/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_group_id",
      "name": "Marketing Team",
      "attributes": {
        "gidNumber": "1002"
      },
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
     - 更新対象のグループID
   * - ``name``
     - はい
     - グループ名（最大100文字）
   * - ``attributes``
     - いいえ
     - 属性のマップ（``gidNumber`` などのLDAP属性を含む）。値は文字列で指定します
   * - ``versionNo``
     - はい
     - 楽観的ロック用のバージョン番号。グループ取得で得た ``versionNo`` の値を指定します

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_group_id",
        "created": false
      }
    }

グループ削除
============

リクエスト
----------

::

    DELETE /api/admin/group/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_group_id",
        "created": false
      }
    }

使用例
======

新規グループ作成
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/group/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Product Team",
           "attributes": {
             "gidNumber": "2000"
           }
         }'

グループ一覧取得
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/group/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-user` - ユーザー管理API
- :doc:`api-admin-role` - ロール管理API
- :doc:`../../admin/group-guide` - グループ管理ガイド
