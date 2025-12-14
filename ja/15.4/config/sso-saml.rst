======================
SAML認証によるSSO設定
======================

概要
====

|Fess| では、SAML（Security Assertion Markup Language）2.0 を使用したシングルサインオン（SSO）認証をサポートしています。
SAML認証を使用することで、IdP（Identity Provider）で認証されたユーザー情報を |Fess| に連携し、ロールベース検索と組み合わせることで、ユーザーの権限に応じた検索結果の出し分けが可能になります。

SAML認証の仕組み
----------------

SAML認証では、|Fess| がSP（Service Provider）として動作し、外部のIdPと連携して認証を行います。

1. ユーザーが |Fess| のSSOエンドポイント（``/sso/``）にアクセス
2. |Fess| がIdPに認証リクエストをリダイレクト
3. ユーザーがIdPで認証を実行
4. IdPがSAMLアサーションを |Fess| に送信
5. |Fess| がアサーションを検証し、ユーザーをログイン

ロールベース検索との連携については、:doc:`security-role` を参照してください。

前提条件
========

SAML認証を設定する前に、以下の前提条件を確認してください。

- |Fess| 14.0 以降がインストールされていること
- SAML 2.0 対応のIdP（Identity Provider）が利用可能であること
- |Fess| がHTTPSでアクセス可能であること（本番環境では必須）
- IdP側で |Fess| をSPとして登録できる権限があること

対応するIdPの例:

- Microsoft Entra ID（Azure AD）
- Okta
- Google Workspace
- Keycloak
- OneLogin
- その他のSAML 2.0対応IdP

基本設定
========

SSO機能の有効化
---------------

SAML認証を有効にするには、``app/WEB-INF/conf/system.properties`` に以下の設定を追加します。

::

    sso.type=saml

SP（Service Provider）設定
--------------------------

|Fess| をSPとして設定するには、SP Base URLを指定します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.sp.base.url``
     - SPのベースURL
     - （必須）

この設定により、以下のエンドポイントが自動的に構成されます。

- **Entity ID**: ``{base_url}/sso/metadata``
- **ACS URL**: ``{base_url}/sso/``
- **SLO URL**: ``{base_url}/sso/logout``

設定例::

    saml.sp.base.url=https://fess.example.com

個別URL設定
~~~~~~~~~~~

Base URLを使用せず、個別にURLを指定することもできます。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.sp.entityid``
     - SPのEntity ID
     - （個別設定時必須）
   * - ``saml.sp.assertion_consumer_service.url``
     - Assertion Consumer Service URL
     - （個別設定時必須）
   * - ``saml.sp.single_logout_service.url``
     - Single Logout Service URL
     - （オプション）

IdP（Identity Provider）設定
----------------------------

IdPから取得した情報を設定します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.idp.entityid``
     - IdPのEntity ID
     - （必須）
   * - ``saml.idp.single_sign_on_service.url``
     - IdPのSSOサービスURL
     - （必須）
   * - ``saml.idp.x509cert``
     - IdPの署名用X.509証明書（Base64エンコード、改行なし）
     - （必須）
   * - ``saml.idp.single_logout_service.url``
     - IdPのSLOサービスURL
     - （オプション）

.. note::
   ``saml.idp.x509cert`` には、証明書のBase64エンコードされた内容を改行なしの1行で指定します。
   ``-----BEGIN CERTIFICATE-----`` と ``-----END CERTIFICATE-----`` の行は含めないでください。

SPメタデータの取得
------------------

|Fess| を起動すると、``/sso/metadata`` エンドポイントでSPメタデータをXML形式で取得できます。

::

    https://fess.example.com/sso/metadata

このメタデータをIdPにインポートするか、メタデータの内容を参考にIdP側でSPを手動登録してください。

.. note::
   メタデータを取得するには、先に基本的なSAML設定（``sso.type=saml`` と ``saml.sp.base.url``）を完了し、|Fess| を起動しておく必要があります。

IdP側での設定
=============

IdP側で |Fess| をSPとして登録する際に、以下の情報を設定します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 設定値
   * - ACS URL / Reply URL
     - ``https://<Fessのホスト>/sso/``
   * - Entity ID / Audience URI
     - ``https://<Fessのホスト>/sso/metadata``
   * - Name ID Format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`` （推奨）

IdPから取得する情報
-------------------

IdPの設定画面またはメタデータから以下の情報を取得し、|Fess| の設定に使用します。

- **IdP Entity ID**: IdPを識別するためのURI
- **SSO URL（HTTP-Redirect）**: シングルサインオンのエンドポイントURL
- **X.509証明書**: SAMLアサーションの署名検証に使用する公開鍵証明書

