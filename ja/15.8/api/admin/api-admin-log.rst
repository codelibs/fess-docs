==========================
Log API
==========================

概要
====

Log APIは、|Fess| のログファイルを参照・ダウンロードするためのAPIです。
サーバー上に出力されたログファイルの一覧取得と、個別のログファイルのダウンロードを行えます。

ベースURL
=========

::

    /api/admin/log

認証
====

他のAdmin APIと同様に、アクセストークンによる認証が必要です。アクセストークンには ``Radmin-api`` 権限（``api.admin.access.permissions`` で設定。既定値は ``Radmin-api``）が必要です。
リクエストヘッダーにアクセストークンを指定します。

::

    Authorization: Bearer <アクセストークン>

認証やアクセストークンの取得方法の詳細は :doc:`api-admin-overview` を参照してください。

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /files
     - ログファイル一覧取得
   * - GET
     - /file/{id}
     - ログファイルのダウンロード

ログファイル一覧取得
====================

サーバーのログ出力ディレクトリに存在するログファイル（``.log`` および ``.log.gz``）の一覧を返します。
ファイルはファイル名の昇順でソートされて返されます。

リクエスト
----------

::

    GET /api/admin/log/files

レスポンス
----------

``files`` に各ログファイルの情報を表すオブジェクトの配列、``total`` に件数が格納されます。
各オブジェクトは以下のフィールドを持ちます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``id``
     - ファイル名を Base64 URL エンコードした値（ダウンロード時の ``{id}`` に使用）
   * - ``name``
     - ログファイル名
   * - ``lastModified``
     - 最終更新日時

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "files": [
          {
            "id": "ZmVzcy5sb2c=",
            "name": "fess.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          },
          {
            "id": "ZmVzcy1jcmF3bGVyLmxvZw==",
            "name": "fess-crawler.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ],
        "total": 2
      }
    }

.. note::

   ``version`` には実行中の |Fess| の製品バージョンが設定されます。\ ``files`` の内容と件数は
   サーバー上のログファイルによって変わるため、上記は一例です。

ログファイルのダウンロード
==========================

指定したログファイルの内容をダウンロードします。
``{id}`` には一覧取得で返された ``id`` （ファイル名を Base64 URL エンコードした値）をそのまま指定します。
レスポンスは ``application/octet-stream`` のストリームとして返されます。
セキュリティのため、``.log`` または ``.log.gz`` で終わる名前のみが対象となり、``..`` などのパス操作を含む名前は受け付けません。
存在しないファイル名やログファイルとして許可されない名前を指定した場合は、空のレスポンスが返されます。

リクエスト
----------

::

    GET /api/admin/log/file/{id}

レスポンス
----------

ログファイルのバイナリストリーム（``Content-Type: application/octet-stream``）。

使用例
======

ログファイル一覧取得
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

ログファイルのダウンロード
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/file/ZmVzcy5sb2c=" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess.log

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-backup` - バックアップAPI
