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

前提条件
========

SAML認証を設定する前に、以下の前提条件を確認してください。

- |Fess| 15.8 以降がインストールされていること
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
   特に ``saml.security.*`` 、 ``saml.strict`` 、 ``saml.debug`` は管理画面にも項目がないため、
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

.. warning::
   ``saml.attribute.role.name`` を設定すると、IdPから送信された属性値がそのまま |Fess| のロールになります。
   ``fess_config.properties`` の ``authentication.admin.roles`` は既定で ``admin`` であるため、
   IdPがロール属性に ``admin`` を含めて送信したユーザーは |Fess| の管理者権限を得ます。
   IdP側でロール属性の値を管理できる範囲を確認し、必要に応じて ``authentication.admin.roles`` を
   別の名前に変更してください。

セキュリティ設定
================

本番環境では、以下のセキュリティ設定を有効にすることを推奨します。

.. note::
   推奨されない設定が残っている場合、SAMLの設定を読み込んだ時点で
   ``Insecure SAML settings: ...`` という警告がログに出力されます。

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
   * - ``saml.security.reject_deprecated_alg``
     - SHA-1などの非推奨署名アルゴリズムを拒否する
     - ``false``

.. warning::
   デフォルトではセキュリティ機能が無効になっています。
   本番環境では、少なくとも ``saml.security.want_assertions_signed=true`` を設定することを強く推奨します。

.. note::
   ``saml.security.reject_deprecated_alg`` が ``false`` の間は、SHA-1（``rsa-sha1`` および ``dsa-sha1``）で
   署名されたアサーションやメッセージも受け入れられます。既定で有効になっていないのは、
   有効にするとSHA-1で署名を行うIdPを拒否してしまうためです。
   IdPがSHA-256以上で署名していることを確認したうえで、``saml.security.reject_deprecated_alg=true`` を設定してください。

.. warning::
   シングルログアウト（``saml.idp.single_logout_service.url``）を設定する場合は、
   ``saml.security.want_messages_signed=true`` を必ず併せて設定してください。
   ``false`` のままでは、``/sso/logout`` が受け取るLogoutRequestに署名が要求されません。
   検証されるのはXMLスキーマ、``NotOnOrAfter``（存在する場合）、``Destination``（存在する場合）、
   および Issuer が ``saml.idp.entityid`` と一致すること（存在する場合）だけで、
   LogoutRequest内のNameIDがログイン中のユーザーと一致するかは検査されません。
   Issuer要素はSAMLのスキーマ上は省略可能であり、省略されたLogoutRequestではIdPのEntity IDとの
   照合そのものが行われません。このため攻撃者はIdPのEntity IDを知らなくても、署名のないLogoutRequestを作成し、
   そのURLをユーザーに踏ませることで認証済みセッションを終了させられます。
   影響は強制ログアウト（サービス妨害）であり、アカウントの乗っ取りではありません。

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

SP証明書・秘密鍵の設定
----------------------

SP側で認証リクエストやログアウトメッセージに署名する場合（``saml.security.authnrequest_signed`` など）、
またはアサーションやNameIDの暗号化を要求する場合（``saml.security.want_assertions_encrypted`` など）は、
SPの秘密鍵とX.509証明書を設定する必要があります。

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
   * - ``saml.strict``
     - 厳密モード（検証を厳密に行う）
     - ``true``
   * - ``saml.security.want_xml_validation``
     - メッセージのXMLスキーマ検証を行う
     - ``true``
   * - ``saml.security.signature_algorithm``
     - 署名アルゴリズム
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``
   * - ``saml.security.requested_authncontext``
     - 要求する認証コンテキスト
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.sp.nameidformat``
     - NameIDフォーマット
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   |Fess| は内部的にSAMLライブラリ（java-saml）を使用しており、``saml.`` で始まるプロパティは
   ライブラリの対応する設定（``onelogin.saml2.`` プレフィックス）にマッピングされます。
   このため、ここで挙げた以外にも、バインディング（``saml.sp.assertion_consumer_service.binding`` など）、
   組織情報（``saml.organization.*``）、連絡先情報（``saml.contacts.*``）といった詳細な設定を
   ``system.properties`` で指定できます。

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
値を指定しない場合は3600秒が使われます。数値として解釈できない値を指定した場合も3600秒が使われ、
``Invalid saml.request.id.ttl`` で始まる警告が出力されます。

.. note::
   1つのセッションで保持できる応答待ちのAuthnRequestは最大10件で、上限を超えると古いものから破棄されます。
   これは複数のタブから同時にログインを開始できるようにするためのもので、``saml.`` で始まる設定では変更できません。

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

    # IdPがSHA-256以上で署名していることを確認してから有効化する
    saml.security.reject_deprecated_alg=true

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
  |Fess| は対応するAuthnRequestのIDを見つけられず、その場で1回だけログインに失敗します。
  ブラウザはログイン画面に戻り「SSOログイン処理に失敗しました。」が表示され、ログには
  ``Received a SAML response with no matching AuthnRequest ID in the session``
  で始まる警告が出力されます。この場合は ``tomcat.sameSiteCookies = none`` を設定してください
  （``SameSite=None`` はHTTPSが必須です）
- IdPのログイン画面で時間がかかり ``saml.request.id.ttl``（既定3600秒）を過ぎた場合も、
  記録されたAuthnRequestのIDが破棄されているため同じ警告が出力されます。
  この場合はログインをやり直してください

.. note::
   15.7 では同じ状況でIdPへの再リダイレクトが繰り返され、ログインがループしていました。
   15.8 ではループせずに1回で失敗するよう変更されています。設定の対処方法は変わりません。

リバースプロキシ経由でDestinationの検証に失敗する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TLSを終端するリバースプロキシやロードバランサーの背後に |Fess| を配置すると、
``saml.sp.base.url`` を正しく設定していてもアサーションの検証に失敗することがあります。

原因は、SAMLライブラリがアサーションの ``Destination`` 属性を、設定されたACS URLではなく
サーブレットコンテナが組み立てたリクエストURLと比較するためです。プロキシがHTTPSを終端すると、
|Fess| が認識するリクエストURLは ``http://<内部ホスト名>:<内部ポート>/sso/`` のような内部向けの値になり、
IdPが送ってきた ``https://fess.example.com/sso/`` と一致しません。
``saml.sp.base.url`` はこの比較には使われないため、この設定だけでは解決しません。

``saml.debug=true`` を設定すると、ログに以下のような理由が出力されます。

::

    The response was received at http://... instead of https://fess.example.com/sso/

この場合は ``tomcat_config.properties`` のコネクタ設定を、外部から見えるスキームとポートに合わせてください。
以下の設定は既定ではコメントアウトされています。

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

あわせて、リバースプロキシが元の ``Host`` ヘッダーをそのまま |Fess| へ渡すように設定してください。
リクエストURLのホスト名部分は ``Host`` ヘッダーから組み立てられます。
``tomcat_config.properties`` を変更した後は |Fess| の再起動が必要です。

同じ検証はシングルログアウトのメッセージにも適用されるため、SLOを利用する場合も同様に設定してください。

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

    saml.debug=true

``saml.debug=true`` を設定すると、SAML認証に失敗した際の詳細な理由がログに出力されます。

また、``app/WEB-INF/classes/log4j2.xml`` に以下のロガーを追加することで、SAML関連の詳細なログを出力できます。

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

参考情報
========

- :doc:`security-role` - ロールベース検索の設定について
- :doc:`sso-oidc` - OpenID ConnectによるSSO設定について
- :doc:`sso-entraid` - Microsoft Entra ID専用のSSO設定について
