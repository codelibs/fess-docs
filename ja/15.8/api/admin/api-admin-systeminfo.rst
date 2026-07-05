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

このAPIへのアクセスには ``Radmin-api`` 権限を持つアクセストークンが必要です。
認証方法の詳細は :doc:`api-admin-overview` を参照してください。

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

このエンドポイントはクエリパラメーターを受け付けません。

レスポンス
----------

レスポンスは、製品バージョンを示す ``version``、処理結果を示す ``status`` と、
以下の4つのプロパティ群を含みます。各プロパティ群は ``label`` と ``value`` を持つ
オブジェクトの配列です。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "envProps": [
          {"label": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"label": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"label": "java.version", "value": "21.0.1"},
          {"label": "java.vendor", "value": "Oracle Corporation"},
          {"label": "os.name", "value": "Linux"},
          {"label": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"label": "crawler.document.max.site.length", "value": "100"},
          {"label": "indexer.thread.dump.enabled", "value": "true"},
          {"label": "app.cipher.key", "value": "XXXXXXXX"}
        ],
        "bugReportProps": [
          {"label": "os.name", "value": "Linux"},
          {"label": "java.vm.version", "value": "21.0.1+12"}
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
   * - ``version``
     - |Fess| の製品バージョン（例: ``15.8.0``）。
   * - ``status``
     - 処理結果を示すコード。``0`` は正常終了を表します。
   * - ``envProps``
     - 環境変数の一覧（``label`` / ``value`` の配列）。``System.getenv()`` で取得される値がそのまま返されます。
   * - ``systemProps``
     - Javaのシステムプロパティの一覧（``label`` / ``value`` の配列）。``System.getProperties()`` で取得される値がそのまま返されます。
   * - ``fessProps``
     - |Fess| の設定プロパティの一覧（``label`` / ``value`` の配列）。``fess_config.properties`` の設定値と、管理画面で設定されるシステムプロパティが含まれます。機密性の高い項目はマスクされます（下記の注記を参照）。
   * - ``bugReportProps``
     - バグレポート用に収集される情報の一覧（``label`` / ``value`` の配列）。OSおよびJava実行環境に関する主要なシステムプロパティ（``os.name``、``os.version``、``java.vm.version`` など）と、|Fess| のシステムプロパティ設定値が含まれます。

.. note::

   ``fessProps`` では、以下の機密性の高い設定値はマスクされ、``XXXXXXXX`` として返されます:
   ``http.proxy.password``、``ldap.admin.security.credentials``、``spnego.preauth.password``、
   ``app.cipher.key``、``oic.client.id``、``oic.client.secret``。

.. warning::

   ``envProps``（環境変数）と ``systemProps``（Javaシステムプロパティ）はマスクされず、
   設定されている値がそのまま返されます。環境変数やシステムプロパティに認証情報などの
   機密情報を含めている場合、それらがレスポンスに含まれる点に注意してください。

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
         | jq -r '.response.systemProps[] | select(.label == "java.version") | .value'

環境変数の一覧表示
------------------

.. code-block:: bash

    # 環境変数を label=value 形式で表示
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.label)=\(.value)"'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-stats` - 統計API
- :doc:`api-admin-general` - 一般設定API
- :doc:`../../admin/systeminfo-guide` - システム情報ガイド
