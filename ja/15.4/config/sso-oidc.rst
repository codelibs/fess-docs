==============================
OpenID ConnectによるSSO設定
==============================

概要
====

|Fess| では、OpenID Connect（OIDC）を使用したシングルサインオン（SSO）認証をサポートしています。
OpenID ConnectはOAuth 2.0を基盤とした認証プロトコルで、ID Token（JWT）を使用してユーザー認証を行います。
OpenID Connect認証を使用することで、OIDCプロバイダー（OP）で認証されたユーザー情報を |Fess| に連携できます。

OpenID Connect認証の仕組み
--------------------------

OpenID Connect認証では、|Fess| がRelying Party（RP）として動作し、外部のOpenIDプロバイダー（OP）と連携して認証を行います。

1. ユーザーが |Fess| のSSOエンドポイント（``/sso/``）にアクセス
2. |Fess| がOPの認可エンドポイントにリダイレクト
3. ユーザーがOPで認証を実行
4. OPが認可コードを |Fess| にリダイレクト
5. |Fess| が認可コードを使用してトークンエンドポイントからID Tokenを取得
6. |Fess| がID Token（JWT）を検証し、ユーザーをログイン

ロールベース検索との連携については、:doc:`security-role` を参照してください。

前提条件
========

OpenID Connect認証を設定する前に、以下の前提条件を確認してください。

- |Fess| 15.4 以降がインストールされていること
- OpenID Connect対応のプロバイダー（OP）が利用可能であること
- |Fess| がHTTPSでアクセス可能であること（本番環境では必須）
- OP側で |Fess| をクライアント（RP）として登録できる権限があること

対応するプロバイダーの例:

- Microsoft Entra ID（Azure AD）
- Google Workspace / Google Cloud Identity
- Okta
- Keycloak
- Auth0
- その他のOpenID Connect対応プロバイダー

基本設定
========

SSO機能の有効化
---------------

OpenID Connect認証を有効にするには、``app/WEB-INF/conf/system.properties`` に以下の設定を追加します。

::

    sso.type=oic

プロバイダー設定
----------------

OPから取得した情報を設定します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``oic.auth.server.url``
     - 認可エンドポイントURL
     - （必須）
   * - ``oic.token.server.url``
     - トークンエンドポイントURL
     - （必須）

.. note::
   これらのURLは、OPのDiscoveryエンドポイント（``/.well-known/openid-configuration``）から取得できます。

クライアント設定
----------------

OP側で登録したクライアント情報を設定します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``oic.client.id``
     - クライアントID
     - （必須）
   * - ``oic.client.secret``
     - クライアントシークレット
     - （必須）
   * - ``oic.scope``
     - 要求するスコープ
     - （必須）

.. note::
   スコープには少なくとも ``openid`` を含める必要があります。
   ユーザーのメールアドレスを取得する場合は ``openid email`` を指定します。

リダイレクトURL設定
-------------------

認証後のコールバックURLを設定します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``oic.redirect.url``
     - リダイレクトURL（コールバックURL）
     - ``{oic.base.url}/sso/``
   * - ``oic.base.url``
     - |Fess| のベースURL
     - ``http://localhost:8080``

.. note::
   ``oic.redirect.url`` を省略した場合、``oic.base.url`` から自動的に構成されます。
   本番環境では、``oic.base.url`` にHTTPSのURLを設定してください。

OP側での設定
============

OP側で |Fess| をクライアント（RP）として登録する際に、以下の情報を設定します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 設定値
   * - アプリケーションの種類
     - Webアプリケーション
   * - リダイレクトURI / コールバックURL
     - ``https://<Fessのホスト>/sso/``
   * - 許可するスコープ
     - ``openid`` および必要なスコープ（``email``, ``profile`` など）

OPから取得する情報
------------------

OPの設定画面またはDiscoveryエンドポイントから以下の情報を取得し、|Fess| の設定に使用します。

- **認可エンドポイント（Authorization Endpoint）**: ユーザー認証を開始するURL
- **トークンエンドポイント（Token Endpoint）**: トークンを取得するURL
- **クライアントID**: OPで発行されたクライアント識別子
- **クライアントシークレット**: クライアント認証に使用する秘密鍵

.. note::
   多くのOPでは、Discoveryエンドポイント（``https://<OP>/.well-known/openid-configuration``）から
   認可エンドポイントとトークンエンドポイントのURLを確認できます。

設定例
======

最小構成（検証環境向け）
------------------------

以下は、検証環境で動作確認を行うための最小限の設定例です。

::

    # SSO有効化
    sso.type=oic

    # プロバイダー設定（OPから取得した値を設定）
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # クライアント設定
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email

    # リダイレクトURL（検証環境）
    oic.redirect.url=http://localhost:8080/sso/

推奨構成（本番環境向け）
------------------------

以下は、本番環境で使用する際の推奨設定例です。

::

    # SSO有効化
    sso.type=oic

    # プロバイダー設定
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # クライアント設定
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email profile

    # ベースURL（本番環境ではHTTPSを使用）
    oic.base.url=https://fess.example.com

トラブルシューティング
======================

よくある問題と解決方法
----------------------

認証後に |Fess| に戻れない
~~~~~~~~~~~~~~~~~~~~~~~~~~

- OP側のリダイレクトURIが正しく設定されているか確認してください
- ``oic.redirect.url`` または ``oic.base.url`` の値がOP側の設定と一致しているか確認してください
- プロトコル（HTTP/HTTPS）が一致しているか確認してください

認証エラーが発生する
~~~~~~~~~~~~~~~~~~~~

- クライアントIDとクライアントシークレットが正しく設定されているか確認してください
- スコープに ``openid`` が含まれているか確認してください
- 認可エンドポイントURLとトークンエンドポイントURLが正しいか確認してください

ユーザー情報が取得できない
~~~~~~~~~~~~~~~~~~~~~~~~~~

- スコープに必要な権限（``email``, ``profile`` など）が含まれているか確認してください
- OP側でクライアントに必要なスコープが許可されているか確認してください

デバッグ設定
------------

問題を調査する際は、|Fess| のログレベルを調整することで、OpenID Connect関連の詳細なログを出力できます。

``app/WEB-INF/classes/log4j2.xml`` で、以下のロガーを追加してログレベルを変更できます。

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

参考情報
========

- :doc:`security-role` - ロールベース検索の設定について
- :doc:`sso-saml` - SAML認証によるSSO設定について
