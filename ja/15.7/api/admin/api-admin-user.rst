==========================
User API
==========================

概要
====

User APIは、|Fess| のユーザーアカウントを管理するためのAPIです。
ユーザーの作成、更新、削除、権限設定などを操作できます。

ベースURL
=========

::

    /api/admin/user

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
     - ユーザー一覧取得
   * - GET
     - /setting/{id}
     - ユーザー取得
   * - POST
     - /setting
     - ユーザー作成
   * - PUT
     - /setting
     - ユーザー更新
   * - DELETE
     - /setting/{id}
     - ユーザー削除

ユーザー一覧取得
================

リクエスト
----------

::

    GET /api/admin/user/settings

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

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
            "id": "user_id_1",
            "name": "admin",
            "attributes": {
              "surname": "Administrator",
              "givenName": "System",
              "mail": "admin@example.com"
            },
            "roles": ["admin"],
            "groups": []
          }
        ],
        "total": 10
      }
    }

ユーザー取得
============

リクエスト
----------

::

    GET /api/admin/user/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "user_id_1",
          "name": "admin",
          "attributes": {
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "telephoneNumber": "",
            "uidNumber": "",
            "gidNumber": "",
            "homeDirectory": ""
          },
          "roles": ["admin"],
          "groups": []
        }
      }
    }

ユーザー作成
============

リクエスト
----------

::

    POST /api/admin/user/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "testuser",
      "password": "securepassword",
      "confirmPassword": "securepassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User",
        "mail": "testuser@example.com"
      },
      "roles": ["user"],
      "groups": ["group_id_1"]
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - ユーザー名（ログインID）
   * - ``password``
     - いいえ
     - パスワード
   * - ``confirmPassword``
     - いいえ
     - 確認用パスワード（``password`` と一致させます）
   * - ``attributes``
     - いいえ
     - 属性のマップ（``surname`` ・``givenName`` ・``mail`` ・``telephoneNumber`` などのLDAP属性を含む）
   * - ``roles``
     - いいえ
     - ロールID配列
   * - ``groups``
     - いいえ
     - グループID配列

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

ユーザー更新
============

リクエスト
----------

::

    PUT /api/admin/user/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_user_id",
      "name": "testuser",
      "password": "newpassword",
      "confirmPassword": "newpassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User Updated",
        "mail": "testuser.updated@example.com"
      },
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

ユーザー削除
============

リクエスト
----------

::

    DELETE /api/admin/user/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

使用例
======

新規ユーザー作成
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "john.doe",
           "password": "SecureP@ss123",
           "confirmPassword": "SecureP@ss123",
           "attributes": {
             "surname": "Doe",
             "givenName": "John",
             "mail": "john.doe@example.com"
           },
           "roles": ["user"],
           "groups": []
         }'

ユーザーのロール変更
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "user_id_123",
           "name": "john.doe",
           "roles": ["user", "editor", "admin"],
           "versionNo": 1
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-role` - ロール管理API
- :doc:`api-admin-group` - グループ管理API
- :doc:`../../admin/user-guide` - ユーザー管理ガイド
