==========================
Plugin API
==========================

概要
====

Plugin APIは、|Fess| のプラグイン（アーティファクト）を管理するためのAPIです。
インストール済みプラグインおよびインストール可能なプラグインの一覧取得、プラグインのインストール・削除を操作できます。

ベースURL
=========

::

    /api/admin/plugin

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /installed
     - インストール済みプラグイン一覧取得
   * - GET
     - /available
     - インストール可能プラグイン一覧取得
   * - POST
     - /
     - プラグインインストール
   * - DELETE
     - /
     - プラグイン削除

プラグイン情報のフィールド
==========================

一覧取得系のエンドポイント（``/installed`` および ``/available``）が返す ``plugins``
配列の各要素は、以下のフィールドを持つオブジェクトです。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - フィールド
     - 説明
   * - ``type``
     - アーティファクトの種別ID。\ ``fess-ds`` （データストア）、``fess-theme`` （テーマ）、
       ``fess-ingest`` （Ingest）、``fess-script`` （スクリプト）、``fess-webapp`` （Webアプリ）、
       ``fess-thumbnail`` （サムネイル）、``fess-crawler`` （クローラ）、``fess-llm`` （LLM）、
       ``jar`` （上記以外の汎用JAR）のいずれかです。
   * - ``id``
     - ``{name}:{version}`` 形式の識別子。
   * - ``name``
     - プラグイン名。
   * - ``version``
     - プラグインのバージョン。
   * - ``url``
     - ダウンロード元のURL。\ ``/available`` の応答にのみ含まれます。\ ``/installed`` では
       値が存在しないため、フィールド自体が省略されます。

.. note::

   |Fess| のAPIレスポンスでは値が ``null`` のフィールドは出力されません。そのため、
   インストール済みプラグインの各要素には ``url`` が含まれません。

インストール済みプラグイン一覧取得
==================================

インストール済みのプラグインの一覧を返します。プラグインディレクトリ上のアーティファクトを
種別ごとに走査し、名前順にソートして返します。

リクエスト
----------

::

    GET /api/admin/plugin/installed

レスポンス
----------

``plugins`` にプラグイン情報を表すオブジェクトの配列が格納されます。
各オブジェクトのフィールドは `プラグイン情報のフィールド`_ を参照してください。
インストール済みプラグインでは ``url`` は出力されません。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.8.0",
            "name": "fess-ds-slack",
            "version": "15.8.0"
          }
        ]
      }
    }

インストール可能プラグイン一覧取得
==================================

インストール可能なプラグインの一覧を返します。\ ``fess_config.properties`` の
``plugin.repositories`` に設定されたリポジトリから、全種別のアーティファクトを取得します。
取得結果は一定時間（既定で5分）キャッシュされます。

リクエスト
----------

::

    GET /api/admin/plugin/available

レスポンス
----------

``plugins`` にインストール可能なプラグイン情報を表すオブジェクトの配列が格納されます。
各オブジェクトのフィールドは `プラグイン情報のフィールド`_ を参照してください。
インストール可能プラグインでは、ダウンロード元の ``url`` が含まれます。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.8.0",
            "name": "fess-ds-slack",
            "version": "15.8.0",
            "url": "https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-slack/15.8.0/fess-ds-slack-15.8.0.jar"
          }
        ]
      }
    }

プラグインインストール
======================

指定した名前とバージョンのプラグインをインストールします。

リクエスト
----------

::

    POST /api/admin/plugin
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.8.0"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - プラグイン名（最大100文字）
   * - ``version``
     - はい
     - プラグインのバージョン（最大100文字）

.. note::

   ``name`` と ``version`` は、``/available`` で取得できるインストール可能プラグインの
   いずれかと一致している必要があります。一致するアーティファクトが存在しない場合は
   エラーになります。

レスポンス
----------

リクエストが受け付けられると ``status`` が ``0`` （OK）のレスポンスを返します。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

``name`` または ``version`` に該当するアーティファクトが存在しない場合は、``status`` が
``1`` （BAD_REQUEST）となり、``message`` に ``invalid name or version`` が設定されます。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "invalid name or version"
      }
    }

.. note::

   インストール処理はバックグラウンドで非同期に実行されます。\ ``status: 0`` のレスポンスは
   リクエストが受け付けられたことを示すものであり、インストールの完了を保証するものでは
   ありません。インストール完了後、同名で別バージョンのプラグインがインストール済みの
   場合は、それらが自動的に削除されます。ダウンロードやインストールに失敗した場合は
   サーバーログに記録されますが、APIのレスポンスには反映されません。

プラグイン削除
==============

指定した名前とバージョンのプラグインを削除します。

リクエスト
----------

::

    DELETE /api/admin/plugin
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.8.0"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - フィールド
     - 必須
     - 説明
   * - ``name``
     - はい
     - プラグイン名（最大100文字）
   * - ``version``
     - いいえ
     - プラグインのバージョン（最大100文字）。削除対象を一意に特定するため、指定することを推奨します。

レスポンス
----------

リクエストが受け付けられると ``status`` が ``0`` （OK）のレスポンスを返します。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

.. note::

   削除処理はバックグラウンドで非同期に実行されます。\ ``status: 0`` のレスポンスは
   リクエストが受け付けられたことを示すもので、該当するプラグインが存在するか、削除が
   成功したかは判定しません。削除に失敗した場合（対象ファイルが存在しない場合など）は
   サーバーログに記録されますが、APIのレスポンスには反映されません。

使用例
======

インストール済みプラグイン一覧の取得
------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin/installed" \
         -H "Authorization: Bearer YOUR_TOKEN"

プラグインのインストール
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.8.0"
         }'

プラグインの削除
----------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.8.0"
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
