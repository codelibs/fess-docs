==========================
SystemInfo API
==========================

概要
====

SystemInfo APIは、|Fess| のシステム情報を取得するためのAPIです。
バージョン情報、環境変数、JVM情報などを確認できます。

ベースURL
=========

::

    /api/admin/systeminfo

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
     - システム情報取得

システム情報取得
================

リクエスト
----------

::

    GET /api/admin/systeminfo

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "systemInfo": {
          "fessVersion": "15.5.0",
          "opensearchVersion": "2.11.0",
          "javaVersion": "21.0.1",
          "serverName": "Apache Tomcat/10.1.15",
          "osName": "Linux",
          "osVersion": "5.15.0-89-generic",
          "osArchitecture": "amd64",
          "jvmTotalMemory": "2147483648",
          "jvmFreeMemory": "1073741824",
          "jvmMaxMemory": "4294967296",
          "processorCount": "8",
          "fileEncoding": "UTF-8",
          "userLanguage": "ja",
          "userTimezone": "Asia/Tokyo"
        },
        "environmentInfo": {
          "JAVA_HOME": "/usr/lib/jvm/java-21",
          "FESS_DICTIONARY_PATH": "/var/lib/fess/dict",
          "FESS_LOG_PATH": "/var/log/fess"
        },
        "systemProperties": {
          "java.version": "21.0.1",
          "java.vendor": "Oracle Corporation",
          "os.name": "Linux",
          "os.version": "5.15.0-89-generic",
          "user.dir": "/opt/fess",
          "user.home": "/home/fess",
          "user.name": "fess"
        }
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``fessVersion``
     - Fessのバージョン
   * - ``opensearchVersion``
     - OpenSearchのバージョン
   * - ``javaVersion``
     - Javaのバージョン
   * - ``serverName``
     - アプリケーションサーバー名
   * - ``osName``
     - OS名
   * - ``osVersion``
     - OSバージョン
   * - ``osArchitecture``
     - OSアーキテクチャ
   * - ``jvmTotalMemory``
     - JVMの総メモリ（バイト）
   * - ``jvmFreeMemory``
     - JVMの空きメモリ（バイト）
   * - ``jvmMaxMemory``
     - JVMの最大メモリ（バイト）
   * - ``processorCount``
     - プロセッサー数
   * - ``fileEncoding``
     - ファイルエンコーディング
   * - ``userLanguage``
     - ユーザー言語
   * - ``userTimezone``
     - ユーザータイムゾーン

使用例
======

システム情報の取得
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

バージョン確認
--------------

.. code-block:: bash

    # Fessバージョンのみを抽出
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo.fessVersion'

メモリ使用状況の確認
--------------------

.. code-block:: bash

    # JVMメモリ情報を抽出
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo | {total: .jvmTotalMemory, free: .jvmFreeMemory, max: .jvmMaxMemory}'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-stats` - 統計API
- :doc:`api-admin-general` - 一般設定API
- :doc:`../../admin/systeminfo-guide` - システム情報ガイド
