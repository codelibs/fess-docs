==================================
LDAP統合ガイド
==================================

概要
====

|Fess| はLDAP（Lightweight Directory Access Protocol）サーバーとの統合をサポートしており、
エンタープライズ環境での認証とユーザー管理を実現できます。

LDAP統合により:

- Active DirectoryやOpenLDAPでのユーザー認証（ログイン）
- グループ・ロールベースのアクセス制御
- 管理画面からのLDAPユーザー／ロール／グループ管理（オプション）

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

設定方法の概要
==============

|Fess| のLDAP設定は、用途によって2つの場所で管理されます。

接続・認証設定（管理画面 / ``system.properties``）
   LDAPサーバーへの接続とログイン認証に関する設定です。
   管理画面の **「システム > 全般」** ページにある「LDAP」セクションから設定でき、
   ``app/WEB-INF/conf/system.properties`` に保存されます。

LDAP管理機能・動作設定（``fess_config.properties``）
   管理画面からLDAPユーザー／ロール／グループを管理する機能や、
   ロール解決などの動作に関する設定です。これらは
   ``app/WEB-INF/classes/fess_config.properties`` に定義されており、
   値を変更する場合はこのファイルを編集します。

.. note::

   ログイン認証だけを利用する場合は、「接続・認証設定」のみで動作します。
   「LDAP管理機能」（``ldap.admin.enabled``）は、管理画面からLDAP側の
   ユーザー／ロール／グループを作成・更新・削除する場合にのみ必要です。

接続・認証設定
==============

これらの設定は管理画面「システム > 全般」のLDAPセクションから設定でき、
``app/WEB-INF/conf/system.properties`` に保存されます。直接ファイルを編集することもできます。

.. list-table:: 接続・認証プロパティ
   :header-rows: 1
   :widths: 30 15 55

   * - プロパティ
     - デフォルト値
     - 説明
   * - ``ldap.provider.url``
     - （なし）
     - LDAPサーバーのURL。例: ``ldap://ldap.example.com:389``。LDAPSの場合は ``ldaps://ldap.example.com:636``。スペース区切りで複数指定するとフェイルオーバーになります。
   * - ``ldap.base.dn``
     - （なし）
     - LDAP検索のベースDN。例: ``dc=example,dc=com``
   * - ``ldap.security.principal``
     - （なし）
     - ユーザー認証（バインド）に使用するDNテンプレート。``%s`` がユーザー名に置換されます。例: ``uid=%s,ou=People,dc=example,dc=com``
   * - ``ldap.security.authentication``
     - ``simple``
     - LDAP認証方式（JNDIの ``java.naming.security.authentication``）。通常は ``simple`` を使用します。
   * - ``ldap.initial.context.factory``
     - ``com.sun.jndi.ldap.LdapCtxFactory``
     - JNDIの初期コンテキストファクトリクラス。通常は変更不要です。
   * - ``ldap.admin.security.principal``
     - （なし）
     - LDAP検索用サービスアカウントのバインドDN。例: ``cn=fess,ou=services,dc=example,dc=com``
   * - ``ldap.admin.security.credentials``
     - （なし）
     - 上記サービスアカウントのパスワード。
   * - ``ldap.account.filter``
     - （なし）
     - ユーザーのロール解決時に、ユーザーエントリを検索するためのフィルター。``%s`` がユーザー名に置換されます。例: ``uid=%s``
   * - ``ldap.group.filter``
     - （空）
     - グループ解決時に使用する検索フィルター。``%s`` がユーザーのDNなどに置換されます。例: ``(member=%s)``
   * - ``ldap.memberof.attribute``
     - ``memberOf``
     - グループメンバーシップを表す属性名。Active Directoryやこの属性を持つサーバーでロールを解決する際に使用します。

設定例（``system.properties`` を直接編集する場合）:

::

    # LDAPサーバーのURL
    ldap.provider.url=ldap://ldap.example.com:389

    # ベースDN
    ldap.base.dn=dc=example,dc=com

    # ユーザー認証用バインドDNテンプレート（%sにユーザー名が埋め込まれる）
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # 検索用サービスアカウントのバインドDNとパスワード
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # ロール解決用のフィルター
    ldap.account.filter=uid=%s
    ldap.group.filter=(member=%s)

