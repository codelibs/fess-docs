======================
SAML認証によるSSO設定
======================

概要
====

|Fess| では、SAML（Security Assertion Markup Language）2.0 を使用したシングルサインオン（SSO）認証をサポートしています。
SAML認証を使用することで、IdP（Identity Provider）で認証されたユーザー情報を |Fess| に連携し、ロールベース検索と組み合わせることで、ユーザーの権限に応じた検索結果の出し分けが可能になります。

.. note::
   SAML認証への対応は ``fess-sso-saml`` プラグインから提供されます。配布物には同梱されて
   いないため、管理画面の「システム > プラグイン」ページ、または
   ``bin/fess-setup install plugin fess-sso-saml`` で導入してください。
   このプラグインは、SAMLライブラリ `saml4j <https://github.com/codelibs/saml4j>`__ でSAMLメッセージを処理します。
   導入するまで、 ``sso.type=saml`` を設定しても ``/sso/`` へのリクエストはログインページへ
   リダイレクトされるだけです。

SAML認証の仕組み
----------------

SAML認証では、|Fess| がSP（Service Provider）として動作し、外部のIdPと連携して認証を行います。

1. ユーザーが |Fess| のSSOエンドポイント（``/sso/``）にアクセス
2. |Fess| がIdPに認証リクエストをリダイレクト
3. ユーザーがIdPで認証を実行
4. IdPがSAMLアサーションを |Fess| に送信
5. |Fess| がアサーションを検証し、ユーザーをログイン

.. note::
   サポートされるのは、上記のように |Fess| 側（``/sso/``）から開始するSP-Initiatedログインのみです。
   |Fess| は送信したAuthnRequestのIDとSAMLレスポンスを対応付けて検証するため、
   IdPのポータル（Oktaのダッシュボードや Microsoft Entra ID の「マイアプリ」など）に置いたタイルから
   開始するIdP-Initiated（未承諾・unsolicited）SSOは、対応付けるAuthnRequestが存在せず拒否されます。
   IdP側にタイルを配置する場合は、リンク先を |Fess| の ``/sso/`` にしてください。

   なお 15.7 では、``tomcat.sameSiteCookies=none`` を設定していると、IdP-Initiatedのログインが
   結果的に動作していました。|Fess| が対応付けできないレスポンスをIdPへ差し戻し、IdPが即座に
   SP-Initiatedのアサーションを返していたためです。15.8 ではこの差し戻しを行わなくなったため、
   IdP-Initiatedのログインは動作しません。

ロールベース検索との連携については、:doc:`security-role` を参照してください。

.. note::
   複数のノードを動かす場合は、ノード間でHTTPセッションを共有する環境変数 ``FESS_SESSION_STORE=opensearch`` を設定すると、あるノードで始めたログインを別のノードで完了できます。有効にする前に、すべてのノードのプラグインを15.10に更新してください。15.9.0のプラグインはログインの状態を共有せず、別のノードに戻ってきた利用者は未ログインのままになります。セッションを共有しない場合は、ロードバランサーで同じセッションを同じノードに固定してください。共有される内容と、セッションストアに接続できない場合の動作については、 :doc:`session-store` を参照してください。

   ``FESS_SESSION_STORE=opensearch`` を設定している場合、SSO プラグイン（ ``fess-sso-saml`` 、 ``fess-sso-oidc`` 、 ``fess-sso-entraid`` ）を追加または削除すると、保存されているセッションの形式バージョンが変わります。その結果、保存されているすべてのセッションが無効になり、すべての利用者が再ログインする必要があります。これらのプラグインは、すべてのノードで同じように追加または削除してください。これらのプラグインの組み合わせが他のノードと異なるノードは、他のノードが保存したセッションを読めず、他のノードもそのノードのセッションを読めません。ストレージ、スクリプト、SPNEGO などの他のプラグインは、形式を変えません。

前提条件
========

SAML認証を設定する前に、以下の前提条件を確認してください。

- |Fess| 15.10 以降がインストールされていること
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

.. note::
   ``sso.type`` および基本的なSAML設定（IdP情報、SP情報、ユーザー属性マッピング）は、管理画面の「システム > 全般」ページからも設定・変更できます。
   管理画面で変更した設定は ``system.properties`` に保存され、再起動後も保持されます。
   ただし、署名・暗号化などのセキュリティ設定やSP証明書・秘密鍵は管理画面では設定できないため、``system.properties`` に直接記述してください。

