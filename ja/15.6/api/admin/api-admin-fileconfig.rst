==========================
FileConfig API
==========================

概要
====

FileConfig APIは、|Fess| のファイルクロール設定を管理するためのAPIです。
ファイルシステムやSMB/CIFSの共有フォルダなどのクロール設定を操作できます。

ベースURL
=========

::

    /api/admin/fileconfig

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET/PUT
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
    PUT /api/admin/fileconfig/settings

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
     - 1ページあたりの件数（デフォルト: 20）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（0から開始）

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
            "paths": "file://///server/share/documents",
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
            "available": true,
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

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
          "paths": "file://///server/share/documents",
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
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
        }
      }
    }

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
      "depth": 5,
      "maxAccessCount": 5000,
      "numOfThread": 2,
      "intervalTime": 500,
      "boost": 1.0,
      "available": true,
      "permissions": ["admin", "user"],
      "labelTypeIds": ["label_id_1"]
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - 設定名
   * - ``paths``
     - はい
     - クロール開始パス（複数の場合は改行区切り）
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
     - 追加設定パラメーター
   * - ``depth``
     - いいえ
     - クロール深度（デフォルト: -1=無制限）
   * - ``maxAccessCount``
     - いいえ
     - 最大アクセス数（デフォルト: 100）
   * - ``numOfThread``
     - いいえ
     - 並列スレッド数（デフォルト: 1）
   * - ``intervalTime``
     - いいえ
     - アクセス間隔（ミリ秒、デフォルト: 0）
   * - ``boost``
     - いいえ
     - 検索結果のブースト値（デフォルト: 1.0）
   * - ``available``
     - いいえ
     - 有効/無効（デフォルト: true）
   * - ``sortOrder``
     - いいえ
     - 表示順序
   * - ``permissions``
     - いいえ
     - アクセス許可ロール
   * - ``virtualHosts``
     - いいえ
     - 仮想ホスト
   * - ``labelTypeIds``
     - いいえ
     - ラベルタイプID

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
      "available": true,
      "versionNo": 1
    }

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
        "status": 0,
        "id": "deleted_fileconfig_id",
        "created": false
      }
    }

パスの形式
==========

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - プロトコル
     - パス形式
   * - ローカルファイル
     - ``file:///path/to/directory``
   * - Windows共有 (SMB)
     - ``file://///server/share/path``
   * - SMB認証付き
     - ``smb://username:password@server/share/path``
   * - NFS
     - ``file://///nfs-server/export/path``

使用例
======

SMB共有のクロール設定
---------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://user:pass@server/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|private)/.*",
           "depth": -1,
           "maxAccessCount": 50000,
           "numOfThread": 3,
           "intervalTime": 200,
           "available": true,
           "permissions": ["guest"]
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-webconfig` - Webクロール設定API
- :doc:`api-admin-dataconfig` - データストア設定API
- :doc:`../../admin/fileconfig-guide` - ファイルクロール設定ガイド
