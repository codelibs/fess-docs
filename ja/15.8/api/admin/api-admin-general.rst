==========================
General API
==========================

概要
====

General APIは、|Fess| の一般設定（システム全般に関わる設定）を管理するためのAPIです。
クロール、ログ、検索結果の表示、サジェスト、ログの保持期間、通知、認証（LDAP / SSO）、
クラウドストレージ連携などの設定を、取得・更新できます。これらの設定は、管理画面の
「全般」設定（:doc:`../../admin/general-guide`）に対応します。

ベースURL
=========

::

    /api/admin/general

このAPIへのアクセスには ``Radmin-api`` 権限を持つアクセストークンが必要です。
認証方法の詳細は :doc:`api-admin-overview` を参照してください。

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

このエンドポイントはクエリパラメーターを受け付けません。

レスポンス
----------

``response.setting`` に、現在の一般設定が含まれます。レスポンスには更新可能なすべての
設定フィールドが含まれますが、以下の例では代表的なフィールドのみを抜粋しています。
オン/オフ設定は ``"true"`` / ``"false"`` の文字列で、日数やスレッド数などは数値で
表現されます。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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
   含まれます。全フィールドは管理画面の「全般」設定ページを参照してください。

.. note::

   セキュリティ上の理由から、認証情報を含むフィールドはレスポンスにそのままの値では
   含まれません。

   - LDAP管理者パスワード ``ldapAdminSecurityCredentials`` は常に ``null`` で
     返されます。
   - その他のシークレット（``storageAccessKey`` / ``storageSecretKey`` /
     ``oicClientId`` / ``oicClientSecret`` / ``spnegoPreauthPassword`` /
     ``entraidClientId`` / ``entraidClientSecret``）は、設定されている場合は
     ``"**********"`` でマスクされ、設定されていない場合は空文字列（``""``）で
     返されます。

一般設定更新
============

リクエスト
----------

::

    PUT /api/admin/general
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

更新は部分更新（merge）として処理されます。サーバーは現在の設定値を読み込んだうえで、
リクエストに含まれる ``null`` 以外のフィールドのみを上書きします。リクエストに含まれない
フィールドや ``null`` のフィールドは、既存の値が維持されます。

.. warning::

   次の4つのフィールドは必須であり、**すべての** PUTリクエストに必ず含める必要が
   あります（部分更新の場合も同様です）。

   - ``dayForCleanup``
   - ``crawlingThreadCount``
   - ``failureCountThreshold``
   - ``csvFileEncoding``

   いずれかが欠けるとバリデーションに失敗し、API は HTTP 400 で ``status: 1`` と
   エラー ``message`` を返します。送信した値で既存の設定が上書きされるため、値を
   変更したくない場合は、事前に ``GET`` で取得した現在の値をそのまま指定してください。
   上記以外のフィールドは任意で、省略した場合は既存の値が維持されます。

.. note::

   数値フィールドは型および範囲のバリデーションが行われます。整数として解釈できない値や
   範囲外の値を送信するとバリデーションに失敗します（HTTP 400、``status: 1``）。各数値
   フィールドの有効範囲は下記のフィールド表に記載しています。

.. note::

   オン/オフ（``available`` 系）のフィールドでは、``"true"`` または ``"on"``
   （いずれも大文字小文字を区別しない）のみが有効化を意味します。それ以外の値
   （``"false"`` や空文字列など）を送信した場合は無効化（``false``）として扱われます。
   フィールドを省略（送信しない）した場合のみ既存の値が維持されます。
   なお ``GET`` のレスポンスでは、これらのフィールドは文字列 ``"true"`` / ``"false"``
   で返されます。

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

設定項目は多岐にわたります。代表的なフィールドを以下に示します（すべてのフィールドは
管理画面の「全般」設定に対応します）。オン/オフ設定は ``"true"`` / ``"false"`` の文字列で
指定します。

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
     - クロール済みドキュメントを保持する日数（-1=クリーンアップ無効。指定範囲: -1〜1000）
   * - ``crawlingThreadCount``
     - はい
     - クロールに使用するスレッド数（指定範囲: 0〜100）
   * - ``failureCountThreshold``
     - はい
     - URLのクロールを停止する失敗回数のしきい値（-1=無効。指定範囲: -1〜10000）
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
     - 検索ログを保持する日数（-1=無効。指定範囲: -1〜100000）
   * - ``purgeJobLogDay``
     - いいえ
     - ジョブログを保持する日数（-1=無効。指定範囲: -1〜100000）
   * - ``purgeUserInfoDay``
     - いいえ
     - ユーザー情報を保持する日数（-1=無効。指定範囲: -1〜100000）
   * - ``purgeSuggestSearchLogDay``
     - いいえ
     - サジェスト検索ログを保持する日数（0=無効。指定範囲: 0〜100000）
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
このAPIで管理します。代表的なフィールドを以下に示します（すべてのフィールドは
管理画面の「全般」設定に対応します）。

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
     - ストレージタイプ（``auto`` / ``s3`` / ``gcs``）
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

更新に成功すると、``version`` と ``status`` のみが返されます（``id`` や ``created`` は
含まれません）。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

更新が失敗した場合（例: バリデーションエラー）、API は HTTP 400 を返し、レスポンスの
``status`` は 0 以外の値（バリデーションエラーの場合は ``1``）になり、``message`` に
エラーの詳細が含まれます。``status`` の値の一覧は
:doc:`api-admin-overview` を参照してください。

使用例
======

.. note::

   以下の例には必須フィールド（``dayForCleanup`` 、``crawlingThreadCount`` 、
   ``failureCountThreshold`` 、``csvFileEncoding``）が含まれています。これらは変更内容に
   関わらず常に送信する必要があるため、実運用では ``GET`` で取得した現在の値を含めて
   ください（以下の例ではデフォルト値を使用しています）。

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
