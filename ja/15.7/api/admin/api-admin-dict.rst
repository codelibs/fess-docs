==========================
Dict API
==========================

概要
====

Dict APIは、|Fess| の辞書を管理するためのAPIです。
ルートのエンドポイントで利用可能な辞書の一覧を取得できます。
個々の辞書項目の参照・作成・更新・削除、辞書ファイルのアップロード・ダウンロードは、
辞書種別ごとのサブエンドポイント（synonym、kuromoji、mapping、protwords、stopwords、stemmeroverride）で操作します。

ベースURL
=========

::

    /api/admin/dict

エンドポイント一覧
==================

辞書ルート
----------

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /
     - 辞書一覧取得

辞書種別ごとのエンドポイント
----------------------------

``{type}`` には ``synonym`` 、 ``kuromoji`` 、 ``mapping`` 、 ``protwords`` 、 ``stopwords`` 、 ``stemmeroverride`` のいずれかを指定します。
これらの値は、辞書一覧取得のレスポンスに含まれる ``type`` フィールドの値と一致します。
``{dictId}`` は辞書一覧取得で得られる辞書のIDです。

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - メソッド
     - パス
     - 説明
   * - GET
     - /{type}/settings/{dictId}
     - 辞書項目一覧取得
   * - GET
     - /{type}/setting/{dictId}/{id}
     - 辞書項目取得
   * - POST
     - /{type}/setting/{dictId}
     - 辞書項目作成
   * - PUT
     - /{type}/setting/{dictId}
     - 辞書項目更新
   * - DELETE
     - /{type}/setting/{dictId}/{id}
     - 辞書項目削除
   * - PUT
     - /{type}/upload/{dictId}
     - 辞書ファイルアップロード
   * - GET
     - /{type}/download/{dictId}
     - 辞書ファイルダウンロード

辞書一覧取得
============

利用可能な辞書ファイルの一覧を取得します。

リクエスト
----------

::

    GET /api/admin/dict

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "ZjA5...synonym.txt",
            "type": "synonym",
            "path": "/var/lib/fess/dict/synonym.txt",
            "timestamp": "2025-01-29T10:00:00.000+0000"
          },
          {
            "id": "ZjA5...mapping.txt",
            "type": "mapping",
            "path": "/var/lib/fess/dict/mapping.txt",
            "timestamp": "2025-01-28T15:30:00.000+0000"
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
   * - ``settings[].id``
     - 辞書ID（個々の辞書操作で ``{dictId}`` として使用）
   * - ``settings[].type``
     - 辞書種別
   * - ``settings[].path``
     - 辞書ファイルのパス
   * - ``settings[].timestamp``
     - 辞書ファイルの更新日時
   * - ``total``
     - 辞書ファイルの総数

辞書項目一覧取得
================

指定した辞書内の項目を一覧取得します。

リクエスト
----------

::

    GET /api/admin/dict/{type}/settings/{dictId}

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``dictId``
     - String
     - はい
     - 辞書ID（パスパラメーター）
   * - ``size``
     - Integer
     - いいえ
     - 1ページあたりの件数（デフォルト: 25）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始、デフォルト: 1）

レスポンス
----------

レスポンスの ``settings`` 配列の各項目のフィールドは辞書種別により異なります（後述の「辞書種別ごとの項目フィールド」を参照）。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": 1,
            "dictId": "ZjA5...synonym.txt",
            "inputs": "検索,サーチ",
            "outputs": "検索,サーチ,リサーチ"
          }
        ],
        "total": 1
      }
    }

上記は ``synonym`` 辞書の例です。

辞書項目取得
============

辞書内の特定の項目を取得します。

リクエスト
----------

::

    GET /api/admin/dict/{type}/setting/{dictId}/{id}

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``dictId``
     - String
     - はい
     - 辞書ID（パスパラメーター）
   * - ``id``
     - Long
     - はい
     - 項目ID（パスパラメーター）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": 1,
          "dictId": "ZjA5...synonym.txt",
          "inputs": "検索,サーチ",
          "outputs": "検索,サーチ,リサーチ"
        }
      }
    }

辞書項目作成
============

辞書に新しい項目を作成します。

リクエスト
----------

::

    POST /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

リクエストボディ（synonymの例）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ"
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": true
      }
    }

辞書項目更新
============

辞書内の既存の項目を更新します。

リクエスト
----------

::

    PUT /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

リクエストボディ（synonymの例）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": 1,
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ,search"
    }

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

辞書項目削除
============

辞書内の項目を削除します。

リクエスト
----------

::

    DELETE /api/admin/dict/{type}/setting/{dictId}/{id}

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``dictId``
     - String
     - はい
     - 辞書ID（パスパラメーター）
   * - ``id``
     - Long
     - はい
     - 項目ID（パスパラメーター）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

辞書ファイルアップロード
========================

辞書ファイル全体をアップロードして置き換えます。

リクエスト
----------

::

    PUT /api/admin/dict/{type}/upload/{dictId}
    Content-Type: multipart/form-data

ファイルフィールドの名前は辞書種別ごとに異なります（後述の「辞書種別ごとの項目フィールド」を参照）。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

辞書ファイルダウンロード
========================

辞書ファイルをダウンロードします。

リクエスト
----------

::

    GET /api/admin/dict/{type}/download/{dictId}

レスポンスは辞書ファイルのバイナリ（ ``application/octet-stream`` ）です。

辞書種別ごとの項目フィールド
============================

辞書項目の作成・更新リクエストボディおよびレスポンスのフィールドは、辞書種別ごとに異なります。
``id`` （項目ID）と ``dictId`` （辞書ID）はレスポンスに共通して含まれます。

.. list-table::
   :header-rows: 1
   :widths: 18 42 40

   * - 種別
     - 項目フィールド
     - アップロードファイルフィールド
   * - ``synonym``
     - ``inputs`` （必須）、 ``outputs`` （必須）
     - ``synonymFile``
   * - ``kuromoji``
     - ``token`` （必須）、 ``segmentation`` （必須）、 ``reading`` （必須）、 ``pos`` （必須）
     - ``kuromojiFile``
   * - ``mapping``
     - ``inputs`` （必須）、 ``output``
     - ``charMappingFile``
   * - ``protwords``
     - ``input`` （必須）
     - ``protwordsFile``
   * - ``stopwords``
     - ``input`` （必須）
     - ``stopwordsFile``
   * - ``stemmeroverride``
     - ``input`` （必須）、 ``output`` （必須）
     - ``stemmerOverrideFile``

使用例
======

辞書一覧の取得
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

同義語辞書の項目一覧取得
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/settings/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN"

同義語辞書への項目追加
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/synonym/setting/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "inputs": "検索,サーチ",
           "outputs": "検索,サーチ,リサーチ"
         }'

同義語辞書ファイルのアップロード
--------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym/upload/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "synonymFile=@synonym.txt"

同義語辞書ファイルのダウンロード
--------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/download/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o synonym.txt

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`../../admin/dict-guide` - 辞書管理ガイド
