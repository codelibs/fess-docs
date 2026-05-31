==================
認証・セッションAPI
==================

概要
====

v2 API はセッションベースの認証を採用しています。
ログインは ``POST /auth/login`` で行い、成功するとセッションが確立され、CSRF トークンが発行されます。

状態を変更するリクエスト（ ``POST`` ）には、 ``X-Fess-CSRF-Token`` ヘッダーが必要です。
CSRF トークンの取得方法やローテーションの仕組み、共通のレスポンスエンベロープおよびエラーモデルについては :doc:`api-overview` を参照してください。

このページでは以下の4つのエンドポイントを説明します。

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: エンドポイント一覧
   :header-rows: 1
   :widths: 25 15 60

   * - エンドポイント
     - メソッド
     - 説明
   * - ``/auth/me``
     - GET
     - 現在の認証済みユーザーを取得します。
   * - ``/auth/login``
     - POST
     - ユーザー名とパスワードでログインします。
   * - ``/auth/logout``
     - POST
     - ログアウトします（冪等）。
   * - ``/auth/password``
     - POST
     - 現在のユーザーのパスワードを変更します。

.. _api-auth-userpayload:

共通のユーザー情報 (UserPayload)
==============================

``GET /auth/me`` および ``POST /auth/login`` のレスポンスに含まれるユーザー情報は、共通の ``UserPayload`` 構造で返されます。
すべての配列フィールドは非 null であり、値がない場合は空配列が返されます。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: UserPayload
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 型
     - 説明
   * - ``user_id``
     - string
     - ユーザーID。（必須）
   * - ``username``
     - string
     - SPA のアカウントメニュー用の表示ユーザー名。現状は ``user_id`` と同じ値ですが、将来バックエンドが独立して提供する可能性があります。（必須）
   * - ``name``
     - string
     - SPA のアカウントメニュー用の表示名。現状は ``user_id`` と同じ値です。（必須）
   * - ``roles``
     - string[]
     - ユーザーのロールの配列。（必須）
   * - ``groups``
     - string[]
     - ユーザーのグループの配列。（必須）
   * - ``permissions``
     - string[]
     - ユーザーのパーミッションの配列。（必須）
   * - ``editable``
     - boolean
     - ユーザー情報が編集可能かどうか。（必須）
   * - ``admin``
     - boolean
     - ユーザーが、設定済みの ``authentication.admin.roles`` のいずれかを持つとき ``true`` になります。SPA の「Administration」項目の表示を制御します。（必須）

認証状態の取得
============

リクエスト
--------

==================  ====================================================
HTTPメソッド         GET
エンドポイント        ``/api/v2/auth/me``
==================  ====================================================

現在の認証済みユーザーを取得します。
匿名の呼び出しに対してはエラーにはならず、 ``authenticated: false`` を返します。
認証済みのときは ``user`` が :ref:`UserPayload <api-auth-userpayload>` を持ちます。

レスポンス
--------

成功時（HTTP 200）には、以下のような共通エンベロープ形式のレスポンスが返ります（認証済みの例）。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "authenticated": true,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        }
      }
    }

``response`` の各要素については以下の通りです。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: レスポンス情報
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 型
     - 説明
   * - ``authenticated``
     - boolean
     - 認証済みかどうか。（必須）
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>` 。 ``authenticated`` が ``true`` のときのみ存在します。

エラーレスポンス
------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: エラーレスポンス
   :header-rows: 1
   :widths: 25 75

   * - ステータスコード
     - 説明
   * - 405 Method Not Allowed
     - サポートされていない HTTP メソッドが指定された場合。
   * - 500 Internal Server Error
     - サーバー内部エラーが発生した場合。

ログイン
======

リクエスト
--------

==================  ====================================================
HTTPメソッド         POST
エンドポイント        ``/api/v2/auth/login``
==================  ====================================================

ユーザー名とパスワードでログインします。
ログイン成功時には、サーブレットのセッションIDがローテーションされ、新しい CSRF トークンが発行され、呼び出し元 IP と対象ユーザーのレート制限バケットがクリアされます。
レート制限を超えた場合は、 ``Retry-After`` ヘッダー（秒）が付与されます。

既に認証済みのセッションでもショートサーキットせず、渡された資格情報は常に検証されます。

``return_to`` は ``^/[A-Za-z0-9_\-/.?&=%:@+~#*!,;]*$`` に一致する相対パスでなければなりません。
さらに、プロトコル相対（先頭 ``//`` ）のパスや ASCII 制御文字を含むパスは拒否され、エコーされるレスポンスから無言で除去されます。

.. note::

   このエンドポイントは **CSRF の対象外** です（ログイン前にトークンが存在しないため）。

.. note::

   他の状態変更エンドポイントと異なり、このエンドポイントは過大なリクエストボディや非対応の ``Content-Type`` を ``400 invalid_request`` にまとめます（他のエンドポイントは ``413`` / ``415`` を返します）。

リクエストボディ (LoginRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Content-Type は ``application/json`` です。

.. tabularcolumns:: |p{3cm}|p{2cm}|p{2cm}|p{7cm}|
.. list-table:: LoginRequest
   :header-rows: 1
   :widths: 20 12 12 56

   * - フィールド
     - 型
     - 必須
     - 説明
   * - ``username``
     - string
     - はい
     - ユーザー名。 ``minLength`` は1です。
   * - ``password``
     - string
     - はい
     - パスワード。 ``minLength`` は1です。
   * - ``return_to``
     - string
     - いいえ
     - ログイン後のリダイレクト先。上記パターンに一致する相対パスである必要があります。

リクエスト例:

.. code-block:: json

    {
      "username": "taro",
      "password": "secret",
      "return_to": "/search"
    }

レスポンス
--------

成功時（HTTP 200, LoginResponse）には、以下のような共通エンベロープ形式のレスポンスが返ります。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        },
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f",
        "return_to": "/search"
      }
    }

``response`` の各要素については以下の通りです。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: レスポンス情報
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 型
     - 説明
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>` 。
   * - ``csrf_token``
     - string
     - 新しいセッションに紐づく新規 CSRF トークン。（必須）
   * - ``return_to``
     - string
     - リクエスト値が許可リストを通過した場合のみエコーされます。

