==================================
LDAP統合ガイド
==================================

概要
====

|Fess| はLDAP（Lightweight Directory Access Protocol）サーバーとの統合をサポートしており、
エンタープライズ環境での認証とユーザー管理を実現できます。

LDAP統合により:

- Active DirectoryやOpenLDAPでのユーザー認証
- グループベースのアクセス制御
- ユーザー情報の自動同期

が可能になります。

対応LDAPサーバー
================

|Fess| は以下のLDAPサーバーとの統合をサポートしています:

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- その他のLDAP v3互換サーバー

前提条件
========

- LDAPサーバーへのネットワークアクセス
- LDAP検索用のサービスアカウント（バインドDN）
- LDAPの構造（ベースDN、属性名など）の理解

基本設定
========

``app/WEB-INF/conf/system.properties`` に以下の設定を追加します。

LDAP接続設定
------------

::

    # LDAP認証を有効にする
    ldap.admin.enabled=true

    # LDAPサーバーのURL
    ldap.provider.url=ldap://ldap.example.com:389

    # セキュア接続（LDAPS）の場合
    # ldap.provider.url=ldaps://ldap.example.com:636

    # ベースDN
    ldap.base.dn=dc=example,dc=com

    # ユーザー認証用バインドDNテンプレート（%sにユーザー名が埋め込まれる）
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # 管理用バインドDN（LDAP検索用サービスアカウント）
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com

    # 管理用バインドパスワード
    ldap.admin.security.credentials=your_password

アカウントフィルター設定
------------------------

::

    # アカウントフィルター（ユーザー認証時の検索フィルター）
    ldap.account.filter=uid=%s

    # LDAP管理画面でのユーザー検索フィルター
    ldap.admin.user.filter=uid=%s

.. note::

   ``ldap.account.filter`` はユーザー認証時の検索フィルターで、
   ``ldap.admin.user.filter`` はLDAP管理画面でのユーザー検索フィルターです。
   用途が異なるため、それぞれ適切に設定してください。

LDAP管理用ベースDN設定
----------------------

::

    # ユーザー検索ベースDN
    ldap.admin.user.base.dn=ou=People,dc=example,dc=com

    # ロール検索ベースDN
    ldap.admin.role.base.dn=ou=Roles,dc=example,dc=com

    # グループ検索ベースDN
    ldap.admin.group.base.dn=ou=Groups,dc=example,dc=com

グループフィルター設定
----------------------

::

    # グループフィルター
    ldap.group.filter=(member={0})

    # memberOf属性名
    ldap.memberof.attribute=memberOf

Active Directory設定
====================

Microsoft Active Directory向けの設定例です。

基本設定
--------

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # ユーザー認証用バインドDNテンプレート（UPN形式）
    ldap.security.principal=%s@example.com

    # 管理用バインドDN（サービスアカウント）
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # アカウントフィルター
    ldap.account.filter=sAMAccountName=%s

    # グループフィルター
    ldap.group.filter=(member={0})

Active Directory固有の設定
--------------------------

::

    # memberOf属性を使用
    ldap.memberof.attribute=memberOf

    # 入れ子グループの解決（LDAP_MATCHING_RULE_IN_CHAIN）
    ldap.group.filter=(member:1.2.840.113556.1.4.1941:={0})

OpenLDAP設定
============

OpenLDAP向けの設定例です。

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # ユーザー認証用バインドDNテンプレート
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # 管理用バインドDN（サービスアカウント）
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # アカウントフィルター
    ldap.account.filter=uid=%s

    # グループフィルター
    ldap.group.filter=(memberUid={0})

セキュリティ設定
================

LDAPS（SSL/TLS）
----------------

暗号化された接続を使用:

::

    # LDAPSを使用
    ldap.provider.url=ldaps://ldap.example.com:636

自己署名証明書の場合は、Java truststore に証明書をインポート:

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

パスワードの保護
----------------

パスワードを環境変数で設定:

::

    ldap.admin.security.credentials=${LDAP_PASSWORD}

フェイルオーバー
================

複数のLDAPサーバーへのフェイルオーバー:

::

    # スペース区切りで複数のURLを指定
    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

トラブルシューティング
======================

接続エラー
----------

**症状**: LDAP接続に失敗する

**確認事項**:

1. LDAPサーバーが起動しているか
2. ファイアウォールでポートが開いているか（389または636）
3. URLが正しいか（``ldap://`` または ``ldaps://``）
4. バインドDNとパスワードが正しいか

認証エラー
----------

**症状**: ユーザー認証に失敗する

**確認事項**:

1. ユーザー検索フィルターが正しいか
2. ユーザーが検索ベースDN内に存在するか
3. ユーザー名属性が正しいか

グループが取得できない
----------------------

**症状**: ユーザーのグループが取得できない

**確認事項**:

1. グループ検索フィルターが正しいか
2. グループのメンバーシップ属性が正しいか
3. グループが検索ベースDN内に存在するか

デバッグ設定
------------

詳細なログを出力:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

参考情報
========

- :doc:`security-role` - ロールベースのアクセス制御
- :doc:`sso-spnego` - SPNEGO（Kerberos）認証
- :doc:`../admin/user-guide` - ユーザー管理ガイド
