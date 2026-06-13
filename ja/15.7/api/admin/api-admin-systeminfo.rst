==========================
SystemInfo API
==========================

概要
====

SystemInfo APIは、|Fess| のシステム情報を取得するためのAPIです。
環境変数、Javaのシステムプロパティ、|Fess| の設定プロパティ、バグレポート用情報を確認できます。

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

レスポンスは、製品バージョンを示す ``version``、処理結果を示す ``status`` と、
以下の4つのプロパティ群を含みます。各プロパティ群は ``key`` と ``value`` を持つ
オブジェクトの配列です。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"key": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"key": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"key": "java.version", "value": "21.0.1"},
          {"key": "java.vendor", "value": "Oracle Corporation"},
          {"key": "os.name", "value": "Linux"},
          {"key": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"key": "crawler.document.max.site.length", "value": "50"},
          {"key": "indexer.thread.dump.enabled", "value": "true"}
        ],
        "bugReportProps": [
          {"key": "os.name", "value": "Linux"},
          {"key": "java.vm.version", "value": "21.0.1+12"}
        ]
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``envProps``
     - 環境変数の一覧（``key`` / ``value`` の配列）
   * - ``systemProps``
     - Javaのシステムプロパティの一覧（``key`` / ``value`` の配列）
   * - ``fessProps``
     - |Fess| の設定プロパティの一覧（``key`` / ``value`` の配列）
   * - ``bugReportProps``
     - バグレポート用に収集される情報の一覧（``key`` / ``value`` の配列）

使用例
======

システム情報の取得
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

特定のシステムプロパティの抽出
------------------------------

.. code-block:: bash

    # java.version の値のみを抽出
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.systemProps[] | select(.key == "java.version") | .value'

環境変数の一覧表示
------------------

.. code-block:: bash

    # 環境変数を key=value 形式で表示
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.key)=\(.value)"'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-stats` - 統計API
- :doc:`api-admin-general` - 一般設定API
- :doc:`../../admin/systeminfo-guide` - システム情報ガイド