ユーザー属性マッピング
======================

SAMLアサーションから取得したユーザー属性を、|Fess| のグループやロールにマッピングできます。

グループ属性の設定
------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.attribute.group.name``
     - グループ情報を含む属性名
     - ``memberOf``
   * - ``saml.default.groups``
     - デフォルトグループ（カンマ区切り）
     - （なし）

設定例::

    saml.attribute.group.name=groups
    saml.default.groups=user

ロール属性の設定
----------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.attribute.role.name``
     - ロール情報を含む属性名
     - （なし）
   * - ``saml.default.roles``
     - デフォルトロール（カンマ区切り）
     - （なし）

設定例::

    saml.attribute.role.name=roles
    saml.default.roles=viewer

.. note::
   IdPから属性が取得できない場合は、デフォルト値が使用されます。
   ロールベース検索を使用する場合は、適切なグループまたはロールを設定してください。

セキュリティ設定
================

本番環境では、以下のセキュリティ設定を有効にすることを推奨します。

署名の設定
----------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.security.authnrequest_signed``
     - 認証リクエストに署名する
     - ``false``
   * - ``saml.security.want_messages_signed``
     - メッセージの署名を要求する
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - アサーションの署名を要求する
     - ``false``
   * - ``saml.security.logoutrequest_signed``
     - ログアウトリクエストに署名する
     - ``false``
   * - ``saml.security.logoutresponse_signed``
     - ログアウトレスポンスに署名する
     - ``false``

.. warning::
   デフォルトではセキュリティ機能が無効になっています。
   本番環境では、少なくとも ``saml.security.want_assertions_signed=true`` を設定することを強く推奨します。

暗号化の設定
------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.security.want_assertions_encrypted``
     - アサーションの暗号化を要求する
     - ``false``
   * - ``saml.security.want_nameid_encrypted``
     - NameIDの暗号化を要求する
     - ``false``

その他のセキュリティ設定
------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.security.strict``
     - 厳密モード（検証を厳密に行う）
     - ``true``
   * - ``saml.security.signature_algorithm``
     - 署名アルゴリズム
     - ``http://www.w3.org/2000/09/xmldsig#rsa-sha1``
   * - ``saml.sp.nameidformat``
     - NameIDフォーマット
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

設定例
======

最小構成（検証環境向け）
------------------------

以下は、検証環境で動作確認を行うための最小限の設定例です。

::

    # SSO有効化
    sso.type=saml

    # SP設定
    saml.sp.base.url=https://fess.example.com

    # IdP設定（IdPの管理画面から取得した値を設定）
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...（Base64エンコードされた証明書）

    # デフォルトグループ
    saml.default.groups=user

推奨構成（本番環境向け）
------------------------

以下は、本番環境で使用する際の推奨設定例です。

::

    # SSO有効化
    sso.type=saml

    # SP設定
    saml.sp.base.url=https://fess.example.com

    # IdP設定
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.single_logout_service.url=https://idp.example.com/saml/logout
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...（Base64エンコードされた証明書）

    # ユーザー属性マッピング
    saml.attribute.group.name=groups
    saml.attribute.role.name=roles
    saml.default.groups=user

    # セキュリティ設定（本番環境では有効化を推奨）
    saml.security.want_assertions_signed=true
    saml.security.want_messages_signed=true

トラブルシューティング
======================

よくある問題と解決方法
----------------------

認証後に |Fess| に戻れない
~~~~~~~~~~~~~~~~~~~~~~~~~~

- IdP側のACS URLが正しく設定されているか確認してください
- ``saml.sp.base.url`` の値がIdP側の設定と一致しているか確認してください

署名検証エラー
~~~~~~~~~~~~~~

- IdPの証明書が正しく設定されているか確認してください
- 証明書の有効期限が切れていないか確認してください
- 証明書はBase64エンコードされた内容のみを改行なしで設定してください

ユーザーのグループ・ロールが反映されない
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- IdP側で属性（Attribute）が正しく設定されているか確認してください
- ``saml.attribute.group.name`` の値がIdPから送信される属性名と一致しているか確認してください
- SAMLアサーションの内容を確認するには、デバッグモードを有効にしてください

デバッグ設定
------------

問題を調査する際は、以下の設定でデバッグモードを有効にできます。

::

    saml.security.debug=true

また、|Fess| のログレベルを調整することで、SAML関連の詳細なログを出力できます。

参考情報
========

- :doc:`security-role` - ロールベース検索の設定について
