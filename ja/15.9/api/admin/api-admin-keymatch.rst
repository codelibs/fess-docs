==========================
KeyMatch API
==========================

概要
====

KeyMatch APIは、|Fess| のキーマッチ（検索キーワードと結果の紐付け）を管理するためのAPIです。
特定のキーワードに対して特定のドキュメントを上位表示させることができます。

ベースURL
=========

::

    /api/admin/keymatch

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
     - キーマッチ一覧取得
   * - GET
     - /setting/{id}
     - キーマッチ取得
   * - POST
     - /setting
     - キーマッチ作成
   * - PUT
     - /setting
     - キーマッチ更新
   * - DELETE
     - /setting/{id}
     - キーマッチ削除

キーマッチ一覧取得
==================

リクエスト
----------

::

    GET /api/admin/keymatch/settings

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
     - 1ページあたりの件数（デフォルト: 25。\ ``paging.page.size`` の設定値）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始、デフォルト: 1）
   * - ``term``
     - String
     - いいえ
     - 検索キーワードによる絞り込み（ワイルドカード一致）
   * - ``query``
     - String
     - いいえ
     - マッチ条件クエリによる絞り込み（ワイルドカード一致）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "max_size": 10,
            "boost": 10.0,
            "version_no": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   ``total`` には絞り込み条件に一致する総件数が設定されます（現在のページの件数ではありません）。
   各設定オブジェクトには上記のフィールドに加えて、値が設定されている場合に ``virtual_host`` 、
   ``created_by`` 、 ``created_time`` 、 ``updated_by`` 、 ``updated_time`` が含まれます。

キーマッチ取得
==============

リクエスト
----------

::

    GET /api/admin/keymatch/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "keymatch_id_1",
          "term": "download",
          "query": "title:download OR content:download",
          "max_size": 10,
          "boost": 10.0,
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   ``version_no`` は楽観ロック用のバージョン番号です。キーマッチを更新する際は、取得時に得られた
   ``version_no`` をリクエストボディに指定してください。指定したIDが存在しない場合はエラーが返されます。

キーマッチ作成
==============

リクエスト
----------

::

    POST /api/admin/keymatch/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing",
      "max_size": 5,
      "boost": 20.0
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - フィールド
     - 型
     - 必須
     - 説明
   * - ``term``
     - String
     - はい
     - 検索キーワード（最大100文字）
   * - ``query``
     - String
     - はい
     - マッチ条件クエリ（最大長は ``form.admin.max.input.size`` の設定値に従う）
   * - ``max_size``
     - Integer
     - はい
     - 最大表示件数（0以上の整数。管理画面での初期値は10）
   * - ``boost``
     - Float
     - はい
     - ブースト値（管理画面での初期値は100.0）
   * - ``virtual_host``
     - String
     - いいえ
     - 仮想ホスト名（最大1000文字。仮想ホストごとにキーマッチを切り替える場合に指定）

.. note::

   ``max_size`` と ``boost`` はAPI経由では必須です。初期値は管理画面のフォームに表示される値であり、
   APIでは適用されません。省略した場合はバリデーションエラーになります。
   なお、 ``created_by`` と ``created_time`` はリクエストで指定してもサーバー側で上書きされます。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_keymatch_id",
        "created": true
      }
    }

キーマッチ更新
==============

リクエスト
----------

::

    PUT /api/admin/keymatch/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_keymatch_id",
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing OR content:price",
      "max_size": 10,
      "boost": 15.0,
      "version_no": 1
    }

フィールド説明
~~~~~~~~~~~~~~

作成時のフィールド（ ``term`` 、 ``query`` 、 ``max_size`` 、 ``boost`` 、 ``virtual_host`` ）に加えて、
以下のフィールドを指定します。

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - フィールド
     - 型
     - 必須
     - 説明
   * - ``id``
     - String
     - はい
     - 更新対象のキーマッチID（最大1000文字）
   * - ``version_no``
     - Integer
     - はい
     - 楽観ロック用のバージョン番号。取得時に得られた値を指定

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_keymatch_id",
        "created": false
      }
    }

キーマッチ削除
==============

リクエスト
----------

::

    DELETE /api/admin/keymatch/setting/{id}

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

製品ページのキーマッチ作成
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "max_size": 10,
           "boost": 15.0
         }'

サポートページのキーマッチ
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "query": "url:*/support/* OR url:*/help/* OR url:*/faq/*",
           "max_size": 5,
           "boost": 20.0
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-elevateword` - エレベートワードAPI
- :doc:`../../admin/keymatch-guide` - キーマッチ管理ガイド
