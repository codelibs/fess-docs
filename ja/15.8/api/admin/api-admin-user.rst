==========================
User API
==========================

概要
====

User APIは、|Fess| のユーザーアカウントを管理するためのREST APIです。
ユーザーの作成・取得・更新・削除、およびロールやグループの割り当てを操作できます。

このAPIは管理用APIであり、利用には管理用アクセストークンによる認証が必要です。
認証方法や共通仕様については :doc:`api-admin-overview` を参照してください。

すべてのレスポンスは ``response`` オブジェクトでラップされ、次の共通フィールドを含みます。

- ``version`` : |Fess| の製品バージョン文字列
- ``status`` : 処理結果のステータスコード（``0`` =正常、``1`` =リクエスト不正、``2`` =システムエラー、``3`` =認証エラー、``9`` =失敗）

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
   :widths: 15 10 10 65

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``size``
     - Integer
     - いいえ
     - 1ページあたりの件数。デフォルトは設定値 ``paging.page.size`` （既定値: 25）。
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始）。デフォルトは 1。

.. note::

   現在の実装では、ユーザー一覧エンドポイントは ``size`` ・``page`` パラメーターを反映しません。
   常に1ページ目を、サーバー設定 ``paging.page.size`` （既定値: 25）の件数で、ユーザー名（``name``）の昇順で返します。
   一致したユーザーの総件数は ``response.total`` で確認できます。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "YWRtaW4=",
            "name": "admin",
            "attributes": {
              "surname": "Administrator",
              "givenName": "System",
              "mail": "admin@example.com"
            },
            "roles": ["admin"],
            "groups": [],
            "versionNo": 1
          }
        ],
        "total": 10
      }
    }

- ``settings`` : 現在のページに含まれるユーザーの配列
- ``total`` : 条件に一致したユーザーの総件数

ユーザー取得
============

リクエスト
----------

::

    GET /api/admin/user/setting/{id}

``{id}`` には、対象ユーザーのドキュメントIDを指定します。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": "YWRtaW4=",
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
          "groups": [],
          "versionNo": 1
        }
      }
    }

.. note::

   ``attributes`` には、``name`` ・``password`` ・``roles`` ・``groups`` を除き、ユーザーに保存されているすべての属性が含まれます。
   ``password`` はレスポンスに含まれません。

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
   :widths: 20 10 70

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
     - 確認用パスワード
   * - ``attributes``
     - いいえ
     - 属性のマップ（後述）
   * - ``roles``
     - いいえ
     - ロールIDの配列
   * - ``groups``
     - いいえ
     - グループIDの配列

.. note::

   REST APIでは、パスワードの必須チェック、``password`` と ``confirmPassword`` の一致チェック、
   パスワードポリシー検証は行われません（これらは管理画面でのみ適用されます）。
   運用上は、一致する有効な ``password`` を指定することを推奨します。

``attributes`` のキーには、ユーザーエンティティの属性名（LDAPスキーマに由来する項目名）を指定します。
代表的なキーは次のとおりです。

- ``surname`` 、``givenName`` 、``displayName`` 、``mail``
- ``telephoneNumber`` 、``mobile`` 、``homePhone``
- ``employeeNumber`` 、``title`` 、``description`` 、``homeDirectory``
- ``uidNumber`` 、``gidNumber``

``uidNumber`` と ``gidNumber`` は数値である必要があります（更新時に型が検証されます）。
このほかにも多くのLDAP属性キーを指定できます。

.. note::

   作成時、ユーザーのID（ドキュメントID）は、ユーザー名をBase64 URLエンコードした値として自動生成されます
   （例: ユーザー名 ``admin`` の場合は ``YWRtaW4=`` ）。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

- ``id`` : 作成されたユーザーのドキュメントID
- ``created`` : 作成された場合は ``true``

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

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - フィールド
     - 必須
     - 説明
   * - ``id``
     - はい
     - 更新対象ユーザーのドキュメントID
   * - ``name``
     - はい
     - ユーザー名（ログインID）
   * - ``versionNo``
     - はい
     - バージョン番号（楽観的ロック用）
   * - ``password``
     - いいえ
     - 新しいパスワード（指定した場合のみ更新）
   * - ``confirmPassword``
     - いいえ
     - 確認用パスワード
   * - ``attributes``
     - いいえ
     - 属性のマップ（「ユーザー作成」を参照）
   * - ``roles``
     - いいえ
     - ロールIDの配列
   * - ``groups``
     - いいえ
     - グループIDの配列

.. note::

   更新時は ``id`` ・``name`` ・``versionNo`` が必須です。
   ``versionNo`` は対象ユーザーの取得（GET）時に返される値で、OpenSearchドキュメントのバージョンに対応します。
   値が現在のバージョンと一致しない場合、競合と判断され更新は拒否されます。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

- ``created`` : 更新の場合は ``false``

ユーザー削除
============

リクエスト
----------

::

    DELETE /api/admin/user/setting/{id}

``{id}`` には、削除対象ユーザーのドキュメントIDを指定します。

.. note::

   ログイン中のユーザー自身を削除することはできません。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

- ``id`` : 削除されたユーザーのドキュメントID

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
