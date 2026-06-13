==========================
CrawlingInfo API
==========================

概要
====

CrawlingInfo APIは、|Fess| のクロール情報（クロールセッション）を参照・管理するためのAPIです。
クロールセッションの一覧取得、個別取得、削除などを操作できます。

ベースURL
=========

::

    /api/admin/crawlinginfo

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /logs
     - クロール情報一覧取得
   * - GET
     - /log/{id}
     - クロール情報取得
   * - DELETE
     - /log/{id}
     - クロール情報削除
   * - DELETE
     - /all
     - 古いクロールセッション一括削除

クロール情報一覧取得
====================

リクエスト
----------

::

    GET /api/admin/crawlinginfo/logs

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
     - 1ページあたりの件数
   * - ``page``
     - Integer
     - いいえ
     - ページ番号
   * - ``sessionId``
     - String
     - いいえ
     - セッションIDフィルター

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "sessionId": "20250129100000",
            "name": "Default Crawler",
            "expiredTime": "1738200000000",
            "createdTime": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "sessionId": "20250128100000",
            "name": "Default Crawler",
            "expiredTime": "1738113600000",
            "createdTime": 1738022400000
          }
        ],
        "total": 10
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
     - クロール情報ID
   * - ``sessionId``
     - セッションID
   * - ``name``
     - セッション名
   * - ``expiredTime``
     - 有効期限
   * - ``createdTime``
     - 作成時刻（エポックミリ秒）

クロール情報取得
================

リクエスト
----------

::

    GET /api/admin/crawlinginfo/log/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "crawling_info_id_1",
          "sessionId": "20250129100000",
          "name": "Default Crawler",
          "expiredTime": "1738200000000",
          "createdTime": 1738108800000
        }
      }
    }

クロール情報削除
================

リクエスト
----------

::

    DELETE /api/admin/crawlinginfo/log/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

古いクロールセッション一括削除
==============================

実行中のセッションを除く古いクロールセッションをまとめて削除します。

リクエスト
----------

::

    DELETE /api/admin/crawlinginfo/all

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

使用例
======

クロール情報一覧の取得
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

特定セッションでフィルター
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?sessionId=20250129100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

クロール情報の取得
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

クロール情報の削除
------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

古いセッションの一括削除
------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-failureurl` - 障害URL API
- :doc:`api-admin-joblog` - ジョブログAPI
- :doc:`../../admin/crawlinginfo-guide` - クロール情報ガイド
