==========================
Storage API
==========================

概要
====

Storage APIは、|Fess| のオブジェクトストレージを管理するためのAPIです。
ストレージ内のファイル・ディレクトリの一覧取得、ファイルのダウンロード・削除・アップロードを操作できます。

ベースURL
=========

::

    /api/admin/storage

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /list/{id}
     - ファイル・ディレクトリ一覧取得
   * - GET
     - /download/{id}
     - ファイルのダウンロード
   * - DELETE
     - /delete/{id}
     - ファイルの削除
   * - PUT
     - /upload/{pathId}
     - ファイルのアップロード

ファイル・ディレクトリ一覧取得
==============================

指定したディレクトリ配下のファイルおよびディレクトリの一覧を返します。
``{id}`` にはエンコードされたパスを指定します。``{id}`` を省略するとルートディレクトリの一覧を取得します。

リクエスト
----------

::

    GET /api/admin/storage/list/{id}

レスポンス
----------

``items`` にファイル・ディレクトリの情報を表すオブジェクトの配列が格納されます（ディレクトリが先、ファイルが後の順）。
各オブジェクトは以下のフィールドを持ちます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``id``
     - エンコードされた識別子（ダウンロード・削除時の ``{id}`` に使用）
   * - ``path``
     - 親パス
   * - ``name``
     - ファイル名またはディレクトリ名
   * - ``hashCode``
     - ハッシュコード
   * - ``size``
     - サイズ（バイト）
   * - ``directory``
     - ディレクトリかどうか（boolean）
   * - ``lastModified``
     - 最終更新日時（ファイルのみ）

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "id": "c3ViZGly",
            "path": "/",
            "name": "subdir",
            "hashCode": 12345,
            "size": 0,
            "directory": true
          },
          {
            "id": "c2FtcGxlLnR4dA==",
            "path": "/",
            "name": "sample.txt",
            "hashCode": 67890,
            "size": 1024,
            "directory": false,
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ]
      }
    }

ファイルのダウンロード
======================

ストレージ内のファイルをダウンロードします。``{id}`` には一覧取得で得られた ``id`` を指定します。
レスポンスは ``application/octet-stream`` のストリームとして返されます。

リクエスト
----------

::

    GET /api/admin/storage/download/{id}

レスポンス
----------

ファイルのバイナリストリーム（``Content-Type: application/octet-stream``）。

ファイルの削除
==============

ストレージ内のファイルを削除します。``{id}`` には一覧取得で得られた ``id`` を指定します。

リクエスト
----------

::

    DELETE /api/admin/storage/delete/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

ファイルのアップロード
======================

ストレージにファイルをアップロードします。``multipart/form-data`` 形式で送信します。

リクエスト
----------

::

    PUT /api/admin/storage/upload/{pathId}
    Content-Type: multipart/form-data

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - フィールド
     - 必須
     - 説明
   * - ``path``
     - いいえ
     - アップロード先のパス（未指定の場合は既定の場所）
   * - ``file``
     - はい
     - アップロードするファイル

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

使用例
======

ルートディレクトリの一覧取得
----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

ファイルのダウンロード
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

ファイルの削除
--------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

ファイルのアップロード
----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload/" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=/" \
         -F "file=@sample.txt"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
