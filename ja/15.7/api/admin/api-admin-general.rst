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

   上記は代表的なフィールドのみを示した例です。実際のレスポンスの ``setting`` には、
   一般設定のすべてのフィールド（クロール・検索・通知・LDAP・SSO・ストレージ関連など）が
   含まれます。全フィールドは ``EditForm.java`` を参照してください。

.. note::

   セキュリティ上の理由から、認証情報を含むフィールドはレスポンスにそのままの値では
   含まれません。

   - LDAP管理者パスワード ``ldapAdminSecurityCredentials`` は常に ``null`` に
     置き換えられます。
   - その他のシークレット（``storageAccessKey`` / ``storageSecretKey`` /
     ``oicClientId`` / ``oicClientSecret`` / ``spnegoPreauthPassword`` /
     ``entraidClientId`` / ``entraidClientSecret``）は、設定済みの場合は
     マスク値 ``"**********"`` に置き換えられて返されます。

一般設定更新
============

リクエスト
----------

::

    PUT /api/admin/general
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

更新は部分更新（merge）として処理されます。現在の設定値に対してリクエストの値が
マージされ、リクエストに含まれないフィールド（``null`` のフィールド）は無視されて
既存の値が維持されます。

.. warning::

   次の4つのフィールドには ``@Required`` 制約があり、**すべての** PUTリクエストに
   必ず含める必要があります。省略するとバリデーションエラー（HTTP 400）になります。

   - ``dayForCleanup``
   - ``crawlingThreadCount``
   - ``failureCountThreshold``
   - ``csvFileEncoding``

   これらは部分更新の対象であっても省略できません。送信した値で既存の設定が
   上書きされるため、値を変更したくない場合は、事前に ``GET`` で取得した現在の値を
   そのまま指定してください。上記以外のフィールドは省略可能で、省略した場合は
   既存の値が維持されます。

.. note::

   数値フィールドには型・範囲のバリデーションがあり、整数として解釈できない値や
   範囲外の値を送信するとバリデーションエラー（HTTP 400）になります。

   - ``dayForCleanup``: ``-1`` 〜 ``1000``
   - ``crawlingThreadCount``: ``0`` 〜 ``100``
   - ``failureCountThreshold``: ``-1`` 〜 ``10000``
   - ``purgeSearchLogDay`` / ``purgeJobLogDay`` / ``purgeUserInfoDay``:
     ``-1`` 〜 ``100000``
   - ``purgeSuggestSearchLogDay``: ``0`` 〜 ``100000``

.. note::

   オン/オフ（``available`` 系）のフィールドでは、``"true"`` または ``"on"``
   （いずれも大文字小文字を区別しない）のみが有効化を意味します。それ以外の値
   （``"false"`` や空文字列など）を送信した場合は無効化（``false``）として扱われます。
   フィールドを省略（送信しない）した場合のみ既存の値が維持されます。
   なお ``GET`` のレスポンスでは、これらのフィールドは ``"true"`` / ``"false"`` の
   文字列で返されます。

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
（全フィールドは ``EditForm.java`` を参照してください。APIのリクエスト/レスポンス
ボディは ``EditForm`` を継承した ``EditBody`` ですが、フィールド定義は ``EditForm``
にあります）。``available`` 系のオン/オフ設定は ``"true"`` / ``"false"`` の文字列で
表現されます。

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
   * - ``appValue``
     - いいえ
     - アプリケーション固有の追加設定値
   * - ``virtualHostValue``
     - いいえ
     - バーチャルホスト設定（マルチテナント構成用）
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
   * - ``loginLink``
     - いいえ
     - 検索画面へのログインリンク表示の有効/無効
   * - ``thumbnail``
     - いいえ
     - サムネイル生成の有効/無効
   * - ``resultCollapsed``
     - いいえ
     - 類似ドキュメントの検索結果の折りたたみ表示の有効/無効
   * - ``ignoreFailureType``
     - いいえ
     - 無視するクロール失敗タイプ
   * - ``crawlingUserAgent``
     - いいえ
     - クロール時に送信するUser-Agent文字列
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
   * - ``searchUseBrowserLocale``
     - いいえ
     - 検索でブラウザのロケールを使用するかどうか
   * - ``ragLlmName``
     - いいえ
     - RAGで使用するLLMプロバイダー名
   * - ``llmLogLevel``
     - いいえ
     - LLM関連パッケージのログレベル

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
   * - ``ldapMemberofAttribute``
     - グループ所属を示すLDAP属性名
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

.. note::

   ``ldapAdminSecurityCredentials``、``storageAccessKey`` / ``storageSecretKey``、
   ``oicClientId`` / ``oicClientSecret``、``entraidClientId`` / ``entraidClientSecret``、
   ``spnegoPreauthPassword`` などのシークレット系フィールドは、マスク値
   ``"**********"`` をそのまま送信した場合、その値は更新されず、保存済みの値が
   維持されます。値を変更する場合のみ、実際の値を送信してください。

   この判定はアスタリスクを除いた文字列が空白かどうかで行われるため、空文字列
   （``""``）やアスタリスクのみの値を送信した場合も同様に更新されません。
   したがって、これらのシークレット系フィールドをAPIから空の値にクリアすることは
   できません。

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

.. note::

   PUTリクエストでは ``dayForCleanup``、``crawlingThreadCount``、
   ``failureCountThreshold``、``csvFileEncoding`` の4フィールドが必須のため、
   以下のすべての例にこれらを含めています。これらは送信した値で既存の設定を
   上書きするため、実際の運用では ``GET`` で取得した現在の値を指定してください
   （以下の例では既定値を示しています）。

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
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
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
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-systeminfo` - システム情報API
- :doc:`../../admin/general-guide` - 一般設定ガイド