.. note::

   ``%s`` プレースホルダーはJavaの ``String.format()`` で処理されます。
   ``ldap.security.principal`` ・ ``ldap.account.filter`` ・ ``ldap.group.filter`` ・
   各管理用フィルターはいずれも ``%s`` 形式を使用します（``{0}`` 形式ではありません）。
   なお、フィルターに渡されるユーザー名はLDAPインジェクション対策として
   |Fess| 内部で自動的にエスケープされます。

LDAP管理機能・動作設定
======================

以下のプロパティは ``app/WEB-INF/classes/fess_config.properties`` で定義されています。
値を変更する場合はこのファイルを編集します。

管理機能の有効化
----------------

.. list-table:: 管理機能プロパティ
   :header-rows: 1
   :widths: 35 15 50

   * - プロパティ
     - デフォルト値
     - 説明
   * - ``ldap.admin.enabled``
     - ``false``
     - 管理画面からLDAPのユーザー／ロール／グループを作成・更新・削除する機能を有効にします。**ログイン認証には不要**で、有効にしなくてもLDAPによるログインは機能します。
   * - ``ldap.admin.sync.password``
     - ``true``
     - 管理画面でユーザーを更新した際に、|Fess| 側のパスワードをLDAPと同期します。
   * - ``ldap.auth.validation``
     - ``true``
     - ログイン時にLDAP認証の検証を行います。

ユーザー／ロール／グループの管理用フィルターとベースDN
------------------------------------------------------

``ldap.admin.enabled=true`` の場合に、管理画面からLDAPエントリを操作するために使用します。

.. list-table:: 管理用フィルター／ベースDN
   :header-rows: 1
   :widths: 38 47 15

   * - プロパティ
     - 説明
     - デフォルト値
   * - ``ldap.admin.user.filter``
     - ユーザー検索フィルター（``%s`` がユーザー名に置換）
     - ``uid=%s``
   * - ``ldap.admin.user.base.dn``
     - ユーザー検索ベースDN
     - ``ou=People,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.user.object.classes``
     - ユーザー作成時のobjectClass
     - ``organizationalPerson,top,person,inetOrgPerson``
   * - ``ldap.admin.role.filter``
     - ロール検索フィルター
     - ``cn=%s``
   * - ``ldap.admin.role.base.dn``
     - ロール検索ベースDN
     - ``ou=Role,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.role.object.classes``
     - ロール作成時のobjectClass
     - ``groupOfNames``
   * - ``ldap.admin.group.filter``
     - グループ検索フィルター
     - ``cn=%s``
   * - ``ldap.admin.group.base.dn``
     - グループ検索ベースDN
     - ``ou=Group,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.group.object.classes``
     - グループ作成時のobjectClass
     - ``groupOfNames``

ロール解決と動作の制御
----------------------

ログイン後のロール／グループ解決の挙動を制御します。

.. list-table:: 動作制御プロパティ
   :header-rows: 1
   :widths: 40 15 45

   * - プロパティ
     - デフォルト値
     - 説明
   * - ``ldap.role.search.user.enabled``
     - ``true``
     - ユーザー名に基づくロールを付与します。
   * - ``ldap.role.search.group.enabled``
     - ``true``
     - グループに基づくロールを付与します。
   * - ``ldap.role.search.role.enabled``
     - ``true``
     - ロールに基づくロールを付与します。
   * - ``ldap.allow.empty.permission``
     - ``true``
     - グループ／ロールが空のユーザーのログインを許可します。
   * - ``ldap.ignore.netbios.name``
     - ``true``
     - グループ名などからNetBIOS名（``DOMAIN\`` 形式の接頭辞）を除去します。
   * - ``ldap.group.name.with.underscores``
     - ``false``
     - グループ名にアンダースコアを許可します。
   * - ``ldap.lowercase.permission.name``
     - ``false``
     - パーミッション名を小文字に変換します。
   * - ``ldap.samaccountname.group``
     - ``false``
     - グループ名に ``sAMAccountName`` 属性を使用します（Active Directory向け）。
   * - ``ldap.max.username.length``
     - ``-1``
     - ユーザー名の最大長。``-1`` は制限なしを意味します。

属性マッピング
--------------

LDAP属性と |Fess| のユーザー属性の対応は ``ldap.attr.*`` プロパティで定義されています。
通常は変更不要ですが、スキーマが異なる場合に調整できます。代表的な例:

