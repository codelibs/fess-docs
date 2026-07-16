==========================
Documents API
==========================

概要
====

Documents APIは、|Fess| のインデックスにドキュメントを一括登録するためのAdmin APIです。
クローラーを介さずに、外部システムが生成したドキュメントを直接インデックスへ追加できます。
1回のリクエストで複数のドキュメントをまとめて登録できます。

ベースURL
=========

::

    /api/admin/documents

認証
====

このAPIを呼び出すには、:doc:`api-admin-overview` で説明しているアクセストークンによる認証が必要です。
トークンにはAdmin APIへのアクセス権限（既定では ``Radmin-api`` ）が付与されている必要があります。
この権限は設定キー ``api.admin.access.permissions`` で変更できます。

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - PUT
     - /bulk
     - ドキュメント一括登録

.. note::

   このエンドポイントは ``PUT`` メソッドのみを受け付けます。

ドキュメント一括登録
====================

複数のドキュメントをインデックスに一括で登録します。

リクエスト
----------

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "サンプルページ1",
          "content": "ページ1の本文テキストです。"
        },
        {
          "url": "https://example.com/page2",
          "title": "サンプルページ2",
          "content": "ページ2の本文テキストです。"
        }
      ]
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``documents``
     - はい
     - 登録するドキュメントの配列。各ドキュメントはフィールド名と値のマップで指定します。\ ``null`` または空配列の場合はエラー（``status`` = ``1``）になります。

ドキュメントのフィールド
~~~~~~~~~~~~~~~~~~~~~~~~~

各ドキュメントには、インデックスのフィールドを名前と値のマップとして自由に指定できます。
最低限、 ``url`` と ``title`` は指定する必要があります（必須フィールドの設定
``index.admin.required.fields`` に従います。既定値は ``url,title,role,boost`` で、
``role`` と ``boost`` は後述のとおり自動補完されるため、実質的に ``url`` と ``title`` が必須です）。

以下のフィールドは省略した場合、自動的に補完されます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 省略時の既定値
   * - ``content_length``
     - ``title`` と ``content`` の文字数の合計
   * - ``favorite_count``
     - ``0``
   * - ``click_count``
     - ``0``
   * - ``boost``
     - ``1.0``
   * - ``role``
     - 検索ゲストロール（ゲストユーザー用に設定された検索ロール）
   * - ``last_modified``
     - 現在時刻
   * - ``timestamp``
     - 現在時刻

また、以下のフィールドは登録時に自動生成されます。

- ``id`` - ドキュメントの ``url`` （および ``role`` 、 ``virtual_host`` ）から決定的に生成され、
  OpenSearch上のドキュメントID（``_id``）として使用されます。レスポンスの ``items[].id``
  にはこの値が返されます。
- ``doc_id`` - ランダムなUUIDが登録ごとに生成され、ドキュメントのフィールドとして格納されます。

.. note::

   ``id`` は ``url`` から決定的に生成されるため、同じ ``url`` のドキュメントを再度登録すると、
   既存のドキュメントが更新されます（``items[].result`` が ``OK`` になります）。

補足
~~~~

- ``lang`` フィールドに ``"auto"`` を含めると、本文から言語が自動判定されます。
- ``config_id`` を指定すると、該当するクロール設定の取り込みパイプライン（ingest pipeline）が
  適用されます。
- サムネイル生成が有効な場合（``thumbnail.crawler.enabled``）、登録時にサムネイル生成が試行されます。
- 各フィールドの値は、フィールドの型設定（``index.admin.array.fields`` 、
  ``index.admin.date.fields`` 、 ``index.admin.long.fields`` 等）に従って検証されます。
  型が一致しない場合はエラー（``status`` = ``1``）になります。

レスポンス
----------

レスポンスは登録した各ドキュメントの処理結果を ``items`` 配列で返します。
成功した項目は ``result`` と ``id`` を、失敗した項目は ``result`` と ``message`` を含みます。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "CREATED",
            "id": "0123456789abcdef"
          }
        ]
      }
    }

``status`` が ``0`` の場合は、すべてのドキュメントの登録に成功したことを示します。
``items[].result`` には、新規作成時は ``CREATED`` 、既存ドキュメントの更新時は ``OK`` が設定されます。

いずれかの項目で登録が失敗した場合、 ``status`` は ``9`` （FAILED）となり、
失敗した項目には ``message`` フィールドが含まれます（``result`` には ``CONFLICT`` や
``BAD_REQUEST`` などのエラーステータス名が設定されます）。成功した項目はそのまま ``id`` を返します。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 9,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "BAD_REQUEST",
            "message": "failure reason ..."
          }
        ]
      }
    }

.. note::

   リクエスト自体が不正な場合（``documents`` が未指定・空、必須フィールドの欠落、
   フィールドの型不一致など）は、ドキュメントの登録処理は実行されず、
   ``status`` = ``1`` （BAD_REQUEST）と ``message`` を含むエラーレスポンスが返されます。
   この場合、``items`` 配列は返されません。

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``items``
     - 各ドキュメントの処理結果の配列
   * - ``items[].result``
     - 処理結果ステータス名。新規作成時は ``CREATED`` 、更新時は ``OK`` 、失敗時は ``BAD_REQUEST`` 等のエラーステータス名
   * - ``items[].id``
     - 登録されたドキュメントのID（成功時のみ）
   * - ``items[].message``
     - 失敗理由のメッセージ（失敗時のみ）

使用例
======

ドキュメントの一括登録
----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "サンプルページ1",
               "content": "ページ1の本文テキストです。"
             }
           ]
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-searchlist` - ドキュメント検索・管理API
- :doc:`api-admin-crawlinginfo` - クロール情報API
- :doc:`../../admin/searchlist-guide` - 検索一覧管理ガイド
