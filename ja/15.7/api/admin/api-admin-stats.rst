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

.. note::

   ``stats`` 配下のオブジェクトのフィールド名は、スネークケース（小文字とアンダースコア区切り、例: ``non_heap``）で出力されます。
   値が ``null`` のフィールドはレスポンスから省略されます。

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
              "non_heap": {
                "used": 134217728,
                "committed": 268435456,
                "max": 0,
                "percent": 0
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
              "swap_space": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "load_averages": [0.5, 0.4, 0.3]
          },
          "process": {
            "file_fescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtual_memory": {"total": 4294967296}
          },
          "engine": {
            "cluster_name": "fess",
            "number_of_nodes": 1,
            "number_of_data_nodes": 1,
            "active_primary_shards": 10,
            "active_shards": 10,
            "active_shards_percent": 100.0,
            "relocating_shards": 0,
            "initializing_shards": 0,
            "unassigned_shards": 0,
            "delayed_unassigned_shards": 0,
            "number_of_pending_tasks": 0,
            "number_of_in_flight_fetch": 0,
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

レスポンスフィールド（トップレベル）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - フィールド
     - 説明
   * - ``version``
     - |Fess| の製品バージョン（例: ``15.7.0``）。
   * - ``status``
     - 処理結果を示すコード。``0`` は正常終了を表します。
   * - ``stats``
     - システムメトリクスを格納するオブジェクト。``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs`` の5つのキーを持ちます。

``jvm``: JVM統計
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - フィールド
     - 説明
   * - ``memory.heap.used``
     - 使用中のヒープメモリ（バイト）。
   * - ``memory.heap.committed``
     - 確保済みのヒープメモリ（バイト）。
   * - ``memory.heap.max``
     - ヒープメモリの最大値（バイト）。
   * - ``memory.heap.percent``
     - ヒープメモリの使用率（%）。
   * - ``memory.non_heap.used``
     - 使用中の非ヒープメモリ（バイト）。
   * - ``memory.non_heap.committed``
     - 確保済みの非ヒープメモリ（バイト）。
   * - ``memory.non_heap.max``
     - 非ヒープメモリの最大値（バイト）。現在の実装では値が設定されず、常に ``0`` が返されます。
   * - ``memory.non_heap.percent``
     - 非ヒープメモリの使用率（%）。現在の実装では値が設定されず、常に ``0`` が返されます。
   * - ``pools``
     - バッファプールの配列。各要素は ``key``（プール名）、``count``（バッファ数）、``used``（使用量、バイト）、``capacity``（総容量、バイト）を含みます。
   * - ``gc``
     - ガベージコレクタの配列。各要素は ``key``（コレクタ名）、``count``（実行回数）、``time``（累積実行時間、ミリ秒）を含みます。
   * - ``threads.count``
     - 現在のスレッド数。
   * - ``threads.peak``
     - スレッド数のピーク値。
   * - ``classes.loaded``
     - 現在ロードされているクラス数。
   * - ``classes.total_loaded``
     - JVM起動以降にロードされた総クラス数。
   * - ``classes.unloaded``
     - アンロードされた総クラス数。
   * - ``uptime``
     - JVMの稼働時間（ミリ秒）。

``os``: OS統計
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - フィールド
     - 説明
   * - ``memory.physical.free``
     - 空き物理メモリ（バイト）。
   * - ``memory.physical.total``
     - 総物理メモリ（バイト）。
   * - ``memory.swap_space.free``
     - 空きスワップ領域（バイト）。
   * - ``memory.swap_space.total``
     - 総スワップ領域（バイト）。
   * - ``cpu.percent``
     - システム全体のCPU使用率（%）。
   * - ``load_averages``
     - ロードアベレージの配列（1分・5分・15分）。取得できない値は ``-1`` になることがあります。

``process``: プロセス統計
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - フィールド
     - 説明
   * - ``file_fescriptor.open``
     - オープン中のファイルディスクリプタ数。
   * - ``file_fescriptor.max``
     - オープン可能なファイルディスクリプタの最大数。
   * - ``cpu.percent``
     - プロセスのCPU使用率（%）。
   * - ``cpu.total``
     - プロセスが使用した累積CPU時間（ミリ秒）。
   * - ``virtual_memory.total``
     - プロセスの総仮想メモリサイズ（バイト）。

.. note::

   ``process.file_fescriptor`` というキー名は、ソースコードのフィールド名 ``fileFescriptor``
   （``fileDescriptor`` の綴り誤りに由来）をスネークケースに変換したものです。実装に合わせており、誤記ではありません。

``engine``: 検索エンジンクラスター統計
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

検索エンジン（OpenSearch）クラスターのヘルス情報です。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - フィールド
     - 説明
   * - ``cluster_name``
     - クラスター名。
   * - ``number_of_nodes``
     - クラスター内の総ノード数。
   * - ``number_of_data_nodes``
     - データノード数。
   * - ``active_primary_shards``
     - アクティブなプライマリシャード数。
   * - ``active_shards``
     - アクティブなシャード数。
   * - ``active_shards_percent``
     - アクティブなシャードの割合（%）。
   * - ``relocating_shards``
     - 再配置中のシャード数。
   * - ``initializing_shards``
     - 初期化中のシャード数。
   * - ``unassigned_shards``
     - 未割り当てのシャード数。
   * - ``delayed_unassigned_shards``
     - 割り当てが遅延している未割り当てシャード数。
   * - ``number_of_pending_tasks``
     - 保留中のタスク数。
   * - ``number_of_in_flight_fetch``
     - 実行中のフェッチ操作数。
   * - ``status``
     - クラスターのヘルス状態（``green`` / ``yellow`` / ``red``）。
   * - ``exception``
     - クラスターに接続できないなどのエラー発生時のみ含まれるエラーメッセージ。この場合、``status`` は ``red`` になります。

``fs``: ファイルシステム統計
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

各ルート（``File.listRoots()`` で取得されるルート）ごとの統計情報を格納した配列です。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - フィールド
     - 説明
   * - ``path``
     - ルートの絶対パス。
   * - ``total``
     - 総容量（バイト）。
   * - ``free``
     - 空き容量（バイト）。
   * - ``usable``
     - 使用可能な容量（バイト）。
   * - ``used``
     - 使用済み容量（バイト）。``total`` から ``usable`` を引いた値です。
   * - ``percent``
     - 使用率（%）。

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