::

    ldap.attr.surname=sn
    ldap.attr.givenName=givenName
    ldap.attr.mail=mail
    ldap.attr.displayName=displayName
    ldap.attr.telephoneNumber=telephoneNumber

.. note::

   ``ldap.attr.state`` は ``st``、``ldap.attr.city`` は ``l`` にマッピングされるなど、
   プロパティ名とLDAP属性名が一致しないものもあります。
   完全な一覧は ``fess_config.properties`` の ``ldap.attr.`` で始まる行を参照してください。

Active Directory設定
====================

Microsoft Active Directory向けの設定例です（``system.properties`` または管理画面）。

::

    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # ユーザー認証用バインドDNテンプレート（UPN形式）
    ldap.security.principal=%s@example.com

    # 検索用サービスアカウント
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # アカウントフィルター
    ldap.account.filter=sAMAccountName=%s

    # memberOf属性を使用
    ldap.memberof.attribute=memberOf

    # グループフィルター
    ldap.group.filter=(member=%s)

入れ子グループ（ネストグループ）を解決する場合は、Active Directory固有の
``LDAP_MATCHING_RULE_IN_CHAIN`` を使用できます。

::

    ldap.group.filter=(member:1.2.840.113556.1.4.1941:=%s)

OpenLDAP設定
============

OpenLDAP向けの設定例です。

::

    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # ユーザー認証用バインドDNテンプレート
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # 検索用サービスアカウント
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # アカウントフィルター
    ldap.account.filter=uid=%s

    # グループフィルター（posixGroupの場合）
    ldap.group.filter=(memberUid=%s)

.. note::

   標準のOpenLDAPは ``memberOf`` 属性を持たないため、
   ``ldap.group.filter`` を使ってグループを解決します。
   ``memberof`` オーバーレイを有効にしている場合は ``ldap.memberof.attribute`` も利用できます。

セキュリティ設定
================

LDAPS（SSL/TLS）
----------------

暗号化された接続を使用:

::

    # LDAPSを使用
    ldap.provider.url=ldaps://ldap.example.com:636

自己署名証明書の場合は、Java truststore に証明書をインポートします。

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

パスワードの保護
----------------

``ldap.admin.security.credentials`` は ``system.properties`` に保存されます。
管理画面から設定した認証情報は内部的に暗号化されて保存されます。
ファイルのアクセス権限を適切に制限してください。

フェイルオーバー
================

複数のLDAPサーバーへフェイルオーバーする場合は、``ldap.provider.url`` に
スペース区切りで複数のURLを指定します。

::

    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

トラブルシューティング
======================

接続エラー
----------

**症状**: LDAP接続に失敗する

**確認事項**:

1. LDAPサーバーが起動しているか
2. ファイアウォールでポートが開いているか（389または636）
3. ``ldap.provider.url`` が正しいか（``ldap://`` または ``ldaps://``）
4. ``ldap.admin.security.principal`` とパスワードが正しいか

認証エラー
----------

**症状**: ユーザー認証に失敗する

**確認事項**:

1. ``ldap.security.principal`` のテンプレートが正しいか（``%s`` を含むか）
2. ユーザーが指定したベースDN内に存在するか
3. ``ldap.account.filter`` が正しいか

グループ／ロールが取得できない
------------------------------

**症状**: ユーザーのグループやロールが取得できない

**確認事項**:

1. ``ldap.group.filter`` が正しいか
2. ``ldap.memberof.attribute`` が正しいか（Active Directoryの場合）
3. グループが検索ベースDN内に存在するか
4. ``ldap.role.search.*.enabled`` が有効になっているか

管理画面からのユーザー管理ができない
------------------------------------

**症状**: 管理画面でLDAPユーザーを作成・編集・削除できない

**確認事項**:

1. ``ldap.admin.enabled`` が ``true`` になっているか
2. ``ldap.admin.user.base.dn`` などの管理用ベースDNが正しいか
3. ``ldap.admin.security.principal`` のサービスアカウントに書き込み権限があるか

デバッグ設定
------------

詳細なログを出力するには、``app/WEB-INF/classes/log4j2.xml`` にロガーを追加します。

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

参考情報
========

- :doc:`security-role` - ロールベースのアクセス制御
- :doc:`sso-spnego` - SPNEGO（Kerberos）認証
- :doc:`../admin/user-guide` - ユーザー管理ガイド
