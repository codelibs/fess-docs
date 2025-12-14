===============================
Microsoft Entra IDによるSSO設定
===============================

概要
====

|Fess| では、Microsoft Entra ID（旧Azure AD）を使用したシングルサインオン（SSO）認証をサポートしています。
Entra ID認証を使用することで、Microsoft 365環境のユーザー情報やグループ情報を |Fess| のロールベース検索と連携できます。

Entra ID認証の仕組み
--------------------

Entra ID認証では、|Fess| がOAuth 2.0/OpenID Connectのクライアントとして動作し、Microsoft Entra IDと連携して認証を行います。

1. ユーザーが |Fess| のSSOエンドポイント（``/sso/``）にアクセス
2. |Fess| がEntra IDの認可エンドポイントにリダイレクト
3. ユーザーがEntra IDで認証（Microsoftサインイン）
4. Entra IDが認可コードを |Fess| にリダイレクト
5. |Fess| が認可コードを使用してアクセストークンを取得
6. |Fess| がMicrosoft Graph APIを使用してユーザーのグループ・ロール情報を取得
7. ユーザーをログインし、グループ情報をロールベース検索に適用

ロールベース検索との連携については、:doc:`security-role` を参照してください。

前提条件
========

Entra ID認証を設定する前に、以下の前提条件を確認してください。

- |Fess| 15.4 以降がインストールされていること
- Microsoft Entra ID（Azure AD）テナントが利用可能であること
- |Fess| がHTTPSでアクセス可能であること（本番環境では必須）
- Entra ID側でアプリケーションを登録できる権限があること

基本設定
========

SSO機能の有効化
---------------

Entra ID認証を有効にするには、``app/WEB-INF/conf/system.properties`` に以下の設定を追加します。

::

    sso.type=entraid

必須設定
--------

Entra IDから取得した情報を設定します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``entraid.tenant``
     - テナントID（例: ``xxx.onmicrosoft.com``）
     - （必須）
   * - ``entraid.client.id``
     - アプリケーション（クライアント）ID
     - （必須）
   * - ``entraid.client.secret``
     - クライアントシークレットの値
     - （必須）
   * - ``entraid.reply.url``
     - リダイレクトURI（コールバックURL）
     - リクエストURLを使用

.. note::
   ``entraid.*`` プレフィックスの代わりに、レガシーの ``aad.*`` プレフィックスも使用できます（後方互換性）。

オプション設定
--------------

必要に応じて以下の設定を追加できます。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``entraid.authority``
     - 認証サーバーURL
     - ``https://login.microsoftonline.com/``
   * - ``entraid.state.ttl``
     - State有効期限（秒）
     - ``3600``
   * - ``entraid.default.groups``
     - デフォルトグループ（カンマ区切り）
     - （なし）
   * - ``entraid.default.roles``
     - デフォルトロール（カンマ区切り）
     - （なし）

Entra ID側での設定
==================

Azure Portalでのアプリ登録
--------------------------

1. `Azure Portal <https://portal.azure.com/>`_ にサインイン

2. **Microsoft Entra ID** を選択

3. 左メニューの **管理** → **アプリの登録** → **新規登録** をクリック

4. アプリケーションを登録:

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - 設定項目
        - 設定値
      * - 名前
        - 任意の名前（例: Fess SSO）
      * - サポートされているアカウントの種類
        - 「この組織ディレクトリのみに含まれるアカウント」
      * - プラットフォームの選択
        - Web
      * - リダイレクトURI
        - ``https://<Fessのホスト>/sso/``

5. **登録** をクリック

クライアントシークレットの作成
------------------------------

1. アプリの詳細ページで **証明書とシークレット** をクリック

2. **新しいクライアントシークレット** をクリック

3. 説明と有効期限を設定して **追加** をクリック

4. 生成された **値** をコピーして保存（この値は再表示されません）

