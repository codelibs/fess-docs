==========================
RelatedQuery API
==========================

概要
====

RelatedQuery APIは、|Fess| の関連クエリを管理するためのAPIです。
ユーザーが入力する検索キーワード（``term``）に対して、関連する検索キーワードの候補
（``queries``）を登録・管理できます。登録した関連クエリは、検索画面で関連する検索候補として
表示されます。

認証方法、共通のレスポンス形式（``version`` フィールドや ``status`` コード）、
ページネーション、エラーレスポンスの詳細は :doc:`api-admin-overview` を参照してください。

ベースURL
=========

::

    /api/admin/relatedquery

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
     - 関連クエリ一覧取得
   * - GET
     - /setting/{id}
     - 関連クエリ取得
   * - POST
     - /setting
     - 関連クエリ作成
   * - PUT
     - /setting
     - 関連クエリ更新
   * - DELETE
     - /setting/{id}
     - 関連クエリ削除

関連クエリ一覧取得
==================

リクエスト
----------

::

    GET /api/admin/relatedquery/settings

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
     - ページ番号（1から開始。デフォルト: 1）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "query_id_1",
            "term": "fess",
            "queries": "fess tutorial\nfess installation\nfess configuration",
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   各設定には ``versionNo``（楽観的ロック用のバージョン番号）が含まれます。``virtualHost``
   や監査用フィールド（``createdBy``、``createdTime``、``updatedBy``、``updatedTime``）は、
   値が設定されている場合に限り含まれます。値が空の ``virtualHost`` はレスポンスに含まれません。

関連クエリ取得
==============

リクエスト
----------

::

    GET /api/admin/relatedquery/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": "fess tutorial\nfess installation\nfess configuration",
          "virtualHost": "site1.example.com",
          "versionNo": 1
        }
      }
    }

関連クエリ作成
==============

リクエスト
----------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search",
      "virtualHost": ""
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - フィールド
     - 必須
     - 説明
   * - ``term``
     - はい
     - 検索キーワード（最大10000文字）
   * - ``queries``
     - はい
     - 関連クエリ。1行に1件を記述した改行区切りの文字列です（空行は無視されます。最大10000文字）
   * - ``virtualHost``
     - いいえ
     - 仮想ホスト（最大1000文字）

.. note::

   ``crudMode`` はAPI側で自動的に設定されるため、リクエストボディに含める必要はありません。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

関連クエリ更新
==============

リクエスト
----------

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search\nsearch tips",
      "virtualHost": "",
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
     - 更新対象の関連クエリID（最大1000文字）
   * - ``term``
     - はい
     - 検索キーワード（最大10000文字）
   * - ``queries``
     - はい
     - 関連クエリ。1行に1件を記述した改行区切りの文字列です（空行は無視されます。最大10000文字）
   * - ``virtualHost``
     - いいえ
     - 仮想ホスト（最大1000文字）
   * - ``versionNo``
     - はい
     - 楽観的ロック用のバージョン番号。取得時のレスポンスに含まれる値を指定します

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

関連クエリ削除
==============

リクエスト
----------

::

    DELETE /api/admin/relatedquery/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

エラーレスポンス
================

リクエストが失敗した場合、``status`` に 0 以外の値が設定され、``message`` にエラー内容が
含まれます。たとえば、必須フィールドの不足などの検証エラーでは ``status`` が ``1`` になります。
ステータスコードの一覧は :doc:`api-admin-overview` を参照してください。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "..."
      }
    }

使用例
======

製品関連のクエリ
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": "product features\nproduct pricing\nproduct comparison\nproduct reviews"
         }'

ヘルプ関連のクエリ
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": "help center\nhelp documentation\nhelp contact support"
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-relatedcontent` - 関連コンテンツAPI
- :doc:`api-admin-suggest` - サジェスト管理API
- :doc:`../../admin/relatedquery-guide` - 関連クエリ管理ガイド