エラーレスポンス
------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: エラーレスポンス
   :header-rows: 1
   :widths: 25 75

   * - ステータスコード
     - 説明
   * - 400 Bad Request
     - リクエストが不正な場合（過大なリクエストボディや非対応の ``Content-Type`` を含む）。
   * - 401 Unauthorized
     - 認証情報が不正な場合。
   * - 405 Method Not Allowed
     - サポートされていない HTTP メソッドが指定された場合。
   * - 429 Too Many Requests
     - レート制限を超えた場合。 ``Retry-After`` ヘッダーに待機すべき秒数が示されます。
   * - 500 Internal Server Error
     - サーバー内部エラーが発生した場合。

ログアウト
========

リクエスト
--------

==================  ====================================================
HTTPメソッド         POST
エンドポイント        ``/api/v2/auth/logout``
==================  ====================================================

ログアウトします。この操作は冪等であり、アクティブなセッションがなくても no-op となりエラーにはなりません。常に ``ok: true`` を返します。

``X-Fess-CSRF-Token`` ヘッダーが必要です。

レスポンス
--------

成功時（HTTP 200, OkResponse）には、以下のような共通エンベロープ形式のレスポンスが返ります。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true
      }
    }

``response`` の各要素については以下の通りです。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: レスポンス情報
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 型
     - 説明
   * - ``ok``
     - boolean
     - 常に ``true`` です。（必須）

エラーレスポンス
------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: エラーレスポンス
   :header-rows: 1
   :widths: 25 75

   * - ステータスコード
     - 説明
   * - 403 Forbidden
     - CSRF トークンが欠落・失効している場合。
   * - 405 Method Not Allowed
     - POST 以外のメソッドが指定された場合。 ``Allow: POST`` ヘッダーが付与されます。

パスワード変更
============

リクエスト
--------

==================  ====================================================
HTTPメソッド         POST
エンドポイント        ``/api/v2/auth/password``
==================  ====================================================

現在のユーザーのパスワードを変更します。
``current_password`` を検証し、 ``new_password`` に設定済みのパスワードポリシーを適用し、現在のセッションを無効化し、 ``re_login_required: true`` で SPA にログインページへのリダイレクトを促します。

セッションがサーバー側で破棄されるため ``csrf_token`` は返りません。SPA は再認証後に新しいトークンを取得する必要があります。

``X-Fess-CSRF-Token`` ヘッダーが必要です。

リクエストボディ (PasswordChangeRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Content-Type は ``application/json`` です。

.. tabularcolumns:: |p{3.5cm}|p{2cm}|p{2cm}|p{6.5cm}|
.. list-table:: PasswordChangeRequest
   :header-rows: 1
   :widths: 22 12 12 54

   * - フィールド
     - 型
     - 必須
     - 説明
   * - ``current_password``
     - string
     - はい
     - 現在のパスワード。 ``minLength`` は1です。
   * - ``new_password``
     - string
     - はい
     - 新しいパスワード。設定済みのパスワードポリシーを満たす必要があります。 ``minLength`` は1です。
   * - ``confirm_password``
     - string
     - はい
     - 確認用のパスワード。 ``new_password`` と一致する必要があります。 ``minLength`` は1です。

レスポンス
--------

成功時（HTTP 200）には、以下のような共通エンベロープ形式のレスポンスが返ります。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true,
        "re_login_required": true
      }
    }

``response`` の各要素については以下の通りです。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: レスポンス情報
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 型
     - 説明
   * - ``ok``
     - boolean
     - 常に ``true`` です。（必須）
   * - ``re_login_required``
     - boolean
     - 常に ``true`` です。現在のセッションはサーバー側で無効化済みです。SPA はログインページへリダイレクトして、新しいセッションと CSRF トークンを取得しなければなりません。（必須）

エラーレスポンス
------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: エラーレスポンス
   :header-rows: 1
   :widths: 25 75

   * - ステータスコード
     - 説明
   * - 400 Bad Request
     - リクエストが不正な場合。
   * - 401 Unauthorized
     - 認証が必要、または ``current_password`` が不正な場合。
   * - 403 Forbidden
     - CSRF トークンが欠落・失効している場合。
   * - 405 Method Not Allowed
     - サポートされていない HTTP メソッドが指定された場合。
   * - 413 Payload Too Large
     - リクエストボディがサイズ上限を超えた場合。
   * - 415 Unsupported Media Type
     - サポートされていない ``Content-Type`` の場合。
   * - 429 Too Many Requests
     - レート制限を超えた場合。
   * - 500 Internal Server Error
     - サーバー内部エラーが発生した場合。