.. note::
   ``saml.`` で始まる設定は ``system.properties`` からのみ読み込まれます。
   JVMのシステムプロパティ（``-Dsaml.security....`` や ``-Dfess.saml.security....``）で指定しても参照されません。
   特に ``saml.security.*`` は管理画面にも項目がないため、
   ``system.properties`` に直接記述する以外に設定する方法はありません。

セッションCookieの設定
----------------------

IdPはアサーションを |Fess| へ **クロスサイトのPOST** で返します。``SameSite=Lax`` のCookieはこのリクエストに送信されないため、|Fess| が同梱する既定値のままではSAMLログインが完了しません。

``tomcat_config.properties`` の ``tomcat.sameSiteCookies`` を ``none`` に変更してください。このファイルはZIP版では ``lib/classes/`` 、DEB/RPM版では ``/etc/fess/`` に配置されています。

::

    tomcat.sameSiteCookies = none

.. warning::
   ``none`` はブラウザが ``Secure`` 属性付きCookieに対してのみ受け入れます。したがって |Fess| をHTTPSで提供する必要があります。HTTPのままでは |Fess| にログインできなくなります。

.. note::
   既定値の ``lax`` はリダイレクト（GET）で戻るSSO方式のために設定されています。SAMLのHTTP-POSTバインディングはこれに該当しないため、SAMLを利用する場合のみ変更が必要です。設定変更後は |Fess| の再起動が必要です。

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
     - ``http://localhost:8080``

.. note::
   ``saml.sp.base.url`` のデフォルトは ``http://localhost:8080`` です。
   検証環境以外では、必ず |Fess| に外部からアクセスする際のURL（本番環境ではHTTPS）を設定してください。

この設定により、以下のエンドポイントが自動的に構成されます。

- **Entity ID**: ``{saml.sp.base.url}/sso/metadata``
- **ACS URL**: ``{saml.sp.base.url}/sso/``
- **SLO URL**: ``{saml.sp.base.url}/sso/logout``

設定例::

    saml.sp.base.url=https://fess.example.com

個別URL設定
~~~~~~~~~~~

通常は ``saml.sp.base.url`` を設定すれば各エンドポイントURLは自動的に構成されますが、
必要に応じて以下のプロパティで個別のURLを明示的に指定し、上書きすることもできます。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.sp.entityid``
     - SPのEntity ID
     - ``{saml.sp.base.url}/sso/metadata``
   * - ``saml.sp.assertion_consumer_service.url``
     - Assertion Consumer Service URL
     - ``{saml.sp.base.url}/sso/``
   * - ``saml.sp.single_logout_service.url``
     - Single Logout Service URL
     - ``{saml.sp.base.url}/sso/logout``

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
   * - ``saml.idp.x509certMulti.1``, ``.2``, ...
     - 追加のIdP署名用証明書（たとえば鍵のロールオーバー時）
     - （オプション）

.. note::
   IdPの証明書は署名に対する唯一のトラストアンカーであり、メッセージに含まれる証明書が信頼されることはありません。
   IdPおよびSPの証明書は、2048ビット以上のRSA鍵である必要があります。
   ``saml.idp.x509certMulti.N`` を設定している場合は、``saml.idp.x509cert`` を省略できます。

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

.. note::
   |Fess| はすべてのアサーションについて以下を検証します。URLは受信したリクエストではなく、``saml.sp.base.url``\ （または個別のURLプロパティ）から導出されます。

   - アサーションに、SPのEntity IDを指す ``AudienceRestriction`` が含まれていること
   - 署名されたResponseの ``Destination`` と、SubjectConfirmationの ``Recipient`` が、Assertion Consumer ServiceのURLであること

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

.. note::
   |Fess| はアサーションのグループ値をそのまま使用し、ディレクトリへの問い合わせや
   ネストされたグループ（親グループ）の展開は行いません。
   親グループが含まれるかどうかは、IdP側のクレーム設定だけで決まります。
   Microsoft Graph APIで親グループを解決する :doc:`sso-entraid` とは動作が異なります。

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

.. warning::
   ``saml.attribute.role.name`` を設定すると、IdPから送信された属性値がそのまま |Fess| のロールになります。
   ``fess_config.properties`` の ``authentication.admin.roles`` は既定で ``admin`` であるため、
   IdPがロール属性に ``admin`` を含めて送信したユーザーは |Fess| の管理者権限を得ます。
   IdP側でロール属性の値を管理できる範囲を確認し、必要に応じて ``authentication.admin.roles`` を
   別の名前に変更してください。

