==========================
FileConfig API
==========================

概要
====

FileConfig APIは、|Fess| のファイルクロール設定を管理するためのAPIです。
ローカルファイルシステム、SMB/CIFS共有フォルダ、FTP、各種オブジェクトストレージなどのクロール設定を操作できます。

ベースURL
=========

::

    /api/admin/fileconfig

.. note::

   すべてのエンドポイントには管理者権限と有効なアクセストークンが必要です。
   認証方法については :doc:`api-admin-overview` を参照してください。

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
     - ファイルクロール設定一覧取得
   * - GET
     - /setting/{id}
     - ファイルクロール設定取得
   * - POST
     - /setting
     - ファイルクロール設定作成
   * - PUT
     - /setting
     - ファイルクロール設定更新
   * - DELETE
     - /setting/{id}
     - ファイルクロール設定削除

ファイルクロール設定一覧取得
============================

リクエスト
----------

::

    GET /api/admin/fileconfig/settings

.. note::

   一覧取得エンドポイントは ``GET`` に加えて ``PUT`` でもアクセスできます。

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始、デフォルト: 1）
   * - ``size``
     - Integer
     - いいえ
     - 1ページあたりの件数（デフォルト: 25。\ ``paging.page.size`` 設定に従います）
   * - ``name``
     - String
     - いいえ
     - 設定名による絞り込み
   * - ``paths``
     - String
     - いいえ
     - クロールパスによる絞り込み
   * - ``description``
     - String
     - いいえ
     - 説明による絞り込み

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "fileconfig_id_1",
            "name": "Shared Documents",
            "description": "共有ドキュメント",
            "paths": "smb://server/share/documents",
            "includedPaths": ".*\\.pdf$",
            "excludedPaths": ".*/(temp|cache)/.*",
            "includedDocPaths": "",
            "excludedDocPaths": "",
            "configParameter": "",
            "depth": 10,
            "maxAccessCount": 1000,
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

``total`` は条件に一致する設定の総件数を表します。

ファイルクロール設定取得
========================

リクエスト
----------

::

    GET /api/admin/fileconfig/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "fileconfig_id_1",
          "name": "Shared Documents",
          "description": "共有ドキュメント",
          "paths": "smb://server/share/documents",
          "includedPaths": ".*\\.pdf$",
          "excludedPaths": ".*/(temp|cache)/.*",
          "includedDocPaths": "",
          "excludedDocPaths": "",
          "configParameter": "",
          "depth": 10,
          "maxAccessCount": 1000,
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   レスポンスには、登録・更新時に自動設定される ``createdBy`` 、 ``createdTime`` 、
   ``updatedBy`` 、 ``updatedTime`` 、 ``versionNo`` が含まれます。
   ``versionNo`` は更新時に必要です（後述の「ファイルクロール設定更新」を参照）。

ファイルクロール設定作成
========================

リクエスト
----------

::

    POST /api/admin/fileconfig/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx)$",
      "excludedPaths": ".*/(temp|backup)/.*",
      "numOfThread": 2,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - 設定名（最大200文字）
   * - ``description``
     - いいえ
     - 設定の説明（最大1000文字）
   * - ``paths``
     - はい
     - クロール開始パス（複数の場合は改行区切り）。\ ``file:`` 、 ``smb:`` 、 ``smb1:`` 、 ``ftp:`` 、 ``storage:`` 、 ``s3:`` 、 ``gcs:`` のいずれかのプロトコルで指定します
   * - ``includedPaths``
     - いいえ
     - クロール対象パスの正規表現パターン
   * - ``excludedPaths``
     - いいえ
     - クロール除外パスの正規表現パターン
   * - ``includedDocPaths``
     - いいえ
     - インデックス対象パスの正規表現パターン
   * - ``excludedDocPaths``
     - いいえ
     - インデックス除外パスの正規表現パターン
   * - ``configParameter``
     - いいえ
     - 追加設定パラメーター（``key=value`` 形式、1行に1項目）
   * - ``depth``
     - いいえ
     - クロール深度（0以上）
   * - ``maxAccessCount``
     - いいえ
     - 最大アクセス数（0以上）
   * - ``numOfThread``
     - はい
     - 並列スレッド数（1以上）
   * - ``intervalTime``
     - はい
     - アクセス間隔（ミリ秒、0以上）
   * - ``boost``
     - はい
     - 検索結果のブースト値
   * - ``available``
     - はい
     - 有効/無効（文字列 ``"true"`` / ``"false"``）
   * - ``sortOrder``
     - はい
     - 表示順序（0以上）
   * - ``permissions``
     - いいえ
     - アクセス許可ロール（複数の場合は改行区切り）
   * - ``virtualHosts``
     - いいえ
     - 仮想ホスト（複数の場合は改行区切り）

