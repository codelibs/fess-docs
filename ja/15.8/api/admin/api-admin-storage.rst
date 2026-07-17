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

認証
====

Storage APIを含む Admin API のすべてのエンドポイントには、アクセストークンによる認証が必要です。
リクエストの ``Authorization`` ヘッダーにアクセストークンを指定します。

::

    Authorization: Bearer <アクセストークン>

アクセストークンの取得方法や必要な権限（既定では ``admin-api`` ロール）の詳細は、
:doc:`api-admin-overview` を参照してください。

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
     - /upload
     - ファイルのアップロード

ファイル・ディレクトリ一覧取得
==============================

指定したディレクトリ配下のファイルおよびディレクトリの一覧を返します。
``{id}`` には一覧取得で得られたディレクトリの ``id`` を指定します。\ ``{id}`` を省略するとルートディレクトリの一覧を取得します。

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
     - エンコードされた識別子。オブジェクトのパスをURLセーフなBase64でエンコードした文字列で、ダウンロード・削除時の ``{id}`` に使用します。
   * - ``path``
     - 親ディレクトリのパス
   * - ``name``
     - ファイル名またはディレクトリ名
   * - ``hashCode``
     - 内部処理で使用されるハッシュ値（オブジェクトの内容を表す安定した値ではありません）
   * - ``size``
     - サイズ（バイト）
   * - ``directory``
     - ディレクトリかどうか（boolean）
   * - ``lastModified``
     - 最終更新日時（ISO 8601形式。ファイルの場合のみ含まれます）

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

ストレージ内のファイルをダウンロードします。\ ``{id}`` には一覧取得で得られた ``id`` を指定します。
レスポンスは ``application/octet-stream`` のストリームとして返されます。

リクエスト
----------

::

    GET /api/admin/storage/download/{id}

レスポンス
----------

ファイルのバイナリストリーム（``Content-Type: application/octet-stream``）。

.. note::

   このAPIのレスポンスには ``Content-Disposition`` ヘッダーは付与されません。
   保存するファイル名はクライアント側で指定してください（cURLの場合は ``-o`` オプション）。

ファイルの削除
==============

ストレージ内のファイルを削除します。\ ``{id}`` には一覧取得で得られた ``id`` を指定します。

リクエスト
----------

::

    DELETE /api/admin/storage/delete/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

ファイルのアップロード
======================

ストレージにファイルをアップロードします。\ ``multipart/form-data`` 形式で送信します。
アップロード先のディレクトリは、URLのパスではなくフォームフィールド ``path`` で指定します。

リクエスト
----------

::

    PUT /api/admin/storage/upload
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
     - アップロード先のディレクトリパス（先頭・末尾のスラッシュは不要）。未指定の場合はルート（バケット直下）に保存されます。
   * - ``file``
     - はい
     - アップロードするファイル

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

エラー
======

各エンドポイントは、処理に失敗した場合に ``status`` が 0 以外の値（検証エラーの場合は ``1``）のレスポンスを返します。
レスポンス本文の ``message`` にエラー内容が含まれます。ステータス値やHTTPステータスコードの詳細は :doc:`api-admin-overview` を参照してください。

主なエラーケースは以下のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - エラーが発生する主なケース
   * - ファイル・ディレクトリ一覧取得
     - 取得件数が上限を超えた場合
   * - ファイルのダウンロード
     - ``id`` が不正な場合、またはダウンロードに失敗した場合
   * - ファイルの削除
     - ``id`` が不正な場合、または削除に失敗した場合
   * - ファイルのアップロード
     - ``file`` が指定されていない場合、またはアップロードに失敗した場合

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

    curl -X PUT "http://localhost:8080/api/admin/storage/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=subdir" \
         -F "file=@sample.txt"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