属性名が重複するIdP
-------------------

IdPが同じ属性名を複数の ``<Attribute>`` 要素に分けて送信した場合、|Fess| は値をマージします。

Keycloakは既定でこの形式のアサーションを送信します。ロールマッパーとグループマッパーは
``single`` オプションを有効にしない限り値ごとに別々の ``<Attribute>`` 要素を出力し、
Keycloakのアカウントは既定で複数のレルムロールを持つためです。|Fess| 側で必要な設定はありません。

セキュリティ設定
================

以下のセキュリティ設定は ``system.properties`` から読み込まれます。

.. note::
   既定値を弱める設定が残っている場合（シングルログアウトを設定したうえでの ``saml.security.want_logout_signed=false`` 、
   ``saml.security.allow_deprecated_alg=true`` 、``saml.security.allow_rsa_1_5=true``）、
   SAMLの設定を読み込んだ時点で ``Insecure SAML settings: ...`` という警告がログに出力されます。

署名の設定
----------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.security.authnrequest_signed``
     - 認証リクエストに署名する（``saml.sp.privatekey`` が必要）
     - ``false``
   * - ``saml.security.want_messages_signed``
     - Responseの署名を要求する
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - Assertionの署名を要求する
     - ``false``
   * - ``saml.security.want_logout_signed``
     - IdPからのログアウトメッセージの署名を要求する
     - ``true``
   * - ``saml.security.allow_deprecated_alg``
     - SHA-1の署名を受け付ける
     - ``false``
   * - ``saml.security.signature_algorithm``
     - 送信する署名のアルゴリズム（``rsa-sha256`` 、``rsa-sha384`` または ``rsa-sha512`` のURI）
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``

.. note::
   これらの設定にかかわらず、ResponseまたはAssertionのいずれかは署名されている必要があります。
   IdPが署名する要素に対して署名を要求するには、``saml.security.want_messages_signed`` または ``saml.security.want_assertions_signed`` を使用してください。
   署名は、署名対象の要素をその要素自身のIDで参照し、``rsa-sha256`` 、``rsa-sha384`` または ``rsa-sha512``（あるいはそのECDSA版）を使用している必要があります。
   SHA-1の署名は ``saml.security.allow_deprecated_alg=true`` を設定しない限り拒否されるため、IdPがSHA-256以上で署名していることを確認してください。

.. note::
   シングルログアウト（``saml.idp.single_logout_service.url``）を設定する場合は、
   IdPが送信するLogoutRequestとLogoutResponseを ``saml.idp.x509cert`` の鍵で署名する必要があります
   （既定で ``saml.security.want_logout_signed=true`` です）。
   ``saml.security.want_logout_signed=false`` は、署名できないIdPに対してのみ設定してください。
   シングルログアウトサービス（``/sso/logout``）は、リダイレクトバインディング（GET）とPOSTバインディングを受け付けます。
   IdP側にも、POSTバインディング用として ``/sso/logout`` のURLを登録してください。
   IdPがAssertion Consumer ServiceにPOSTしてくるLogoutResponseは認識されません。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.session.end_with_idp``
     - IdPのセッションが終了したら |Fess| のログインも終了する。Assertionの ``SessionNotOnOrAfter`` に ``saml.security.clock_drift`` を加えた時刻に終了します。``false`` で無効
     - ``true``

.. note::
   IdPが ``SessionNotOnOrAfter`` を指定しない場合、この設定は働きません。IdPのセッションの上限が短い場合（Keycloakの既定は10時間）、以前より早くログアウトされることがあります。IdP側でログアウトしても、 |Fess| のログインはこの時刻まで続きます。この理由でログインが終了すると、監査ログに理由 ``idp_session_ended`` の ``SESSION_END`` が記録されます（ :doc:`../install/security` を参照）。

暗号化の設定
------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.security.want_assertions_encrypted``
     - アサーションの暗号化を要求する（``saml.sp.privatekey`` が必要）
     - ``false``
   * - ``saml.security.allow_rsa_1_5``
     - RSA 1.5の鍵輸送を受け付ける（``saml.sp.privatekey`` が必要）。設定しない場合はOAEPのみ受け付けます
     - ``false``

