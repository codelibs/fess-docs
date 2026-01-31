==========================
AccessToken API
==========================

概要
====

AccessToken APIは、|Fess| のAPIアクセストークンを管理するためのAPIです。
トークンの作成、更新、削除などを操作できます。

ベースURL
=========

::

    /api/admin/accesstoken

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
     - アクセストークン一覧取得
   * - GET
     - /setting/{id}
     - アクセストークン取得
   * - POST
     - /setting
     - アクセストークン作成
   * - PUT
     - /setting
     - アクセストークン更新
   * - DELETE
     - /setting/{id}
     - アクセストークン削除

アクセストークン一覧取得
========================

リクエスト
----------

::

    GET /api/admin/accesstoken/settings
    PUT /api/admin/accesstoken/settings

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
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "token",
            "expiredTime": 1735689600000,
            "permissions": ["admin"]
          }
        ],
        "total": 5
      }
    }

アクセストークン取得
====================

リクエスト
----------

::

    GET /api/admin/accesstoken/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "token_id_1",
          "name": "API Token 1",
          "token": "abcd1234efgh5678",
          "parameterName": "token",
          "expiredTime": 1735689600000,
          "permissions": ["admin"]
        }
      }
    }

アクセストークン作成
====================

リクエスト
----------

::

    POST /api/admin/accesstoken/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Integration API Token",
      "parameterName": "token",
      "permissions": ["user"]
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
     - トークン名
   * - ``token``
     - いいえ
     - トークン文字列（未指定の場合は自動生成）
   * - ``parameterName``
     - いいえ
     - パラメーター名（デフォルト: "token"）
   * - ``expiredTime``
     - いいえ
     - 有効期限（Unix時間ミリ秒）
   * - ``permissions``
     - いいえ
     - 許可ロール

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "token": "generated_token_string",
        "created": true
      }
    }

アクセストークン更新
====================

リクエスト
----------

::

    PUT /api/admin/accesstoken/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_token_id",
      "name": "Updated API Token",
      "parameterName": "token",
      "expiredTime": 1767225600000,
      "permissions": ["user", "editor"],
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_token_id",
        "created": false
      }
    }

アクセストークン削除
====================

リクエスト
----------

::

    DELETE /api/admin/accesstoken/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_token_id",
        "created": false
      }
    }

使用例
======

APIトークン作成
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/accesstoken/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "External App Token",
           "parameterName": "token",
           "permissions": ["guest"]
         }'

トークンを使用したAPI呼び出し
-----------------------------

.. code-block:: bash

    # トークンをパラメーターとして使用
    curl "http://localhost:8080/json/?q=test&token=your_token_here"

    # トークンをAuthorizationヘッダーとして使用
    curl "http://localhost:8080/json/?q=test" \
         -H "Authorization: Bearer your_token_here"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`../search-api` - 検索API
- :doc:`../../admin/accesstoken-guide` - アクセストークン管理ガイド
