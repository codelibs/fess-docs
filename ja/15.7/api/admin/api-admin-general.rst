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
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "incrementalCrawling": "true",
          "dayForCleanup": -1,
          "crawlingThreadCount": 5,
          "searchLog": "true",
          "userInfo": "true",
          "userFavorite": "false",
          "webApiJson": "true",
          "defaultLabelValue": "",
          "defaultSortValue": "",
          "appendQueryParameter": "false",
          "loginRequired": "false",
          "thumbnail": "true",
          "failureCountThreshold": -1,
          "popularWord": "true",
          "csvFileEncoding": "UTF-8",
          "purgeSearchLogDay": 30,
          "purgeJobLogDay": 30,
          "purgeUserInfoDay": 30,
          "purgeSuggestSearchLogDay": 30,
          "notificationTo": "",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "ldapProviderUrl": "ldap://localhost:389/",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapAdminSecurityPrincipal": "cn=admin,dc=example,dc=com",
          "ldapAdminSecurityCredentials": null,
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   セキュリティ上の理由から、LDAP管理者のパスワードである ``ldapAdminSecurityCredentials``
   はレスポンスでは常に ``null`` に置き換えられます（ソース:
   ``ApiAdminGeneralAction.java:71``）。

一般設定更新
============

リクエスト
----------

::

    PUT /api/admin/general
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

更新は部分更新（merge）として処理されます。リクエストに含まれないフィールドは
既存の値が維持され、``null`` のフィールドは無視されます（ソース:
``ApiAdminGeneralAction.java:84-90``）。

.. code-block:: json

    {
      "incrementalCrawling": "true",
      "dayForCleanup": -1,
      "crawlingThreadCount": 10,
      "failureCountThreshold": 100,
      "csvFileEncoding": "UTF-8",
      "popularWord": "true"
    }

主なフィールド
~~~~~~~~~~~~~~

設定項目は多岐にわたります。代表的なフィールドを以下に示します
（全フィールドは ``EditForm.java`` を参照）。``available`` 系のオン/オフ設定は
``"true"`` / ``"false"`` の文字列で表現されます。

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - フィールド
     - 必須
     - 説明
   * - ``incrementalCrawling``
     - いいえ
     - 増分クロールの有効/無効
   * - ``dayForCleanup``
     - はい
     - クロール済みドキュメントを保持する日数（-1=クリーンアップ無効）
   * - ``crawlingThreadCount``
     - はい
     - クロールに使用するスレッド数
   * - ``failureCountThreshold``
     - はい
     - URLのクロールを停止する失敗回数のしきい値（-1=無効）
   * - ``csvFileEncoding``
     - はい
     - CSVエクスポートのエンコーディング
   * - ``searchLog``
     - いいえ
     - 検索クエリログの有効/無効
   * - ``userInfo``
     - いいえ
     - ユーザー情報の記録の有効/無効
   * - ``userFavorite``
     - いいえ
     - お気に入り機能の有効/無効
   * - ``webApiJson``
     - いいえ
     - JSON Web APIの有効/無効
   * - ``popularWord``
     - いいえ
     - 人気ワードの集計・表示の有効/無効
   * - ``defaultLabelValue``
     - いいえ
     - 既定のラベル値
   * - ``defaultSortValue``
     - いいえ
     - 既定のソート順
   * - ``appendQueryParameter``
     - いいえ
     - 検索結果URLへのクエリパラメーター付与
   * - ``loginRequired``
     - いいえ
     - 検索にログインを必須とするか
   * - ``thumbnail``
     - いいえ
     - サムネイル生成の有効/無効
   * - ``ignoreFailureType``
     - いいえ
     - 無視するクロール失敗タイプ
   * - ``purgeSearchLogDay``
     - いいえ
     - 検索ログを保持する日数（-1=無効）
   * - ``purgeJobLogDay``
     - いいえ
     - ジョブログを保持する日数（-1=無効）
   * - ``purgeUserInfoDay``
     - いいえ
     - ユーザー情報を保持する日数（-1=無効）
   * - ``purgeSuggestSearchLogDay``
     - いいえ
     - サジェスト検索ログを保持する日数（0=無効）
   * - ``purgeByBots``
     - いいえ
     - 検索ログを破棄する対象のボットUser-Agent
   * - ``notificationTo``
     - いいえ
     - システム通知の送信先メールアドレス
   * - ``notificationLogin``
     - いいえ
     - ログインページに表示する通知メッセージ
   * - ``notificationSearchTop``
     - いいえ
     - 検索トップページに表示する通知メッセージ
   * - ``notificationAdvanceSearch``
     - いいえ
     - 詳細検索ページに表示する通知メッセージ
   * - ``suggestSearchLog``
     - いいえ
     - 検索ログからのサジェストの有効/無効
   * - ``suggestDocuments``
     - いいえ
     - ドキュメントからのサジェストの有効/無効
   * - ``logLevel``
     - いいえ
     - システムログのログレベル
   * - ``logNotificationEnabled``
     - いいえ
     - ERROR/WARNログの通知の有効/無効
   * - ``logNotificationLevel``
     - いいえ
     - ログ通知レベル
   * - ``slackWebhookUrls``
     - いいえ
     - 通知用のSlack Webhook URL
   * - ``googleChatWebhookUrls``
     - いいえ
     - 通知用のGoogle Chat Webhook URL