.. note::

   ``createdBy`` 、 ``createdTime`` 、 ``updatedBy`` 、 ``updatedTime`` などの監査用フィールドは
   サーバー側で自動設定されるため、リクエストボディで指定する必要はありません。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_fileconfig_id",
        "created": true
      }
    }

ファイルクロール設定更新
========================

リクエスト
----------

::

    PUT /api/admin/fileconfig/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

更新時は、作成時のフィールドに加えて、更新対象を特定する ``id`` とバージョン番号 ``versionNo`` が必須です。
``versionNo`` には取得API（GET）のレスポンスに含まれる現在の値を指定します。

.. code-block:: json

    {
      "id": "existing_fileconfig_id",
      "name": "Updated Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
      "excludedPaths": ".*/(temp|backup|archive)/.*",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 3,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

更新時の追加フィールド
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - フィールド
     - 必須
     - 説明
   * - ``id``
     - はい
     - 更新対象の設定ID（最大1000文字）
   * - ``versionNo``
     - はい
     - 更新対象の現在のバージョン番号。取得API（GET）のレスポンスに含まれる ``versionNo`` を指定します

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_fileconfig_id",
        "created": false
      }
    }

ファイルクロール設定削除
========================

リクエスト
----------

::

    DELETE /api/admin/fileconfig/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

パスの形式
==========

``paths`` には以下のプロトコルを使用できます（対応プロトコルは ``crawler.file.protocols`` 設定で変更できます）。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - プロトコル
     - パス形式
   * - ローカルファイル
     - ``file:///path/to/directory``
   * - SMB/CIFS共有
     - ``smb://server/share/path``
   * - SMB/CIFS共有（SMB1）
     - ``smb1://server/share/path``
   * - FTP
     - ``ftp://server/path``
   * - S3互換オブジェクトストレージ（MinIO等）
     - ``storage://bucket/path``
   * - Amazon S3
     - ``s3://bucket/path``
   * - Google Cloud Storage
     - ``gcs://bucket/path``

.. note::

   SMB/CIFSやFTPの認証情報（ユーザー名・パスワード）は、パスに埋め込まず
   「ファイル認証」設定で構成します。詳細は :doc:`../../admin/fileauth-guide` を参照してください。

使用例
======

ローカルファイルのクロール設定
------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Local Files",
           "paths": "file:///data/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|backup)/.*",
           "numOfThread": 2,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

SMB共有のクロール設定
---------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://server/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|private)/.*",
           "maxAccessCount": 50000,
           "numOfThread": 3,
           "intervalTime": 200,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

.. note::

   SMB共有へのアクセスに認証が必要な場合は、事前に「ファイル認証」設定で
   対象ホストの認証情報を登録してください。

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-webconfig` - Webクロール設定API
- :doc:`api-admin-dataconfig` - データストア設定API
- :doc:`../../admin/fileconfig-guide` - ファイルクロール設定ガイド
- :doc:`../../admin/fileauth-guide` - ファイル認証設定ガイド
