==========================
Role API
==========================

概要
====

Role APIは、|Fess| のロールを管理するためのAPIです。
ロールの作成、更新、削除などを操作できます。

ベースURL
=========

::

    /api/admin/role

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
     - ロール一覧取得
   * - GET
     - /setting/{id}
     - ロール取得
   * - POST
     - /setting
     - ロール作成
   * - PUT
     - /setting
     - ロール更新
   * - DELETE
     - /setting/{id}
     - ロール削除

ロール一覧取得
==============

リクエスト
----------

::

    GET /api/admin/role/settings

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
     - 1ページあたりの件数（デフォルト: 25。``fess_config.properties`` の ``paging.page.size`` で変更可能）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始、デフォルト: 1。0以下を指定した場合は1として扱われます）
   * - ``id``
     - String
     - いいえ
     - 指定したロールIDで完全一致フィルタリングします

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "role_id_1",
            "name": "admin",
            "versionNo": 1
          },
          {
            "id": "role_id_2",
            "name": "user",
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

ロール取得
==========

リクエスト
----------

::

    GET /api/admin/role/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "role_id_1",
          "name": "admin",
          "versionNo": 1
        }
      }
    }

ロール作成
==========

リクエスト
----------

::

    POST /api/admin/role/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "editor"
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
     - ロール名（最大100文字）
   * - ``attributes``
     - いいえ
     - 属性のマップ。値は文字列で指定します

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_role_id",
        "created": true
      }
    }

ロール更新
==========

リクエスト
----------

::

    PUT /api/admin/role/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_role_id",
      "name": "editor_updated",
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
     - 更新対象のロールID
   * - ``name``
     - はい
     - ロール名（最大100文字）
   * - ``attributes``
     - いいえ
     - 属性のマップ。値は文字列で指定します
   * - ``versionNo``
     - はい
     - 楽観的ロック用のバージョン番号。ロール取得で得た ``versionNo`` の値を指定します

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_role_id",
        "created": false
      }
    }

ロール削除
==========

リクエスト
----------

::

    DELETE /api/admin/role/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_role_id",
        "created": false
      }
    }

使用例
======

新規ロール作成
--------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/role/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "content_manager"
         }'

ロール一覧取得
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-user` - ユーザー管理API
- :doc:`api-admin-group` - グループ管理API
- :doc:`../../admin/role-guide` - ロール管理ガイド