.. note::
   IdPがRSA 1.5でしか暗号化できない場合を除き、``saml.security.allow_rsa_1_5`` は ``false`` のままにしてください。

SP証明書・秘密鍵の設定
----------------------

SP側で認証リクエストやログアウトメッセージに署名する場合（``saml.security.authnrequest_signed`` など）、
またはアサーションやNameIDの暗号化を要求する場合（``saml.security.want_assertions_encrypted`` など）は、
SPの秘密鍵（PKCS#8）とX.509証明書を設定する必要があります。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.sp.x509cert``
     - SPのX.509証明書（Base64エンコード、改行なし）
     - （空文字）
   * - ``saml.sp.privatekey``
     - SPの秘密鍵（Base64エンコード、改行なし）
     - （空文字）

.. note::
   ``saml.sp.x509cert`` と ``saml.sp.privatekey`` には、``saml.idp.x509cert`` と同様に、
   Base64エンコードされた内容を改行なしの1行で指定します（``-----BEGIN ...-----`` と ``-----END ...-----`` の行は含めません）。
   署名・暗号化を有効にする場合は、SP証明書をIdP側にも登録してください。SP証明書は ``/sso/metadata`` のSPメタデータに含まれて公開されます。

その他のセキュリティ設定
------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.security.requested_authncontext``
     - 要求する認証コンテキスト（空にすると何も要求しない）
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.security.requested_authncontextcomparison``
     - 要求する認証コンテキストの比較方法（``exact`` 、``minimum`` 、``maximum`` または ``better``）
     - ``exact``
   * - ``saml.security.clock_drift``
     - 有効期間の検証で許容する時刻のずれ（秒、0〜600）
     - ``120``
   * - ``saml.security.max_message_size``
     - 受け付けるデコード後のメッセージの最大サイズ（バイト、1024〜16777216）
     - ``1048576``
   * - ``saml.sp.nameidformat``
     - NameIDフォーマット
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   アサーションのAudience、Recipient、Destination、Issuer、有効期間は常に検証され、
   レスポンスは |Fess| が開始したログインに対するものでなければなりません。
   Audienceを持たないアサーション、またはAudienceにSPのEntity IDが含まれないアサーションは拒否されます。
   検証は常に厳密に行われ、``saml.strict=false`` は拒否されます。

使用されなくなったプロパティ
----------------------------

以下のプロパティは無視されます。これらを挙げた警告が1件ログに出力されます。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - プロパティ
     - 現在の扱い
   * - ``saml.security.reject_deprecated_alg``
     - SHA-1の署名は既定で拒否されます。``saml.security.allow_deprecated_alg=true`` で受け付けます
   * - ``saml.security.allowed_key_transport_algorithms``
     - 既定ではOAEPのみ受け付けます。``saml.security.allow_rsa_1_5=true`` でRSA 1.5も受け付けます
   * - ``saml.security.allow_duplicated_attribute_name``
     - 重複した属性は常にマージされます
   * - ``saml.security.reject_missing_audience``
     - Audienceを持たないアサーションは常に拒否されます
   * - ``saml.idp.certfingerprint``, ``saml.idp.certfingerprint_algorithm``
     - ``saml.idp.x509cert`` を設定してください。フィンガープリントはトラストアンカーではありません
   * - ``saml.security.sign_metadata``, ``saml.security.want_nameid_encrypted``, ``saml.security.want_xml_validation``, ``saml.security.logoutrequest_signed``, ``saml.security.logoutresponse_signed``, ``saml.security.digest_algorithm``, ``saml.keystore.*``, ``saml.contacts.*``, ``saml.organization.*``, ``saml.compress.*``, ``saml.parsing.*``, ``saml.unique_id_prefix``、``*.binding`` および ``*.response.url`` のプロパティ
     - 使用されなくなりました

ライブラリが認識しないその他の ``saml.`` プロパティがあると、そのプロパティ名を示すメッセージとともにSAMLログインが停止します。
これは、セキュリティ設定の記述ミスを見逃さないようにするためです。``saml.debug`` は受け付けられますが、効果はありません。

AuthnRequestの有効期限
======================

|Fess| は ``/sso/`` へのアクセスごとにAuthnRequestを1件IdPへ送信し、そのIDをセッションに記録します。
IdPから返されたSAMLレスポンスは、記録されたIDと対応付けて検証されます。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``saml.request.id.ttl``
     - 応答のないAuthnRequestのIDを保持する期間（秒）
     - ``3600``

