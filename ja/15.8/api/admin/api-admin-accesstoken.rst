==========================
AccessToken API
==========================

概要
====

AccessToken APIは、|Fess| のAPIアクセストークンを管理するためのAPIです。
トークンの作成、取得、更新、削除を実行できます。

アクセストークンは、|Fess| の検索APIやAdmin APIをプログラムから呼び出す際の認証に使用します。
このAPIを含むAdmin APIの共通仕様（認証方法、レスポンス形式、``status`` の値、エラーレスポンス、
HTTPステータスコード）については :doc:`api-admin-overview` を参照してください。

.. note::

   このAPIにアクセスするには、リクエストに使用するアクセストークンに ``api.admin.access.permissions``
   （既定値 ``{role}admin-api`` ）に一致する権限が必要です。

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
   * - GET
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
     - 1ページあたりの件数（デフォルト: 25。 ``paging.page.size`` で変更可能）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始。デフォルト: 1）
   * - ``id``
     - String
     - いいえ
     - 指定したIDのトークンのみを取得するフィルター

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "permission",
            "permissions": "{role}admin-api",
            "expires": "2026-01-01T00:00:00",
            "createdBy": "admin",
            "createdTime": 1735689600000,
            "updatedBy": "admin",
            "updatedTime": 1735689600000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   各トークンオブジェクトには、 ``createdBy`` 、 ``createdTime`` 、 ``updatedBy`` 、
   ``updatedTime`` 、 ``versionNo`` といった監査情報・バージョン情報も含まれます。
   ``createdTime`` と ``updatedTime`` はエポックからのミリ秒（数値）です。
   値が ``null`` のフィールドはレスポンスから除外されます。
   ``permissions`` は改行（ ``\n`` ）区切りの文字列として返されます。

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
          "parameterName": "permission",
          "permissions": "{role}admin-api",
          "expires": "2026-01-01T00:00:00",
          "createdBy": "admin",
          "createdTime": 1735689600000,
          "updatedBy": "admin",
          "updatedTime": 1735689600000,
          "versionNo": 1
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
      "permissions": "{role}admin-api",
      "expires": "2026-01-01T00:00:00"
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
     - トークン名（最大1000文字）
   * - ``permissions``
     - いいえ
     - このトークンに付与する権限。改行（ ``\n`` ）区切りで複数指定できます（例: ``{role}admin-api`` ）。Admin APIを呼び出すトークンには、 ``api.admin.access.permissions`` （既定値 ``{role}admin-api`` ）に一致する権限が必要です。
   * - ``parameterName``
     - いいえ
     - 追加権限を渡すためのリクエストパラメーター名。このトークンで認証されたリクエストに、ここで指定した名前のパラメーターが含まれる場合、その値が ``permissions`` に追加されます。省略した場合は設定されません。
   * - ``expires``
     - いいえ
     - 有効期限。 ``YYYY-MM-DDTHH:MM:SS`` 形式の文字列で指定します（例: ``2026-01-01T00:00:00`` ）。省略した場合は無期限です。

.. note::

   トークン文字列（ ``token`` ）はサーバー側で自動生成されます。リクエストボディに ``token``
   を指定しても無視されます。作成レスポンスにはトークン文字列が含まれないため、生成された
   トークン文字列は「アクセストークン取得」（ ``GET /setting/{id}`` ）で取得してください。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
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
      "permissions": "{role}admin-api\n{role}user",
      "expires": "2026-01-01T00:00:00",
      "versionNo": 1
    }

フィールド説明
~~~~~~~~~~~~~~

更新では、作成時のフィールドに加えて以下のフィールドを使用します。

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - フィールド
     - 必須
     - 説明
   * - ``id``
     - はい
     - 更新対象のトークンID
   * - ``versionNo``
     - はい
     - 楽観ロック用のバージョン番号。事前に取得したトークンの ``versionNo`` を指定します。

.. note::

   トークン文字列（ ``token`` ）は更新できません。リクエストボディに ``token`` を指定しても
   無視され、既存の値が維持されます。

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
        "status": 0
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
           "name": "Search API Token",
           "permissions": "{role}guest"
         }'

トークンを使用したAPI呼び出し
-----------------------------

作成したトークンは、検索APIなどを呼び出す際の認証に使用します。

.. code-block:: bash

    # トークンをAuthorizationヘッダーとして使用
    curl "http://localhost:8080/api/v2/search?q=test" \
         -H "Authorization: Bearer your_token_here"

    # トークンをクエリパラメーターとして使用（ api.access.token.request.parameter の設定が必要）
    curl "http://localhost:8080/api/v2/search?q=test&token=your_token_here"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要（認証・レスポンス形式・エラー）
- :doc:`../api-search` - 検索API
- :doc:`../../admin/accesstoken-guide` - アクセストークン管理ガイド
