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

    # バインドDN（サービスアカウント）
    ldap.security.principal=cn=fess,ou=services,dc=example,dc=com

    # バインドパスワード
    ldap.admin.security.credentials=your_password

ユーザー検索設定
----------------

::

    # ユーザー検索のベースDN
    ldap.user.search.base=ou=users,dc=example,dc=com

    # ユーザー検索フィルター
    ldap.user.search.filter=(uid={0})

    # ユーザー名属性
    ldap.user.name.attribute=uid

グループ検索設定
----------------

::

    # グループ検索のベースDN
    ldap.group.search.base=ou=groups,dc=example,dc=com

    # グループ検索フィルター
    ldap.group.search.filter=(member={0})

    # グループ名属性
    ldap.group.name.attribute=cn

Active Directory設定
====================

Microsoft Active Directory向けの設定例です。

基本設定
--------

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # サービスアカウント（UPN形式）
    ldap.security.principal=fess@example.com
    ldap.admin.security.credentials=your_password

    # ユーザー検索
    ldap.user.search.base=ou=Users,dc=example,dc=com
    ldap.user.search.filter=(sAMAccountName={0})
    ldap.user.name.attribute=sAMAccountName

    # グループ検索
    ldap.group.search.base=ou=Groups,dc=example,dc=com
    ldap.group.search.filter=(member={0})
    ldap.group.name.attribute=cn

Active Directory固有の設定
--------------------------

::

    # 入れ子グループの解決
    ldap.memberof.enabled=true

    # memberOf属性を使用
    ldap.group.search.filter=(member:1.2.840.113556.1.4.1941:={0})

OpenLDAP設定
============

OpenLDAP向けの設定例です。

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # サービスアカウント
    ldap.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # ユーザー検索
    ldap.user.search.base=ou=people,dc=example,dc=com
    ldap.user.search.filter=(uid={0})
    ldap.user.name.attribute=uid

    # グループ検索
    ldap.group.search.base=ou=groups,dc=example,dc=com
    ldap.group.search.filter=(memberUid={0})
    ldap.group.name.attribute=cn

セキュリティ設定
================

LDAPS（SSL/TLS）
----------------

暗号化された接続を使用:

::

    # LDAPSを使用
    ldap.provider.url=ldaps://ldap.example.com:636

    # StartTLSを使用
    ldap.start.tls=true

自己署名証明書の場合は、Java truststore に証明書をインポート:

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

パスワードの保護
----------------

パスワードを環境変数で設定:

::

    ldap.admin.security.credentials=${LDAP_PASSWORD}

ロールマッピング
================

LDAPグループを |Fess| のロールにマッピングできます。

自動マッピング
--------------

グループ名がそのままロール名として使用されます:

::

    # LDAPグループ "fess-users" → Fessロール "fess-users"
    ldap.group.role.mapping.enabled=true

カスタムマッピング
------------------

::

    # グループ名をロールにマッピング
    ldap.group.role.mapping.Administrators=admin
    ldap.group.role.mapping.PowerUsers=editor
    ldap.group.role.mapping.Users=guest

ユーザー情報の同期
==================

LDAPからユーザー情報を |Fess| に同期できます。

自動同期
--------

ログイン時に自動的にユーザー情報を同期:

::

    ldap.user.sync.enabled=true

同期する属性
------------

::

    # メールアドレス
    ldap.user.email.attribute=mail

    # 表示名
    ldap.user.displayname.attribute=displayName

接続プーリング
==============

パフォーマンス向上のための接続プール設定:

::

    # 接続プールを有効にする
    ldap.connection.pool.enabled=true

    # 最小接続数
    ldap.connection.pool.min=1

    # 最大接続数
    ldap.connection.pool.max=10

    # 接続タイムアウト（ミリ秒）
    ldap.connection.timeout=5000

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
