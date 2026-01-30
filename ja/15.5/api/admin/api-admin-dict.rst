==========================
Dict API
==========================

概要
====

Dict APIは、|Fess| の辞書ファイルを管理するためのAPIです。
同義語辞書、マッピング辞書、保護語辞書などの管理を行えます。

ベースURL
=========

::

    /api/admin/dict

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /
     - 辞書一覧取得
   * - GET
     - /{id}
     - 辞書内容取得
   * - PUT
     - /{id}
     - 辞書内容更新
   * - POST
     - /upload
     - 辞書ファイルアップロード

辞書一覧取得
============

リクエスト
----------

::

    GET /api/admin/dict

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dicts": [
          {
            "id": "synonym",
            "name": "同義語辞書",
            "path": "/var/lib/fess/dict/synonym.txt",
            "type": "synonym",
            "updatedAt": "2025-01-29T10:00:00Z"
          },
          {
            "id": "mapping",
            "name": "マッピング辞書",
            "path": "/var/lib/fess/dict/mapping.txt",
            "type": "mapping",
            "updatedAt": "2025-01-28T15:30:00Z"
          },
          {
            "id": "protwords",
            "name": "保護語辞書",
            "path": "/var/lib/fess/dict/protwords.txt",
            "type": "protwords",
            "updatedAt": "2025-01-27T12:00:00Z"
          }
        ],
        "total": 3
      }
    }

辞書内容取得
============

リクエスト
----------

::

    GET /api/admin/dict/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dict": {
          "id": "synonym",
          "name": "同義語辞書",
          "path": "/var/lib/fess/dict/synonym.txt",
          "type": "synonym",
          "content": "検索,サーチ,リサーチ\nFess,フェス\n全文検索,フルテキストサーチ",
          "updatedAt": "2025-01-29T10:00:00Z"
        }
      }
    }

辞書内容更新
============

リクエスト
----------

::

    PUT /api/admin/dict/{id}
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "content": "検索,サーチ,リサーチ,search\nFess,フェス\n全文検索,フルテキストサーチ,full-text search"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``content``
     - はい
     - 辞書内容（改行区切り）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary updated successfully"
      }
    }

辞書ファイルアップロード
========================

リクエスト
----------

::

    POST /api/admin/dict/upload
    Content-Type: multipart/form-data

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="type"

    synonym
    --boundary
    Content-Disposition: form-data; name="file"; filename="synonym.txt"
    Content-Type: text/plain

    検索,サーチ,リサーチ
    Fess,フェス
    --boundary--

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``type``
     - はい
     - 辞書タイプ（synonym/mapping/protwords/stopwords）
   * - ``file``
     - はい
     - 辞書ファイル

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary uploaded successfully"
      }
    }

辞書タイプ
==========

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - タイプ
     - 説明
   * - ``synonym``
     - 同義語辞書（検索時に同義語を展開）
   * - ``mapping``
     - マッピング辞書（文字の正規化）
   * - ``protwords``
     - 保護語辞書（ステミング対象外の単語）
   * - ``stopwords``
     - ストップワード辞書（インデックス対象外の単語）
   * - ``kuromoji``
     - Kuromoji辞書（日本語形態素解析）

辞書形式の例
============

同義語辞書
----------

::

    # カンマ区切りで同義語を指定
    検索,サーチ,リサーチ,search
    Fess,フェス,fess
    全文検索,フルテキストサーチ,full-text search

マッピング辞書
--------------

::

    # 変換前 => 変換後
    ０ => 0
    １ => 1
    ２ => 2

保護語辞書
----------

::

    # ステミング処理から保護する単語
    running
    searching
    indexing

使用例
======

辞書一覧の取得
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

同義語辞書の内容取得
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN"

同義語辞書の更新
----------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "content": "検索,サーチ,search\nFess,フェス,fess\nドキュメント,文書,document"
         }'

辞書ファイルのアップロード
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "type=synonym" \
         -F "file=@synonym.txt"

注意事項
========

- 辞書を更新した後は、インデックスの再構築が必要な場合があります
- 大規模な辞書ファイルは検索パフォーマンスに影響を与える可能性があります
- 辞書の文字エンコーディングはUTF-8を使用してください

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`../../admin/dict-guide` - 辞書管理ガイド
- :doc:`../../config/dict-config` - 辞書設定ガイド
