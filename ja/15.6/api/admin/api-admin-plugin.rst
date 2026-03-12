==========================
Plugin API
==========================

概要
====

Plugin APIは、|Fess| のプラグインを管理するためのAPIです。
プラグインのインストール、有効化、無効化、削除などを操作できます。

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
     - /
     - プラグイン一覧取得
   * - POST
     - /install
     - プラグインインストール
   * - DELETE
     - /{id}
     - プラグイン削除

プラグイン一覧取得
==================

リクエスト
----------

::

    GET /api/admin/plugin

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "plugins": [
          {
            "id": "analysis-kuromoji",
            "name": "Japanese (kuromoji) Analysis Plugin",
            "version": "2.11.0",
            "description": "Japanese language analysis plugin",
            "enabled": true,
            "installed": true
          },
          {
            "id": "analysis-icu",
            "name": "ICU Analysis Plugin",
            "version": "2.11.0",
            "description": "Unicode normalization and collation",
            "enabled": true,
            "installed": true
          }
        ],
        "total": 2
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``id``
     - プラグインID
   * - ``name``
     - プラグイン名
   * - ``version``
     - プラグインバージョン
   * - ``description``
     - プラグイン説明
   * - ``enabled``
     - 有効化状態
   * - ``installed``
     - インストール状態

プラグインインストール
======================

リクエスト
----------

::

    POST /api/admin/plugin/install
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "url": "https://example.com/plugins/my-plugin-1.0.0.zip"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``url``
     - はい
     - プラグインのダウンロードURL

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin installed successfully. Restart required.",
        "pluginId": "my-plugin"
      }
    }

プラグイン削除
==============

リクエスト
----------

::

    DELETE /api/admin/plugin/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin deleted successfully. Restart required."
      }
    }

使用例
======

プラグイン一覧の取得
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN"

プラグインのインストール
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin/install" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "url": "https://artifacts.opensearch.org/releases/plugins/analysis-icu/2.11.0/analysis-icu-2.11.0.zip"
         }'

プラグインの削除
----------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin/analysis-icu" \
         -H "Authorization: Bearer YOUR_TOKEN"

注意事項
========

- プラグインのインストールまたは削除後は、Fessの再起動が必要です
- 互換性のないプラグインをインストールするとFessが起動しなくなる可能性があります
- プラグインの削除は慎重に行ってください。依存関係がある場合、システムに影響を与える可能性があります

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-systeminfo` - システム情報API
- :doc:`../../admin/plugin-guide` - プラグイン管理ガイド
