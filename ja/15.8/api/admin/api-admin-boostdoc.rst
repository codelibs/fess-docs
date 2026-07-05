==========================
BoostDoc API
==========================

概要
====

BoostDoc APIは、|Fess| のドキュメントブースト設定を管理するためのAPIです。
ドキュメントブーストを設定すると、特定の条件に一致するドキュメントのスコアを引き上げ、
検索結果の上位に表示されやすくできます。

ブーストはインデックス作成時（クロール時）に各ドキュメントへ適用されます。
条件（``urlExpr``）とブースト値（``boostExpr``）はいずれもGroovyの式として評価されます。
複数のルールは ``sortOrder`` の昇順で評価され、最初に条件が一致したルールのブースト値のみが適用されます
（一致したルールが見つかると、それ以降のルールは評価されません）。

.. note::

   管理画面では、``urlExpr`` は「条件」、``boostExpr`` は「ブースト値式」として表示されます。
   設定項目の詳細は :doc:`../../admin/boostdoc-guide` を参照してください。

ベースURL
=========

::

    /api/admin/boostdoc

認証
====

このAPIを利用するには、``Radmin-api`` 権限を持つアクセストークンが必要です。
アクセストークンの取得方法と指定方法は :doc:`api-admin-overview` を参照してください。

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /settings
     - ドキュメントブースト一覧取得
   * - GET
     - /setting/{id}
     - ドキュメントブースト取得
   * - POST
     - /setting
     - ドキュメントブースト作成
   * - PUT
     - /setting
     - ドキュメントブースト更新
   * - DELETE
     - /setting/{id}
     - ドキュメントブースト削除

ドキュメントブースト一覧取得
============================

リクエスト
----------

::

    GET /api/admin/boostdoc/settings

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``size``
     - Integer
     - いいえ
     - 1ページあたりの件数（デフォルト: 25）
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始。デフォルト: 1）
   * - ``urlExpr``
     - String
     - いいえ
     - 条件式による絞り込み（部分一致）
   * - ``boostExpr``
     - String
     - いいえ
     - ブースト値式による絞り込み（部分一致）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "boostdoc_id_1",
            "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
            "boostExpr": "3.0",
            "sortOrder": 1,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   レスポンスの各設定オブジェクトには、上記フィールドに加えて、作成・更新に関するメタデータ
   （``createdBy``、``createdTime``、``updatedBy``、``updatedTime``）も含まれます。
   ``versionNo`` は更新（PUT）時に必須となるため、更新前に取得・一覧APIで現在の値を確認してください。

ドキュメントブースト取得
========================

リクエスト
----------

::

    GET /api/admin/boostdoc/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
          "boostExpr": "3.0",
          "sortOrder": 1,
          "versionNo": 1
        }
      }
    }

ドキュメントブースト作成
========================

リクエスト
----------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "5.0",
      "sortOrder": 0
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``urlExpr``
     - はい
     - 条件式。ブースト対象のドキュメントを判定するGroovy式で、``Boolean`` を返します。管理画面の「条件」に相当します（最大10000文字）。
   * - ``boostExpr``
     - はい
     - ブースト値式。ブースト値（数値）を返すGroovy式です。``3.0`` のような固定値も指定できます。管理画面の「ブースト値式」に相当します（最大10000文字）。
   * - ``sortOrder``
     - はい
     - 適用順序。ルールは昇順で評価され、最初に条件が一致したルールのブースト値が適用されます（フォーム初期値: 0、0以上の整数）。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

ドキュメントブースト更新
========================

リクエスト
----------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

更新時は、作成時のフィールドに加えて ``id``（更新対象のID、最大1000文字）と ``versionNo``（楽観的ロック用のバージョン番号）が必須です。
``versionNo`` には、取得・一覧APIのレスポンスに含まれる現在のバージョン番号を指定します。バージョン番号が一致しない場合、更新は失敗します。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

ドキュメントブースト削除
========================

リクエスト
----------

::

    DELETE /api/admin/boostdoc/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

条件式・ブースト値式について
============================

``urlExpr``（条件）と ``boostExpr``（ブースト値式）は、いずれもGroovyの式として評価されます。
式の中では、インデックス対象ドキュメントのフィールド値をフィールド名の変数として参照できます。

- ``urlExpr`` は ``Boolean`` を返す必要があります（例: ``url.startsWith("https://docs.example.com/")``）。単なる正規表現文字列（例: ``.*docs\.example\.com.*``）はGroovy式として ``Boolean`` を返さないため、条件として機能しません。正規表現を使う場合はGroovyの ``String#matches`` を利用します。
- ``boostExpr`` は数値を返す必要があります。結果は ``float`` に変換され、0より大きい場合にのみブーストが適用されます。

.. note::

   式の中で参照できる主なフィールド変数: ``url``、``title``、``content``、``content_length``、``last_modified`` など。
   ``click_count`` と ``favorite_count`` は、それぞれ ``indexer.click.count.enabled`` /
   ``indexer.favorite.count.enabled``（いずれもデフォルトで有効）の場合に参照できます。
   ``now - 7d`` のようなOpenSearchの日付計算構文はGroovyでは使用できません。

条件式（``urlExpr``）の例
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 条件式
     - 説明
   * - ``url.startsWith("https://docs.example.com/")``
     - 指定したURLで始まるドキュメントを対象にする
   * - ``url.matches("https://www\\.example\\.com/.*")``
     - 正規表現（Groovyの ``String#matches``）でURLを判定する
   * - ``title.contains("リリースノート")``
     - タイトルに特定の語を含むドキュメントを対象にする

ブースト値式（``boostExpr``）の例
---------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - ブースト値式
     - 説明
   * - ``3.0``
     - 固定値でブースト
   * - ``click_count * 0.1 + 1``
     - クリック数に応じてブースト
   * - ``Math.log(click_count + 1)``
     - クリック数に基づく対数スケールブースト

使用例
======

ドキュメントサイトのブースト
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

クリック数の多いコンテンツのブースト
------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://www.example.com/\")",
           "boostExpr": "click_count * 0.1 + 1",
           "sortOrder": 10
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-elevateword` - エレベートワードAPI
- :doc:`../../admin/boostdoc-guide` - ドキュメントブースト管理ガイド
