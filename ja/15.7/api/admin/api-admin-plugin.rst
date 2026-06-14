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

インストール済みプラグイン一覧取得
==================================

インストール済みのプラグインの一覧を返します。

リクエスト
----------

::

    GET /api/admin/plugin/installed

レスポンス
----------

``plugins`` にプラグイン情報を表すオブジェクトの配列が格納されます。
各オブジェクトは文字列のキーと値のマップで、``name`` （プラグイン名）や ``version`` （バージョン）などを含みます。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

インストール可能プラグイン一覧取得
==================================

インストール可能なプラグインの一覧を返します。

リクエスト
----------

::

    GET /api/admin/plugin/available

レスポンス
----------

``plugins`` にインストール可能なプラグイン情報を表すオブジェクトの配列が格納されます。
各オブジェクトは ``installed`` 同様、文字列のキーと値のマップです。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
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
      "version": "15.7.0"
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

レスポンス
----------

成功時は ``status`` のみを返します。
``name`` または ``version`` に該当するアーティファクトが存在しない場合は、``status`` が ``1`` （BAD_REQUEST）となり、``message`` に ``invalid name or version`` が設定されます。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

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
      "version": "15.7.0"
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
     - プラグインのバージョン（最大100文字）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

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
           "version": "15.7.0"
         }'

プラグインの削除
----------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