記録されたIDは、この期間を過ぎると破棄されます。IdPのログイン画面を開いたまま放置するなどして
有効期限を過ぎた場合、戻ってきたアサーションは対応付けられず、その場で1回だけログインに失敗します。

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
    # IdPが署名する要素に対して署名を要求する
    # （Responseの場合は saml.security.want_messages_signed=true）
    saml.security.want_assertions_signed=true

トラブルシューティング
======================

よくある問題と解決方法
----------------------

認証後に |Fess| に戻れない
~~~~~~~~~~~~~~~~~~~~~~~~~~

- IdP側のACS URLが正しく設定されているか確認してください
- ``saml.sp.base.url`` の値がIdP側の設定と一致しているか確認してください
- IdPからのSAMLアサーションはクロスサイトのPOSTで送信されます。``tomcat_config.properties`` の
  ``tomcat.sameSiteCookies`` が ``lax``（既定値）の場合、ブラウザはセッションCookieを送信しないため、
  その場で1回だけログインに失敗します。この場合は ``tomcat.sameSiteCookies = none`` を設定してください
  （``SameSite=None`` はHTTPSが必須です）
- IdPでのログインに時間がかかった場合、アサーションが戻ってきた時点でAuthnRequestのIDは残っていないため、
  その場で1回だけログインに失敗します。この場合はログインをやり直してください
- |Fess| は ``app/WEB-INF/web.xml`` で ``session-timeout`` を指定していないため、
  サーブレットコンテナの既定値である30分が適用されます。これは ``saml.request.id.ttl`` の3600秒より短く、
  セッションが先に破棄されます。このため ``saml.request.id.ttl`` だけを大きくしても猶予は延びません。
  猶予を延ばしたい場合は、セッションタイムアウトも合わせて延長してください

DestinationまたはRecipientの検証に失敗する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

署名されたResponseの ``Destination`` と、SubjectConfirmationの ``Recipient`` は、
|Fess| のAssertion Consumer ServiceのURLである必要があります。このURLは |Fess| に届いたリクエストではなく
``saml.sp.base.url``（または ``saml.sp.assertion_consumer_service.url``）から導出されるため、
TLSを終端するリバースプロキシがあっても比較には影響しません。

- ``saml.sp.base.url`` に、スキームとポートを含む外部から見えるURLを設定してください
- IdP側にも同じACS URL（``{saml.sp.base.url}/sso/``）を登録してください
- ``saml.sp.entityid`` を上書きしている場合は、IdPがその値をAudienceとして使用する必要があります

署名検証エラー
~~~~~~~~~~~~~~

- IdPの証明書が正しく設定されているか確認してください
- 証明書の有効期限が切れていないか確認してください
- 証明書はBase64エンコードされた内容のみを改行なしで設定してください
- IdPの証明書は、2048ビット以上のRSA鍵である必要があります
- ResponseまたはAssertionのいずれかが署名されており、その署名がSHA-256以上を使用している必要があります
  （SHA-1は ``saml.security.allow_deprecated_alg=true`` の場合のみ受け付けられます）
- レスポンスが拒否された理由は、``Authentication failed: <reason> - <detail>`` としてログに出力されます

ユーザーのグループ・ロールが反映されない
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- IdP側で属性（Attribute）が正しく設定されているか確認してください
- ``saml.attribute.group.name`` の値がIdPから送信される属性名と一致しているか確認してください
- Microsoft Entra IDでは、ソース属性を変更しない限りグループクレームの値はグループの ``ObjectId`` （GUID）になるため、
  グループ名とは一致しません
- ユーザーが150を超えるグループに所属している場合、Microsoft Entra IDはグループクレーム自体を送信しません
  （ネストされたグループもこの上限に数えられます）。このとき |Fess| は ``saml.default.groups`` にフォールバックします
- IdPが実際に送信するアサーションの属性名と比較してください

ログ設定
--------

SAML認証に失敗した場合、その理由は常に警告としてログに出力されます。
``saml.debug`` プロパティは効果がありません。

SAML関連の詳細なログを出力するには、``app/WEB-INF/classes/log4j2.xml`` に以下のロガーを追加します。

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

参考情報
========

- :doc:`security-role` - ロールベース検索の設定について
- :doc:`sso-oidc` - OpenID ConnectによるSSO設定について
- :doc:`sso-entraid` - Microsoft Entra ID専用のSSO設定について