認証関連フィールド
~~~~~~~~~~~~~~~~~~

LDAPおよびSSO（OpenID Connect、SAML、SPNEGO、Entra ID）に関する設定も
このAPIで管理します。代表的なフィールドを以下に示します
（全フィールドは ``EditForm.java`` を参照）。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - フィールド
     - 説明
   * - ``ldapProviderUrl``
     - LDAP接続URL
   * - ``ldapBaseDn``
     - LDAPベースDN
   * - ``ldapSecurityPrincipal``
     - LDAPバインド用のセキュリティプリンシパル
   * - ``ldapAdminSecurityPrincipal``
     - LDAP管理操作用のセキュリティプリンシパル
   * - ``ldapAdminSecurityCredentials``
     - LDAP管理者パスワード（レスポンスでは ``null`` に置換）
   * - ``ldapAccountFilter`` / ``ldapGroupFilter``
     - ユーザー/グループ検索フィルター
   * - ``ssoType``
     - SSOタイプ（``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``）
   * - ``oicClientId`` / ``oicClientSecret`` / ``oicAuthServerUrl`` 他
     - OpenID Connectの設定
   * - ``samlIdpEntityid`` / ``samlSpEntityid`` 他
     - SAMLの設定
   * - ``spnegoKrb5Conf`` / ``spnegoLoginConf`` 他
     - SPNEGOの設定
   * - ``entraidClientId`` / ``entraidTenant`` 他
     - Microsoft Entra IDの設定

ストレージ関連フィールド
~~~~~~~~~~~~~~~~~~~~~~~~

クラウドストレージ（S3 / GCS）連携の設定も管理できます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - フィールド
     - 説明
   * - ``storageType``
     - ストレージタイプ（``s3`` / ``gcs`` / ``auto``）
   * - ``storageEndpoint``
     - ストレージのエンドポイントURL
   * - ``storageAccessKey`` / ``storageSecretKey``
     - 認証用のアクセスキー/シークレットキー
   * - ``storageBucket``
     - バケット名
   * - ``storageRegion``
     - S3のリージョン
   * - ``storageProjectId`` / ``storageCredentialsPath``
     - GCSのプロジェクトID / 認証情報ファイルパス

レスポンス
----------

更新成功時は ``status`` のみが返されます（``id`` や ``created`` は含まれません）。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

使用例
======

クロール設定の更新
------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "incrementalCrawling": "true",
           "crawlingThreadCount": 10,
           "failureCountThreshold": 100,
           "dayForCleanup": -1,
           "csvFileEncoding": "UTF-8"
         }'

ログ保持期間の更新
------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "purgeSearchLogDay": 90,
           "purgeJobLogDay": 90,
           "purgeUserInfoDay": 90
         }'

サジェスト設定の更新
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-systeminfo` - システム情報API
- :doc:`../../admin/general-guide` - 一般設定ガイド
