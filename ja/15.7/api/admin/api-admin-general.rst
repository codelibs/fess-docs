==========================
General API
==========================

概要
====

General APIは、|Fess| の一般設定を管理するためのAPIです。
システム全般に関わる設定の取得と更新を行えます。

ベースURL
=========

::

    /api/admin/general

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
     - 一般設定取得
   * - PUT
     - /
     - 一般設定更新

一般設定取得
============

リクエスト
----------

::

    GET /api/admin/general

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "crawlerDocumentMaxSize": "10485760",
          "crawlerDocumentMaxSiteLength": "50",
          "crawlerDocumentMaxFetcherSize": "3",
          "crawlerDocumentCrawlerThreadCount": "10",
          "crawlerDocumentMaxDepth": "-1",
          "crawlerDocumentMaxAccessCount": "100",
          "indexerThreadDumpEnabled": "true",
          "indexerUnprocessedDocumentSize": "1000",
          "indexerClickCountEnabled": "true",
          "indexerFavoriteCountEnabled": "true",
          "indexerWebfsMaxContentLength": "10485760",
          "indexerWebfsContentEncoding": "UTF-8",
          "queryReplaceTermWithPrefixQuery": "false",
          "queryMaxSearchResultOffset": "100000",
          "queryMaxPageSize": "1000",
          "queryDefaultPageSize": "20",
          "queryAdditionalDefaultQuery": "",
          "queryGeoEnabled": "false",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "suggestBadWord": "true",
          "suggestPopularWordSeedLength": "1",
          "suggestPopularWordTags": "user",
          "suggestPopularWordFields": "tags",
          "suggestPopularWordExcludeWordFields": "",
          "ldapInitialContextFactory": "com.sun.jndi.ldap.LdapCtxFactory",
          "ldapSecurityAuthentication": "simple",
          "ldapProviderUrl": "ldap://localhost:389",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapBindDn": "",
          "ldapBindPassword": "",
          "notificationLogin": "true",
          "notificationSearchTop": "true"
        }
      }
    }

一般設定更新
============

リクエスト
----------

::

    PUT /api/admin/general
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "crawlerDocumentMaxSize": "20971520",
      "crawlerDocumentMaxSiteLength": "100",
      "crawlerDocumentCrawlerThreadCount": "20",
      "queryMaxPageSize": "500",
      "queryDefaultPageSize": "50",
      "suggestSearchLog": "true",
      "suggestDocuments": "true",
      "suggestBadWord": "true",
      "notificationLogin": "false",
      "notificationSearchTop": "false"
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - フィールド
     - 説明
   * - ``crawlerDocumentMaxSize``
     - クロール対象ドキュメントの最大サイズ（バイト）
   * - ``crawlerDocumentMaxSiteLength``
     - クロール対象サイトの最大長
   * - ``crawlerDocumentMaxFetcherSize``
     - 最大フェッチャーサイズ
   * - ``crawlerDocumentCrawlerThreadCount``
     - クローラースレッド数
   * - ``crawlerDocumentMaxDepth``
     - クロールの最大深度（-1=無制限）
   * - ``crawlerDocumentMaxAccessCount``
     - 最大アクセス数
   * - ``indexerThreadDumpEnabled``
     - スレッドダンプ有効化
   * - ``indexerUnprocessedDocumentSize``
     - 未処理ドキュメント数
   * - ``indexerClickCountEnabled``
     - クリック数カウント有効化
   * - ``indexerFavoriteCountEnabled``
     - お気に入り数カウント有効化
   * - ``queryReplaceTermWithPrefixQuery``
     - 前方一致クエリへの変換
   * - ``queryMaxSearchResultOffset``
     - 検索結果の最大オフセット
   * - ``queryMaxPageSize``
     - 1ページあたりの最大件数
   * - ``queryDefaultPageSize``
     - 1ページあたりのデフォルト件数
   * - ``queryAdditionalDefaultQuery``
     - 追加デフォルトクエリ
   * - ``suggestSearchLog``
     - 検索ログからのサジェスト有効化
   * - ``suggestDocuments``
     - ドキュメントからのサジェスト有効化
   * - ``suggestBadWord``
     - NGワードフィルタ有効化
   * - ``ldapProviderUrl``
     - LDAP接続URL
   * - ``ldapBaseDn``
     - LDAPベースDN
   * - ``notificationLogin``
     - ログイン通知
   * - ``notificationSearchTop``
     - 検索トップ通知

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

クローラー設定の更新
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "crawlerDocumentMaxSize": "52428800",
           "crawlerDocumentCrawlerThreadCount": "15",
           "crawlerDocumentMaxAccessCount": "1000"
         }'

検索設定の更新
--------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "queryMaxPageSize": "1000",
           "queryDefaultPageSize": "50",
           "queryMaxSearchResultOffset": "50000"
         }'

サジェスト設定の更新
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestSearchLog": "true",
           "suggestDocuments": "true",
           "suggestBadWord": "true"
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-systeminfo` - システム情報API
- :doc:`../../admin/general-guide` - 一般設定ガイド
