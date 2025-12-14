=================================
Windows統合認証によるSSO設定
=================================

概要
====

|Fess| はWindows統合認証（SPNEGO/Kerberos）を使用したシングルサインオン（SSO）認証をサポートしています。
Windows統合認証を使用することで、Active Directoryドメインに参加しているWindowsにログインしたユーザーは、追加のログイン操作なしで |Fess| にアクセスできます。

Windows統合認証の仕組み
-----------------------

Windows統合認証では、 |Fess| はSPNEGO（Simple and Protected GSSAPI Negotiation Mechanism）プロトコルを使用してKerberos認証を行います。

1. ユーザーがWindowsドメインにログイン
2. ユーザーが |Fess| にアクセス
3. |Fess| がSPNEGOチャレンジを送信
4. ブラウザがKerberosチケットを取得してサーバーに送信
5. |Fess| がチケットを検証し、ユーザー名を取得
6. LDAPを使用してユーザーのグループ情報を取得
7. ユーザーがログイン状態になり、グループ情報がロールベース検索に適用される

ロールベース検索との連携については、 :doc:`security-role` を参照してください。

前提条件
========

Windows統合認証を設定する前に、以下の前提条件を確認してください：

- |Fess| 15.4以降がインストールされている
- Active Directory（AD）サーバーが利用可能
- |Fess| サーバーがADドメインからアクセス可能
- ADでサービスプリンシパル名（SPN）を設定する権限がある
- LDAPでユーザー情報を取得するためのアカウントがある

Active Directory側の設定
========================

サービスプリンシパル名（SPN）の登録
-----------------------------------

|Fess| 用のSPNをActive Directoryに登録する必要があります。
ADドメインに参加しているWindowsでコマンドプロンプトを開き、 ``setspn`` コマンドを実行します。

::

    setspn -S HTTP/<Fessサーバーのホスト名> <ADアクセス用ユーザー>

例：

::

    setspn -S HTTP/fess-server.example.local svc_fess

登録を確認するには：

::

    setspn -L <ADアクセス用ユーザー>

.. note::
   SPNの登録後、Fessサーバーで実行した場合は一度Windowsからログアウトし、再ログインしてください。

基本設定
========

SSOの有効化
-----------

Windows統合認証を有効にするには、 ``app/WEB-INF/conf/system.properties`` に以下の設定を追加します：

::

    sso.type=spnego

Kerberos設定ファイル
--------------------

``app/WEB-INF/classes/krb5.conf`` を作成し、Kerberos設定を記述します。

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

.. note::
   ``EXAMPLE.LOCAL`` はお使いのADドメイン名（大文字）に、 ``AD-SERVER.EXAMPLE.LOCAL`` はADサーバーのホスト名に置き換えてください。

ログイン設定ファイル
--------------------

``app/WEB-INF/classes/auth_login.conf`` を作成し、JAASログイン設定を記述します。

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

必須設定
--------

``app/WEB-INF/conf/system.properties`` に以下の設定を追加します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト値
   * - ``spnego.preauth.username``
     - AD接続用ユーザー名
     - （必須）
   * - ``spnego.preauth.password``
     - AD接続用パスワード
     - （必須）
   * - ``spnego.krb5.conf``
     - Kerberos設定ファイルパス
     - ``krb5.conf``
   * - ``spnego.login.conf``
     - ログイン設定ファイルパス
     - ``auth_login.conf``

オプション設定
--------------

必要に応じて以下の設定を追加できます。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト値
   * - ``spnego.login.client.module``
     - クライアントモジュール名
     - ``spnego-client``
   * - ``spnego.login.server.module``
     - サーバーモジュール名
     - ``spnego-server``
   * - ``spnego.allow.basic``
     - Basic認証を許可
     - ``true``
   * - ``spnego.allow.unsecure.basic``
     - 非セキュアなBasic認証を許可
     - ``true``
   * - ``spnego.prompt.ntlm``
     - NTLMプロンプトを表示
     - ``true``
   * - ``spnego.allow.localhost``
     - localhostからのアクセスを許可
     - ``true``
   * - ``spnego.allow.delegation``
     - 委任を許可
     - ``false``
   * - ``spnego.exclude.dirs``
     - 認証除外ディレクトリ（カンマ区切り）
     - （なし）
   * - ``spnego.logger.level``
     - ログレベル（0-7）
     - （自動）

