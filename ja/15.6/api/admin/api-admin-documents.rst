==========================
Documents API
==========================

概要
====

Documents APIは、|Fess| のインデックス内のドキュメントを管理するためのAPIです。
ドキュメントの一括削除、更新、検索などの操作を行えます。

ベースURL
=========

::

    /api/admin/documents

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - DELETE
     - /
     - ドキュメント削除（クエリ指定）
   * - DELETE
     - /{id}
     - ドキュメント削除（ID指定）

クエリ指定でのドキュメント削除
==============================

検索クエリに一致するドキュメントを一括削除します。

リクエスト
----------

::

    DELETE /api/admin/documents

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``q``
     - String
     - はい
     - 削除対象の検索クエリ

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deleted": 150
      }
    }

使用例
~~~~~~

.. code-block:: bash

    # 特定のサイトのドキュメントを削除
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 古いドキュメントを削除
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO 2023-01-01]" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # ラベル指定でドキュメントを削除
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=label:old_label" \
         -H "Authorization: Bearer YOUR_TOKEN"

ID指定でのドキュメント削除
==========================

ドキュメントIDを指定して削除します。

リクエスト
----------

::

    DELETE /api/admin/documents/{id}

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``id``
     - String
     - はい
     - ドキュメントID（パスパラメーター）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

使用例
~~~~~~

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/documents/doc_id_12345" \
         -H "Authorization: Bearer YOUR_TOKEN"

クエリ構文
==========

削除クエリには、|Fess| の標準検索構文が使用できます。

基本的なクエリ
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - クエリ例
     - 説明
   * - ``url:example.com``
     - URLに"example.com"を含むドキュメント
   * - ``url:https://example.com/*``
     - 特定のプレフィックスを持つURL
   * - ``host:example.com``
     - 特定のホストのドキュメント
   * - ``title:keyword``
     - タイトルにキーワードを含むドキュメント
   * - ``content:keyword``
     - 本文にキーワードを含むドキュメント
   * - ``label:mylabel``
     - 特定のラベルを持つドキュメント

日付範囲クエリ
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - クエリ例
     - 説明
   * - ``lastModified:[2023-01-01 TO 2023-12-31]``
     - 指定期間内に更新されたドキュメント
   * - ``lastModified:[* TO 2023-01-01]``
     - 指定日より前に更新されたドキュメント
   * - ``created:[2024-01-01 TO *]``
     - 指定日以降に作成されたドキュメント

複合クエリ
----------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - クエリ例
     - 説明
   * - ``url:example.com AND label:blog``
     - AND条件
   * - ``url:example.com OR url:sample.com``
     - OR条件
   * - ``NOT url:example.com``
     - NOT条件
   * - ``(url:example.com OR url:sample.com) AND label:news``
     - グループ化

注意事項
========

削除操作の注意
--------------

.. warning::
   削除操作は取り消せません。本番環境で実行する前に、必ずテスト環境で確認してください。

- 大量のドキュメントを削除する場合、処理に時間がかかることがあります
- 削除中はインデックスのパフォーマンスに影響が出る可能性があります
- 削除後、検索結果に反映されるまで少し時間がかかる場合があります

推奨プラクティス
----------------

1. **削除前の確認**: 同じクエリで検索APIを使用し、削除対象を確認
2. **段階的な削除**: 大量削除は複数回に分けて実行
3. **バックアップ**: 重要なデータは事前にバックアップ

使用例
======

サイト全体の再クロール準備
--------------------------

.. code-block:: bash

    # 特定サイトの古いドキュメントを削除
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=host:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # クロールジョブを開始
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

古いドキュメントのクリーンアップ
--------------------------------

.. code-block:: bash

    # 1年以上更新されていないドキュメントを削除
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO now-1y]" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-crawlinginfo` - クロール情報API
- :doc:`../../admin/searchlist-guide` - 検索一覧管理ガイド
