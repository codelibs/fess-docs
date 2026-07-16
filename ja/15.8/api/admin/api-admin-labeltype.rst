==========================
LabelType API
==========================

概要
====

LabelType APIは、|Fess| のラベルタイプを管理するためのAPIです。
ラベルタイプを使用すると、クロール対象のパスや仮想ホストに基づいて検索結果を分類し、
検索画面でのラベルによる絞り込み（フィルタリング）に利用できます。

認証方法やレスポンスの共通仕様（``status`` コード、``version`` フィールド、エラー形式、
HTTPステータスコードなど）については :doc:`api-admin-overview` を参照してください。
本APIにアクセスするには、管理API権限（``admin-api``）を持つアクセストークンを
``Authorization: Bearer <アクセストークン>`` ヘッダーで指定する必要があります。

ベースURL
=========

::

    /api/admin/labeltype

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
     - ラベルタイプ一覧取得
   * - GET
     - /setting/{id}
     - ラベルタイプ取得
   * - POST
     - /setting
     - ラベルタイプ作成
   * - PUT
     - /setting
     - ラベルタイプ更新
   * - DELETE
     - /setting/{id}
     - ラベルタイプ削除

ラベルタイプ一覧取得
====================

リクエスト
----------

::

    GET /api/admin/labeltype/settings

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
     - 1ページあたりの件数。デフォルトは ``paging.page.size`` の設定値（標準では ``25``）です。
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始）。デフォルトは ``1`` です。
   * - ``name``
     - String
     - いいえ
     - 表示名による絞り込み（ワイルドカード検索）。
   * - ``value``
     - String
     - いいえ
     - ラベル値による絞り込み（ワイルドカード検索）。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "permissions": "{role}admin",
            "virtualHost": "",
            "sortOrder": 0,
            "createdBy": "admin",
            "createdTime": 1700000000000,
            "updatedBy": "admin",
            "updatedTime": 1700000000000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   各設定オブジェクトには、監査用の ``createdBy`` / ``createdTime`` / ``updatedBy`` /
   ``updatedTime`` と、楽観的ロック用の ``versionNo`` も含まれます（値が ``null`` の
   フィールドは省略されます）。\ ``response`` オブジェクトには製品バージョンを示す
   ``version`` が常に含まれますが、以降の例では簡潔さのために省略している場合があります。

ラベルタイプ取得
================

リクエスト
----------

::

    GET /api/admin/labeltype/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "permissions": "{role}admin",
          "virtualHost": "",
          "sortOrder": 0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

ラベルタイプ作成
================

リクエスト
----------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - フィールド
     - 型
     - 必須
     - 説明
   * - ``name``
     - String
     - はい
     - ラベル表示名（最大100文字）。
   * - ``value``
     - String
     - はい
     - ラベル値（検索時に ``label`` パラメーターで使用）。半角英数字とアンダースコア（``_``）のみ使用可能で、正規表現 ``^[a-zA-Z0-9_]+$`` に一致する必要があります（最大100文字）。
   * - ``includedPaths``
     - String
     - いいえ
     - ラベル対象とするパスの正規表現。複数指定する場合は改行（``\n``）で区切ります。
   * - ``excludedPaths``
     - String
     - いいえ
     - ラベル対象から除外するパスの正規表現。複数指定する場合は改行（``\n``）で区切ります。
   * - ``permissions``
     - String
     - いいえ
     - アクセスを許可するロール／グループ／ユーザー（例: ``{role}admin``）。複数指定する場合は改行（``\n``）で区切ります。
   * - ``sortOrder``
     - Integer
     - いいえ
     - 表示順序（0以上の整数）。指定しない場合は ``0`` です。
   * - ``virtualHost``
     - String
     - いいえ
     - 仮想ホスト（最大1000文字）。

.. note::

   ``createdBy`` / ``createdTime`` などの監査フィールドはサーバー側で自動的に設定される
   ため、リクエストでの指定は不要です。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

作成に成功すると ``created`` は ``true`` になります。

ラベルタイプ更新
================

リクエスト
----------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest",
      "versionNo": 1
    }

更新時は、作成時のフィールドに加えて以下のフィールドが必須です。

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - フィールド
     - 型
     - 必須
     - 説明
   * - ``id``
     - String
     - はい
     - 更新対象のラベルタイプID。
   * - ``versionNo``
     - Integer
     - はい
     - 楽観的ロック用のバージョン番号。取得時のレスポンスに含まれる ``versionNo`` を指定します。指定したバージョンが現在のものと一致しない場合、更新は失敗します。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

更新の場合、``created`` は ``false`` になります。

ラベルタイプ削除
================

リクエスト
----------

::

    DELETE /api/admin/labeltype/setting/{id}

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

ドキュメント用ラベル作成
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

ラベルタイプ一覧取得
--------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/labeltype/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

ラベルを使用した検索
--------------------

.. code-block:: bash

    # ラベルでフィルタリング
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`../api-search` - 検索API
- :doc:`../../admin/labeltype-guide` - ラベルタイプ管理ガイド