.. warning::
   ``spnego.allow.unsecure.basic=true`` は、Base64エンコードされた認証情報を暗号化されていない接続で送信する可能性があります。
   本番環境では ``false`` に設定し、HTTPSを使用することを強く推奨します。

LDAP設定
========

Windows統合認証でログインしたユーザーのグループ情報を取得するために、LDAP設定が必要です。
|Fess| 管理画面の「システム」→「全般」でLDAP設定を行います。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 設定例
   * - LDAP URL
     - ``ldap://AD-SERVER.example.local:389``
   * - Base DN
     - ``dc=example,dc=local``
   * - Bind DN
     - ``svc_fess@example.local``
   * - パスワード
     - AD接続用ユーザーのパスワード
   * - User DN
     - ``%s@example.local``
   * - アカウントフィルタ
     - ``(&(objectClass=user)(sAMAccountName=%s))``
   * - memberOf属性
     - ``memberOf``

ブラウザ設定
============

Windows統合認証を使用するには、クライアント側のブラウザ設定が必要です。

Internet Explorer / Microsoft Edge
----------------------------------

1. インターネットオプションを開く
2. 「セキュリティ」タブを選択
3. 「ローカル イントラネット」ゾーンの「サイト」をクリック
4. 「詳細設定」をクリックし、FessのURLを追加
5. 「ローカル イントラネット」ゾーンの「レベルのカスタマイズ」をクリック
6. 「ユーザー認証」→「ログオン」→「イントラネット ゾーンでのみ自動的にログオンする」を選択
7. 「詳細設定」タブで「統合Windows認証を使用する」にチェック

Google Chrome
-------------

Chromeは通常、Windowsのインターネットオプション設定を使用します。
追加設定が必要な場合は、グループポリシーまたはレジストリで ``AuthServerAllowlist`` を設定します。

Mozilla Firefox
---------------

1. アドレスバーに ``about:config`` と入力
2. ``network.negotiate-auth.trusted-uris`` を検索
3. FessサーバーのURLまたはドメインを設定（例：``https://fess-server.example.local``）

設定例
======

最小構成（検証用）
------------------

以下は検証環境での最小構成例です。

``app/WEB-INF/conf/system.properties``:

::

    # SSO有効化
    sso.type=spnego

    # SPNEGO設定
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-password

``app/WEB-INF/classes/krb5.conf``:

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

``app/WEB-INF/classes/auth_login.conf``:

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

推奨構成（本番用）
------------------

以下は本番環境での推奨構成例です。

``app/WEB-INF/conf/system.properties``:

::

    # SSO有効化
    sso.type=spnego

    # SPNEGO設定
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-secure-password
    spnego.krb5.conf=krb5.conf
    spnego.login.conf=auth_login.conf

    # セキュリティ設定（本番環境）
    spnego.allow.basic=false
    spnego.allow.unsecure.basic=false
    spnego.allow.localhost=false

トラブルシューティング
======================

よくある問題と解決方法
----------------------

認証ダイアログが表示される
~~~~~~~~~~~~~~~~~~~~~~~~~~

- ブラウザの設定でFessサーバーがイントラネットゾーンに追加されているか確認
- 「統合Windows認証を使用する」が有効になっているか確認
- SPNが正しく登録されているか確認（ ``setspn -L <ユーザー名>`` ）

認証エラーが発生する
~~~~~~~~~~~~~~~~~~~~

- ``krb5.conf`` のドメイン名（大文字）とADサーバー名が正しいか確認
- ``spnego.preauth.username`` と ``spnego.preauth.password`` が正しいか確認
- ADサーバーへのネットワーク接続を確認

グループ情報が取得できない
~~~~~~~~~~~~~~~~~~~~~~~~~~

- LDAP設定が正しいか確認
- Bind DNとパスワードが正しいか確認
- ユーザーがADでグループに所属しているか確認

デバッグ設定
------------

問題を調査するために、 |Fess| のログレベルを調整してSPNEGO関連の詳細ログを出力できます。

``app/WEB-INF/conf/system.properties`` に以下を追加：

::

    spnego.logger.level=1

または、 ``app/WEB-INF/classes/log4j2.xml`` に以下のロガーを追加：

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>
    <Logger name="org.codelibs.spnego" level="DEBUG"/>

参考情報
========

- :doc:`security-role` - ロールベース検索の設定
- :doc:`sso-saml` - SAML認証によるSSO設定
- :doc:`sso-oidc` - OpenID Connect認証によるSSO設定
- :doc:`sso-entraid` - Microsoft Entra IDによるSSO設定

