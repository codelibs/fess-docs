==========================
Backup API
==========================

概要
====

Backup APIは、|Fess| の設定データをバックアップ・リストアするためのAPIです。
クロール設定、ユーザー、ロール、辞書などの設定をエクスポート・インポートできます。

ベースURL
=========

::

    /api/admin/backup

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /export
     - 設定データエクスポート
   * - POST
     - /import
     - 設定データインポート

設定データエクスポート
======================

リクエスト
----------

::

    GET /api/admin/backup/export

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``types``
     - String
     - いいえ
     - エクスポート対象（カンマ区切り、デフォルト: all）

エクスポート対象タイプ
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - タイプ
     - 説明
   * - ``webconfig``
     - Webクロール設定
   * - ``fileconfig``
     - ファイルクロール設定
   * - ``dataconfig``
     - データストア設定
   * - ``scheduler``
     - スケジュール設定
   * - ``user``
     - ユーザー設定
   * - ``role``
     - ロール設定
   * - ``group``
     - グループ設定
   * - ``labeltype``
     - ラベルタイプ設定
   * - ``keymatch``
     - キーマッチ設定
   * - ``dict``
     - 辞書データ
   * - ``all``
     - 全ての設定（デフォルト）

レスポンス
----------

バイナリデータ（ZIP形式）

Content-Type: ``application/zip``
Content-Disposition: ``attachment; filename="fess-backup-20250129-100000.zip"``

ZIPファイル内容
~~~~~~~~~~~~~~~

::

    fess-backup-20250129-100000.zip
    ├── webconfig.json
    ├── fileconfig.json
    ├── dataconfig.json
    ├── scheduler.json
    ├── user.json
    ├── role.json
    ├── group.json
    ├── labeltype.json
    ├── keymatch.json
    ├── dict/
    │   ├── synonym.txt
    │   ├── mapping.txt
    │   └── protwords.txt
    └── metadata.json

設定データインポート
====================

リクエスト
----------

::

    POST /api/admin/backup/import
    Content-Type: multipart/form-data

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="file"; filename="fess-backup.zip"
    Content-Type: application/zip

    [バイナリデータ]
    --boundary
    Content-Disposition: form-data; name="overwrite"

    true
    --boundary--

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``file``
     - はい
     - バックアップZIPファイル
   * - ``overwrite``
     - いいえ
     - 既存設定を上書き（デフォルト: false）
   * - ``types``
     - いいえ
     - インポート対象（カンマ区切り、デフォルト: all）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Backup imported successfully",
        "imported": {
          "webconfig": 5,
          "fileconfig": 3,
          "dataconfig": 2,
          "scheduler": 4,
          "user": 10,
          "role": 5,
          "group": 3,
          "labeltype": 8,
          "keymatch": 12,
          "dict": 3
        }
      }
    }

使用例
======

全設定のエクスポート
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup.zip

特定設定のエクスポート
----------------------

.. code-block:: bash

    # Webクロール設定とユーザー設定のみエクスポート
    curl -X GET "http://localhost:8080/api/admin/backup/export?types=webconfig,user" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup-partial.zip

設定のインポート
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=false"

既存設定を上書きしてインポート
------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=true"

特定設定のみインポート
----------------------

.. code-block:: bash

    # ユーザーとロールのみインポート
    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "types=user,role" \
         -F "overwrite=false"

バックアップの自動化
--------------------

.. code-block:: bash

    #!/bin/bash
    # 毎日午前2時にバックアップを取得するスクリプト例

    DATE=$(date +%Y%m%d)
    BACKUP_DIR="/backup/fess"

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o "${BACKUP_DIR}/fess-backup-${DATE}.zip"

    # 30日より古いバックアップを削除
    find "${BACKUP_DIR}" -name "fess-backup-*.zip" -mtime +30 -delete

注意事項
========

- バックアップにはパスワード情報も含まれるため、セキュアに保管してください
- インポート時に ``overwrite=true`` を指定すると既存設定が上書きされます
- 大規模な設定の場合、エクスポート/インポートに時間がかかる場合があります
- バージョンが異なるFess間でのインポートは互換性の問題が発生する可能性があります

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`../../admin/backup-guide` - バックアップ管理ガイド
- :doc:`../../admin/maintenance-guide` - メンテナンスガイド
