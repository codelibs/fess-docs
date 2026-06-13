==========================
Stats API
==========================

概要
====

Stats APIは、|Fess| が稼働するサーバーのシステムメトリクスを取得するためのAPIです。
JVM、OS、プロセス、検索エンジン（OpenSearch）クラスター、ファイルシステムの各統計情報を確認できます。

.. note::

   このAPIは検索クエリやクリックなどの検索分析データを返すものではありません。
   インデックス内のドキュメントの検索・管理には :doc:`api-admin-searchlist` を参照してください。

ベースURL
=========

::

    /api/admin/stats

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
     - システム統計情報取得

システム統計情報取得
====================

リクエスト
----------

::

    GET /api/admin/stats

このエンドポイントはクエリパラメーターを受け付けません。

レスポンス
----------

レスポンスは、製品バージョンを示す ``version``、処理結果を示す ``status`` と、
システムメトリクスを格納する ``stats`` オブジェクトを含みます。
``stats`` は ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs`` の5つのキーを持ちます。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "stats": {
          "jvm": {
            "memory": {
              "heap": {
                "used": 536870912,
                "committed": 1073741824,
                "max": 2147483648,
                "percent": 25
              },
              "nonHeap": {
                "used": 134217728,
                "committed": 268435456
              }
            },
            "pools": [
              {"key": "mapped", "count": 1, "used": 4096, "capacity": 4096}
            ],
            "gc": [
              {"key": "young", "count": 12, "time": 345}
            ],
            "threads": {"count": 80, "peak": 95},
            "classes": {"loaded": 12000, "total_loaded": 12500, "unloaded": 500},
            "uptime": 3600000
          },
          "os": {
            "memory": {
              "physical": {"free": 2147483648, "total": 8589934592},
              "swapSpace": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "loadAverages": [0.5, 0.4, 0.3]
          },
          "process": {
            "fileFescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtualMemory": {"total": 4294967296}
          },
          "engine": {
            "clusterName": "fess",
            "numberOfNodes": 1,
            "numberOfDataNodes": 1,
            "activePrimaryShards": 10,
            "activeShards": 10,
            "activeShardsPercent": 100.0,
            "relocatingShards": 0,
            "initializingShards": 0,
            "unassignedShards": 0,
            "delayedUnassignedShards": 0,
            "numberOfPendingTasks": 0,
            "numberOfInFlightFetch": 0,
            "status": "green"
          },
          "fs": [
            {
              "path": "/",
              "total": 107374182400,
              "free": 53687091200,
              "usable": 53687091200,
              "used": 53687091200,
              "percent": 50
            }
          ]
        }
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - フィールド
     - 説明
   * - ``jvm``
     - JVM統計。``memory``（``heap`` / ``nonHeap``）、``pools``（バッファプール）、``gc``（GC）、``threads``、``classes``、``uptime``（ミリ秒）を含みます。
   * - ``os``
     - OS統計。``memory``（``physical`` / ``swapSpace``）、``cpu``、``loadAverages``（ロードアベレージの配列）を含みます。
   * - ``process``
     - プロセス統計。``fileFescriptor``（オープン/最大ファイルディスクリプタ数）、``cpu``、``virtualMemory`` を含みます。
   * - ``engine``
     - 検索エンジン（OpenSearch）クラスターの状態。``clusterName``、ノード数、シャード数、``status`` などを含みます。クラスターに接続できない場合は ``status`` が ``"red"`` となり、``exception`` にエラーメッセージが含まれます。
   * - ``fs``
     - ファイルシステム統計の配列。各ルートについて ``path``、``total``、``free``、``usable``、``used``（バイト）、``percent``（使用率）を含みます。

.. note::

   ``process.fileFescriptor`` というキー名はソースコードの実装に準じています（``fileDescriptor`` のスペルではありません）。

使用例
======

システム統計情報の取得
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

JVMヒープ使用率の確認
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

検索エンジンクラスターの状態確認
--------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-systeminfo` - システム情報API
- :doc:`api-admin-searchlist` - ドキュメント検索・管理API