.. warning::
   クライアントシークレットの値は、作成直後のみ表示されます。
   別の画面に遷移する前に必ず記録してください。

APIアクセス許可の設定
---------------------

1. 左メニューの **APIのアクセス許可** をクリック

2. **アクセス許可の追加** をクリック

3. **Microsoft Graph** を選択

4. **委任されたアクセス許可** を選択

5. 以下のアクセス許可を追加:

   - ``Group.Read.All`` - ユーザーのグループ情報を取得するために必要

6. **アクセス許可の追加** をクリック

7. **「<テナント名>に管理者の同意を与えます」** をクリック

.. note::
   管理者の同意は、テナント管理者権限が必要です。

取得する情報
------------

以下の情報をFessの設定に使用します。

- **アプリケーション（クライアント）ID**: 概要ページの「アプリケーション (クライアント) ID」
- **テナントID**: 概要ページの「ディレクトリ (テナント) ID」または ``xxx.onmicrosoft.com`` 形式
- **クライアントシークレットの値**: 証明書とシークレットで作成した値

グループ・ロールマッピング
==========================

Entra ID認証では、Microsoft Graph APIを使用してユーザーが所属するグループおよびロールを自動的に取得します。
取得したグループIDおよびグループ名は、|Fess| のロールベース検索に使用できます。

ネストされたグループ
--------------------

|Fess| は、ユーザーが直接所属するグループだけでなく、そのグループが所属する親グループ（ネストされたグループ）も再帰的に取得します。
この処理はログイン後に非同期で実行されるため、ログイン時間への影響を最小限に抑えています。

デフォルトグループの設定
------------------------

すべてのEntra IDユーザーに共通のグループを付与する場合:

::

    entraid.default.groups=authenticated_users,entra_users

設定例
======

最小構成（検証環境向け）
------------------------

以下は、検証環境で動作確認を行うための最小限の設定例です。

::

    # SSO有効化
    sso.type=entraid

    # Entra ID設定
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

推奨構成（本番環境向け）
------------------------

以下は、本番環境で使用する際の推奨設定例です。

::

    # SSO有効化
    sso.type=entraid

    # Entra ID設定
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # デフォルトグループ（オプション）
    entraid.default.groups=authenticated_users

レガシー設定（後方互換性）
--------------------------

以前のバージョンとの互換性のため、``aad.*`` プレフィックスも使用できます。

::

    # SSO有効化
    sso.type=entraid

    # レガシー設定キー
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

トラブルシューティング
======================

よくある問題と解決方法
----------------------

認証後にFessに戻れない
~~~~~~~~~~~~~~~~~~~~~~

- Azure Portalのアプリ登録でリダイレクトURIが正しく設定されているか確認してください
- ``entraid.reply.url`` の値がAzure Portalの設定と完全に一致しているか確認してください
- プロトコル（HTTP/HTTPS）が一致しているか確認してください
- リダイレクトURIの末尾に ``/`` が含まれているか確認してください

認証エラーが発生する
~~~~~~~~~~~~~~~~~~~~

- テナントID、クライアントID、クライアントシークレットが正しく設定されているか確認してください
- クライアントシークレットの有効期限が切れていないか確認してください
- APIアクセス許可に管理者の同意が与えられているか確認してください

グループ情報が取得できない
~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``Group.Read.All`` のアクセス許可が付与されているか確認してください
- 管理者の同意が与えられているか確認してください
- ユーザーがEntra ID上でグループに所属しているか確認してください

デバッグ設定
------------

問題を調査する際は、|Fess| のログレベルを調整することで、Entra ID関連の詳細なログを出力できます。

``app/WEB-INF/classes/log4j2.xml`` で、以下のロガーを追加してログレベルを変更できます。

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

参考情報
========

- :doc:`security-role` - ロールベース検索の設定について
- :doc:`sso-saml` - SAML認証によるSSO設定について
- :doc:`sso-oidc` - OpenID Connect認証によるSSO設定について
